from pathlib import Path
from ...utils import kanban_utils, log_utils
from ...config.paths import ROOT_PATH, REPO_PATH
import click
from rich.console import Console
import json
import git
import os

repo = git.Repo.init(str(REPO_PATH))
logger = log_utils.get_logger()

console = Console()

kanban_path = ROOT_PATH / "kanban.json"


@click.group()
def kanban() -> None:
    """Creates the main click group for kanban boards."""
    pass


@kanban.command()
@click.argument("name")
@click.argument("status")
@click.argument("description")
@click.argument("tags")
def add(name: str, status: str, description: str, tags: str) -> None:
    """Adds a card to the kanban board.

    :param name: Name of the card.
    :type name: str
    :param status: Status of the card.
    :type status: str
    :param description: Description of the card.
    :type description: str
    :param tags: Tags for the card.
    :type tags: str
    :rtype: None
    """

    words = tags.split(" ")
    extracted_tags = [word[1:] for word in words if word[0] == "@"]

    description = description.strip()
    try:
        with kanban_path.open("r") as kanban_file:
            kanban_json = json.load(kanban_file)

            card_id = len([card for card in kanban_json]) + 1
            if description == "+file":
                description_file_name = input("Enter file path to load description: ")
                content = {
                    "id": ("#" + str(card_id)),
                    "name": name,
                    "status": status.lower(),
                    "description": os.fspath(Path(description_file_name)),
                    "tags": extracted_tags,
                }
            else:
                content = {
                    "id": ("#" + str(card_id)),
                    "name": name,
                    "status": status.lower(),
                    "description": description,
                    "tags": extracted_tags,
                }
            kanban_json.append(content)

            with kanban_path.open("w") as kanban_file:
                kanban_json = json.dump(kanban_json, kanban_file)
                console.print(
                    f':white_check_mark: "{name}" has been added to the board!'
                )
    except FileNotFoundError as e:
        with kanban_path.open("a") as kanban_file:
            kanban_file.write("[]")
        logger.error(e)
        console.print(
            ":cross_mark: Failed to write to the file! Please check the logs in the home directory."
        )


@kanban.command()
@click.argument("id")
def delete(id: str) -> None:
    """Deletes a card from the kanban board.

    :param id: ID of the card.
    :type id: str
    :rtype: None
    """

    try:
        kanban_json = None
        with kanban_path.open("r") as kanban_file:
            kanban_json = json.load(kanban_file)

        filtered_kanban = [card for card in kanban_json if card["id"] != id]

        try:
            with kanban_path.open("w") as kanban_file:
                filtered_kanban = json.dump(filtered_kanban, kanban_file)
        except FileNotFoundError as e:
            logger.error(e)
            console.print(
                ":cross_mark: Failed to write to the file! Please check the logs in the home directory."
            )

    except FileNotFoundError as e:
        logger.error(e)
        console.print(
            ":cross_mark: Failed to read from the file! Please check the logs in the home directory."
        )


@kanban.command()
@click.argument("id")
@click.argument("name")
@click.argument("description")
@click.argument("tags")
def edit(id: str, name: str, description: str, tags: str) -> None:
    """Edits a card in the kanban board.

    :param id: ID of the card.
    :type id: str
    :param name: Name of the card.
    :type name: str
    :param description: Description of the card.
    :type description: str
    :param tags: Tags for the card.
    :type tags: str
    :rtype: None
    """

    words = tags.split(" ")
    extracted_tags = [word[1:] for word in words if word[0] == "@"]

    try:
        with kanban_path.open("r") as kanban_file:
            kanban_json = json.load(kanban_file)
            filtered_kanban = kanban_json

            for card in filtered_kanban:
                if card["id"] == id:
                    if name.strip() != ".":
                        card["name"] = name

                    if description.strip() == "+file":
                        description_file_name = input(
                            "Enter file path to load description: "
                        )

                        card["description"] = os.fspath(Path(description_file_name))
                    else:
                        if description != ".":
                            card["description"] = description

                    if tags.strip() != ".":
                        card["tags"] = extracted_tags

            with kanban_path.open("w") as kanban_file:
                filtered_kanban = json.dump(filtered_kanban, kanban_file)
                console.print(
                    f":white_check_mark: Card {id} has been modified in the kanban!"
                )
                repo.index.add([str(kanban_path)])
                repo.index.commit(f"Modified Card {id} in the kanban board.")
                console.print(
                    f":white_check_mark: Card {id} has been modified in the git repository!"
                )

    except FileNotFoundError as e:
        with kanban_path.open("a") as kanban_file:
            kanban_file.write("[]")
        logger.error(e)
        console.print(
            ":cross_mark: Failed to write to the file! Please check the logs in the home directory."
        )


@kanban.command()
@click.argument("id")
@click.argument("new_status")
def move_card(id: str, new_status: str) -> None:
    """Moves a card to the specified status.

    :param id: ID of the card.
    :type id: str
    :param new_status: The new status to which the card should be moved to.
    :type new_status: str
    :rtype: None
    """

    try:
        kanban_json = None
        with kanban_path.open("r") as kanban_file:
            kanban_json = json.load(kanban_file)

        filtered_kanban = kanban_json

        for task in filtered_kanban:
            if task["id"] == id:
                task["status"] = new_status

        try:
            with kanban_path.open("w") as kanban_file:
                filtered_kanban = json.dump(filtered_kanban, kanban_file)
        except FileNotFoundError as e:
            logger.error(e)
            console.print(
                ":cross_mark: Failed to write to the file! Please check the logs in the home directory."
            )

    except FileNotFoundError as e:
        logger.error(e)
        console.print(
            ":cross_mark: Failed to read from the file! Please check the logs in the home directory."
        )


@kanban.command()
def show() -> None:
    """Shows the kanban board."""

    try:
        with kanban_path.open("r") as kanban_file:
            kanban_content = json.load(kanban_file)
            kanban_utils.parse_kanban(kanban_content)
    except FileNotFoundError as e:
        logger.error(e)
        console.print(
            ":cross_mark: Failed to read from the file! Please check the logs in the home directory."
        )
