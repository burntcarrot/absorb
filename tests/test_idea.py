import click.testing
import pytest
import os
from pathlib import Path
from click.testing import CliRunner
from absorb.core.idea.commands import idea
from absorb.config.paths import ROOT_PATH


@pytest.fixture
def runner() -> CliRunner:
    return click.testing.CliRunner()


file_path = os.fspath(
    Path(Path.cwd() / Path(Path("tests") / Path("files") / "idea_description.txt"))
)

# Tests for new() (new idea)
def test_idea_new(runner: CliRunner) -> None:
    """Adding an idea normally should return 0, if it is valid in nature."""
    result = runner.invoke(
        idea, ["new", "Make a cool machine!", "Some description.", "@ideas"]
    )
    assert result.exit_code == 0


def test_idea_new_empty_description(runner: CliRunner) -> None:
    """Adding an idea normally should return 0, if it is valid in nature."""
    result = runner.invoke(idea, ["new", ".", ".", "."])
    assert result.exit_code == 0


def test_idea_new_description_file(runner: CliRunner) -> None:
    """Adding an idea with decription file should return 0, if it is valid in nature."""
    result = runner.invoke(
        idea, ["new", "Make a cool machine!", "+file", "@file"], input=file_path
    )
    assert result.exit_code == 0


def test_idea_new_no_tags(runner: CliRunner) -> None:
    """Adding an idea with no tags should return 0, if it is valid in nature."""
    result = runner.invoke(
        idea, ["new", "Make a cool machine!", "Some description.", "."]
    )
    assert result.exit_code == 0


def test_idea_new_FileNotFoundError(runner: CliRunner) -> None:
    """Adding an idea normally but ideas.json doesnt exist should return 0, if it is valid in nature."""
    os.rename(ROOT_PATH / "ideas.json", ROOT_PATH / "_ideas.json")
    result = runner.invoke(
        idea, ["new", "Make a cool machine!", "Some description.", "@ideas"]
    )
    assert result.exit_code == 0
    os.remove(ROOT_PATH / "ideas.json")
    os.rename(ROOT_PATH / "_ideas.json", ROOT_PATH / "ideas.json")


# Tests for edit() (edit idea)
def test_idea_edit(runner: CliRunner) -> None:
    """Editing an idea normally should return 0, if it is valid in nature."""
    result = runner.invoke(
        idea,
        [
            "edit",
            "#1",
            "Make a super cool machine!",
            "New description.",
            "@ideas @create",
        ],
    )
    assert result.exit_code == 0


def test_idea_edit_with_no_tags(runner: CliRunner) -> None:
    """Editing an idea with no tags should return 0, if it is valid in nature."""
    result = runner.invoke(
        idea, ["edit", "#1", "Make a super cool machine!", "New description.", "."]
    )
    assert result.exit_code == 0


def test_idea_edit_only_name(runner: CliRunner) -> None:
    """Editing an idea's name with no tags or description should return 0, if it is valid in nature."""
    result = runner.invoke(idea, ["edit", "#1", "Make a super cool machine!", ".", "."])
    assert result.exit_code == 0


def test_idea_edit_with_description_file(runner: CliRunner) -> None:
    """Editing an idea with description file should return 0, if it is valid in nature."""
    result = runner.invoke(
        idea,
        ["edit", "#1", "Make a super cool machine!", "+file", "."],
        input=file_path,
    )
    assert result.exit_code == 0


def test_idea_edit_only_tags(runner: CliRunner) -> None:
    """Editing an idea's tags with no description or name should return 0, if it is valid in nature."""
    result = runner.invoke(idea, ["edit", "#1", ".", ".", "@create"])
    assert result.exit_code == 0


def test_idea_edit_with_no_tags_FileNotFoundError(runner: CliRunner) -> None:
    """Editing an idea with no tags but ideas.json doesnt exist should return 0, if it is valid in nature."""
    os.rename(ROOT_PATH / "ideas.json", ROOT_PATH / "_ideas.json")
    result = runner.invoke(
        idea, ["edit", "#1", "Make a super cool machine!", "New description.", "."]
    )
    assert result.exit_code == 0
    os.remove(ROOT_PATH / "ideas.json")
    os.rename(ROOT_PATH / "_ideas.json", ROOT_PATH / "ideas.json")


# Tests for open() (open idea)
def test_idea_open(runner: CliRunner) -> None:
    """Opening an idea should return 0, if it is valid in nature."""
    result = runner.invoke(idea, ["open", "#1"])
    assert result.exit_code == 0


# this will cover absorb\utils\idea_utils.py 58 but only works if the
# #2 idea has . as description
def test_idea_open_2(runner: CliRunner) -> None:
    """Opening an idea should return 0, if it is valid in nature."""
    result = runner.invoke(idea, ["open", "#2"])
    assert result.exit_code == 0


def test_idea_open_FileNotFoundError(runner: CliRunner) -> None:
    """Opening an idea bit ideas.json doesnt exist should return 0, if it is valid in nature."""
    os.rename(ROOT_PATH / "ideas.json", ROOT_PATH / "_ideas.json")
    result = runner.invoke(idea, ["open", "#2"])
    assert result.exit_code == 0
    os.rename(ROOT_PATH / "_ideas.json", ROOT_PATH / "ideas.json")


# Tests for show() (show idea)
def test_idea_show(runner: CliRunner) -> None:
    """Showing all ideas should return 0, if it is valid in nature."""
    result = runner.invoke(idea, ["show"])
    assert result.exit_code == 0


def test_idea_show_FileNotFoundError(runner: CliRunner) -> None:
    """Showing all ideas but ideas.json doesnt exist should return 0, if it is valid in nature."""
    os.rename(ROOT_PATH / "ideas.json", ROOT_PATH / "_ideas.json")
    result = runner.invoke(idea, ["show"])
    assert result.exit_code == 0
    os.remove(ROOT_PATH / "ideas.json")
    os.rename(ROOT_PATH / "_ideas.json", ROOT_PATH / "ideas.json")
