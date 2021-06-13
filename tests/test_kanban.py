import click.testing
import pytest
import os
from pathlib import Path
from click.testing import CliRunner
from absorb.core.kanban.commands import kanban


@pytest.fixture
def runner() -> CliRunner:
    return click.testing.CliRunner()


# Tests for add() (add card)
def test_kanban_add_card(runner: CliRunner) -> None:
    """Adding a card should return 0, if it is valid in nature."""
    result = runner.invoke(
        kanban, ["add", "New card.", "doing", "Some description.", "@new"]
    )
    assert result.exit_code == 0


def test_kanban_add_card_no_tags(runner: CliRunner) -> None:
    """Adding a card should return 0, if it is valid in nature."""
    result = runner.invoke(
        kanban, ["add", "New card.", "doing", "Some description.", "."]
    )
    assert result.exit_code == 0


card_path = os.fspath(
    Path(Path.cwd() / Path(Path("tests") / Path("files") / "example-fail.json"))
)


def test_kanban_add_card_with_input_file_description(runner: CliRunner) -> None:
    """Adding a card with input file should return 0, if it is valid in nature."""
    result = runner.invoke(
        kanban, ["add", "New card.", "doing", "+file", "@new"], input=card_path
    )
    assert result.exit_code == 0


# Tests for delete() (delete card)
def test_kanban_delete_card(runner: CliRunner) -> None:
    """Deleting a card should return 0, if it is valid in nature."""
    result = runner.invoke(kanban, ["delete", "#1"])
    assert result.exit_code == 0


# Tests for edit() (edit card)
def test_kanban_edit_card_only_name(runner: CliRunner) -> None:
    """Editing a card's name should return 0, if it is valid in nature."""
    result = runner.invoke(kanban, ["edit", "#2", "New name.", ".", "."])
    assert result.exit_code == 0


def test_kanban_edit_card_name_and_description(runner: CliRunner) -> None:
    """Editing a card's name and description should return 0, if it is valid in nature."""
    result = runner.invoke(kanban, ["edit", "#2", "New name.", "New description.", "."])
    assert result.exit_code == 0


def test_kanban_edit_card_name_description_tags(runner: CliRunner) -> None:
    """Editing a card's name, description and tags should return 0, if it is valid in nature."""
    result = runner.invoke(
        kanban, ["edit", "#2", "New name.", "New description.", "@new-tag"]
    )
    assert result.exit_code == 0


# Tests for move_card() (move card)
def test_kanban_move_card(runner: CliRunner) -> None:
    """Moving a card should return 0, if it is valid in nature."""
    result = runner.invoke(kanban, ["move-card", "#2", "completed"])
    assert result.exit_code == 0


# Tests for show() (show kanban board)
def test_kanban_show(runner: CliRunner) -> None:
    """Showing the board should return 0."""
    result = runner.invoke(kanban, ["show"])
    assert result.exit_code == 0
