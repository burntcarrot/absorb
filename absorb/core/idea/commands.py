import click
import os
import json
import git
from pathlib import Path
from rich.console import Console
from ...utils import idea_utils, log_utils
from ...config.paths import ROOT_PATH, REPO_PATH


repo = git.Repo.init(str(REPO_PATH))
logger = log_utils.get_logger()

console = Console()

idea_path = ROOT_PATH / "ideas.json"


@click.group()
def idea() -> None:
    """The main click group for idea."""

    pass


@idea.command()
@click.argument("name")
@click.argument("description")
@click.argument("tags")
def new(name: str, description: str, tags: str) -> None:
    """Adds a new idea to ideas.json and commits the idea to the git repository.

    :param name: Name of the idea.
    :type name: str
    :param description: Description of the idea.
    :type description: str
    :param tags: Tags for the idea.
    :type tags: str
    :rtype: None
    """

    words = tags.split(" ")
    extracted_tags = [word[1:] for word in words if word[0] == "@"]

    description = description.strip()
    try:
        with idea_path.open("r") as ideas_file:
            ideas_json = json.load(ideas_file)
            card_id = len([idea for idea in ideas_json]) + 1
            if description == "+file":
                description_file_name = input("Enter file path to load description: ")
                content = {
                    "id": ("#" + str(card_id)),
                    "name": name,
                    "description": os.fspath(Path(description_file_name)),
                    "tags": extracted_tags,
                }
            else:
                content = {
                    "id": ("#" + str(card_id)),
                    "name": name,
                    "description": description,
                    "tags": extracted_tags,
                }

            ideas_json.append(content)

            with idea_path.open("w") as ideas_file:
                ideas_json = json.dump(ideas_json, ideas_file)
                console.print(
                    f':white_check_mark: "{name}" has been added to the list!'
                )

            repo.index.add([str(REPO_PATH / "ideas.json")])
            repo.index.commit(f'Added idea "{name}"')
    except FileNotFoundError as e:
        with idea_path.open("a") as ideas_file:
            ideas_file.write("[]")
        logger.error(e)
        console.print(
            ":cross_mark: Failed to write to the file! Please check the logs in the home directory."
        )


@idea.command()
@click.argument("id")
@click.argument("name")
@click.argument("description")
@click.argument("tags")
def edit(id: str, name: str, description: str, tags: str) -> None:
    """Edits an existing idea in ideas.json and commits the changes in the git repository.

    :param id: ID of the idea.
    :type id: str
    :param name: Name of the idea.
    :type name: str
    :param description: Description of the idea.
    :type description: str
    :param tags: Tags for the idea.
    :type tags: str
    :rtype: None
    """

    words = tags.split(" ")
    extracted_tags = [word[1:] for word in words if word[0] == "@"]

    try:
        with idea_path.open("r") as idea_file:
            idea_json = json.load(idea_file)
            filtered_idea = idea_json

            for card in filtered_idea:
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

            with idea_path.open("w") as idea_file:
                filtered_idea = json.dump(filtered_idea, idea_file)
                console.print(
                    f":white_check_mark: Card {id} has been modified in the idea!"
                )
                repo.index.add([str(idea_path)])
                repo.index.commit(f"Modified Card {id} in the idea board.")
                console.print(
                    f":white_check_mark: Card {id} has been modified in the git repository!"
                )

    except FileNotFoundError as e:
        with idea_path.open("a") as idea_file:
            idea_file.write("[]")
        logger.error(e)
        console.print(
            ":cross_mark: Failed to write to the file! Please check the logs in the home directory."
        )


@idea.command()
@click.argument("id")
def open(id: str) -> None:
    """Opens an idea present in ideas.json

    :param id: ID of the idea.
    :type id: str
    :rtype: None
    """

    try:
        with idea_path.open("r") as idea_file:
            idea_content = json.load(idea_file)
            filtered_ideas = []
            for idea in idea_content:
                if idea["id"] == id:
                    filtered_ideas.append(idea)
            idea_utils.open_idea(filtered_ideas)
    except FileNotFoundError as e:
        logger.error(e)
        console.print(
            ":cross_mark: Failed to read from the file! Please check the logs in the home directory."
        )


@idea.command()
def show() -> None:
    """Shows all ideas present in ideas.json"""

    try:
        with idea_path.open("r") as ideas_file:
            idea_content = json.load(ideas_file)
            idea_utils.parse_ideas(idea_content)
    except FileNotFoundError as e:
        with idea_path.open("a") as idea_file:
            idea_file.write("[]")
        logger.error(e)
        console.print(
            ":cross_mark: Failed to write to the file! Please check the logs in the home directory."
        )
