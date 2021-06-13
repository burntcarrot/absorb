from typing import Any
from rich.table import Table
from rich.console import Console
from pathlib import Path

kanban_board = Table(show_header=True, header_style="bold")
kanban_board.add_column("Completed")
kanban_board.add_column("Doing")
kanban_board.add_column("Planned")

console = Console()


def parse_card(card: Any) -> str:
    """Returns a string containing the card content.

    :param card: JSON object containing data for the card.
    :type card: Any
    :return: Formatted string with the card.
    :rtype: str
    """

    card_id = card["id"]
    card_name = card["name"]
    card_tags = card["tags"]
    card_description_path = Path(card["description"])

    card_description = card["description"]

    if card_description != ".":
        try:
            if card_description_path.is_file():
                with card_description_path.open("r") as card_description_file:
                    card_description = "".join(card_description_file.readlines())
        except FileNotFoundError:
            console.print(
                ":cross_mark: Failed to read from the file! Please check the logs in the home directory."
            )
        return f"[bold red]{card_id}[/bold red]\n{card_name}\n[bold yellow]\ndescription:\n{card_description}\ntags: {card_tags}[/bold yellow]\n"
    else:
        return f"[bold red]{card_id}[/bold red]\n{card_name}\n[bold yellow]tags: {card_tags}[/bold yellow]\n"


def parse_kanban(content: Any) -> None:
    """Prints the kanban board.

    :param content: File content containing cards.
    :type content: Any
    :rtype: None
    """

    cards = {"completed": [], "doing": [], "planned": []}

    for task in content:
        card = task
        # print(task)
        if card["status"] == "completed":
            cards["completed"].append(card)
        elif card["status"] == "doing":
            cards["doing"].append(card)
        elif card["status"] == "planned":
            cards["planned"].append(card)

    completed_cards = "\n".join([parse_card(card) for card in cards["completed"]])
    doing_cards = "\n".join([parse_card(card) for card in cards["doing"]])
    planned_cards = "\n".join([parse_card(card) for card in cards["planned"]])
    kanban_board.add_row(completed_cards, doing_cards, planned_cards)
    console.print(kanban_board)
