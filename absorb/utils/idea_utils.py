from rich.table import Table
from rich.console import Console
from pathlib import Path
from typing import Any

console = Console()


def parse_ideas(file_content: Any) -> None:
    """Prints the ideas table.

    :param file_content: File content containing ideas.
    :type file_content: Any
    :rtype: None
    """

    ideas_table = Table(show_header=True, header_style="bold")
    ideas_table.add_column("ID")
    ideas_table.add_column("Idea Name")
    ideas_table.add_column("Tags")
    for idea in file_content:
        idea_entry = idea
        tags = idea_entry["tags"]
        ideas_table.add_row(
            idea_entry["id"], idea_entry["name"], f"[bold yellow]{tags}[/bold yellow]"
        )

    console.print(ideas_table)


def parse_idea(idea: Any) -> str:
    """Returns a string containing the idea.

    :param idea: JSON object containing data for the idea.
    :type idea: Any
    :return: Formatted string with the idea.
    :rtype: str
    """

    idea_id = idea["id"]
    idea_name = idea["name"]
    idea_tags = idea["tags"]
    idea_description_path = Path(idea["description"])

    idea_description = idea["description"]

    if idea_description != ".":
        try:
            if idea_description_path.is_file():
                with idea_description_path.open("r") as idea_description_file:
                    idea_description = "".join(idea_description_file.readlines())
        except FileNotFoundError:
            console.print(
                ":cross_mark: Failed to read from the file! Please check the logs in the home directory."
            )
        return f"\n[bold red]Idea ID: {idea_id}[/bold red]\n[bold magenta]{idea_name}[/bold magenta]\n\n[bold green]Idea Description:[/bold green]\n\n{idea_description}\n\n[bold yellow]Tags: {idea_tags}[/bold yellow]\n"
    else:
        return f"\n[bold red]Idea ID: {idea_id}[/bold red]\n[bold magenta]{idea_name}[/bold magenta]\n[bold yellow]Tags: {idea_tags}[/bold yellow]\n"


def open_idea(file_content: Any) -> None:
    """Prints the parsed idea.

    :param file_content: File content containing the idea.
    :type file_content: Any
    :rtype: None
    """

    for idea in file_content:
        console.print(parse_idea(idea))
