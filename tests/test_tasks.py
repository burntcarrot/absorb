import click.testing
import pytest
import os
from pathlib import Path
from click.testing import CliRunner
from datetime import datetime, timedelta
from absorb.core.tasks.commands import tasks, parse_date, load_json
from absorb.config.paths import ROOT_PATH


@pytest.fixture
def runner() -> CliRunner:
    return click.testing.CliRunner()


# parse date
def test_parse_date_optional() -> None:
    """A dot(.) means that parse_date should return the current time."""
    result = parse_date(".")
    assert result.replace(microsecond=0) == datetime.now().replace(microsecond=0)


def test_parse_dates_only_plus() -> None:
    """A plus sign (+) with no characters should return the current time."""
    result = parse_date("+")
    assert result.replace(microsecond=0) == datetime.now().replace(microsecond=0)


def test_parse_dates_plus_with_character() -> None:
    """A plus sign (+) with invalid characters should return the current time."""
    result = parse_date("+1")
    assert result.replace(microsecond=0) == datetime.now().replace(microsecond=0)


def test_parse_dates_only_day() -> None:
    """A plus sign (+) with a 'd' character should return the amount of days being added to the current time."""
    result = parse_date("+1d")
    assert result.replace(microsecond=0) == (
        datetime.now() + timedelta(days=float(1))
    ).replace(microsecond=0)


def test_parse_dates_day_with_hours() -> None:
    """A plus sign (+) with 'd' and 'h' characters should return the amount of days and hours being added to the current time."""
    result = parse_date("+1d 5h")
    assert result.replace(microsecond=0) == (
        datetime.now() + timedelta(days=float(1), hours=float(5))
    ).replace(microsecond=0)


def test_parse_dates_day_with_hours_minutes() -> None:
    """A plus sign (+) with 'd', 'h' and 'm' characters should return the amount of days, hours and minutes being added to the current time."""
    result = parse_date("+1d 5h 5m")
    assert result.replace(microsecond=0) == (
        datetime.now() + timedelta(days=float(1), hours=float(5), minutes=float(5))
    ).replace(microsecond=0)


def test_parse_dates_day_with_hours_minutes_seconds() -> None:
    """A plus sign (+) with 'd', 'h', 'm' and 's' characters should return the amount of days, hours, minutes and seconds being added to the current time."""
    result = parse_date("+1d 5h 5m 5s")
    assert result.replace(microsecond=0) == (
        datetime.now()
        + timedelta(days=float(1), hours=float(5), minutes=float(5), seconds=float(5))
    ).replace(microsecond=0)


def test_parse_dates_invalid_char() -> None:
    """A invalid character should return the current time."""
    result = parse_date("x")
    assert result.replace(microsecond=0) == (datetime.now()).replace(microsecond=0)


def test_parse_dates_invalid_len() -> None:
    """Invalid characters should return the current time."""
    result = parse_date("xyz")
    assert result.replace(microsecond=0) == (datetime.now()).replace(microsecond=0)


def test_parse_dates_only_day_args() -> None:
    """A plus sign (+) with a 'd' character should return the amount of days being added to the give time (args)."""
    result = parse_date("+1d", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    assert result.replace(microsecond=0) == (
        datetime.now() + timedelta(days=float(1))
    ).replace(microsecond=0)


def test_parse_dates_date_string() -> None:
    """Parses a date string and returns a datetime object after parsing the date string."""
    result = parse_date(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    assert result.replace(microsecond=0) == (datetime.now()).replace(microsecond=0)


# JSON path from root folder
json_path = Path(Path.cwd() / Path(Path("tests") / Path("files") / "example-fail.json"))


# Tests for load_json
def test_load_json_fail() -> None:
    """If the file couldn't be opened by load_json, it would return -1."""
    with json_path.open("r") as tasks_file:
        result = load_json(tasks_file)

    assert result == -1


# Test to check if a command fails if file is not found
def test_task_no_file(runner: CliRunner) -> None:
    """Adding a task normally should return 0, but if a file is not found, it should return -1."""
    result = runner.invoke(tasks, ["add", "New task.", ".", "low", "."])
    assert result.exit_code == 0


def test_task_show_group_valid_hour(runner: CliRunner) -> None:
    """Adding a task with duedate in 5 hours should return 0, if the group is valid in nature."""
    # mock entry
    result = runner.invoke(tasks, ["add", "New task.", "+5h", "low", "@relax"])
    assert result.exit_code == 0


# Tests for show() and show_group()
def test_task_show_group_valid(runner: CliRunner) -> None:
    """Showing a task (by group) should return 0, if the group is valid in nature."""
    # mock entry
    runner.invoke(tasks, ["add", "New task.", "+4d", "low", "@relax"])
    result = runner.invoke(tasks, ["show-group", "@relax"])
    assert result.exit_code == 0


def test_task_show_group_invalid(runner: CliRunner) -> None:
    """Showing a task (by group) should return -1, if the group is invalid in nature."""
    result = runner.invoke(tasks, ["show-group", "not a tag"])
    assert result.exit_code == -1


def test_task_show_group_valid_FileNotFoundError(runner: CliRunner) -> None:
    """Showing a task (by group) but task.json doesn't exist it should return -1."""
    # mock entry
    os.rename(ROOT_PATH / "tasks.json", ROOT_PATH / "_tasks.json")
    runner.invoke(tasks, ["add", "New task.", "+4d", "low", "@relax"])
    result = runner.invoke(tasks, ["show-group", "@relax"])
    assert result.exit_code == -1
    os.remove(ROOT_PATH / "tasks.json")
    os.rename(ROOT_PATH / "_tasks.json", ROOT_PATH / "tasks.json")


def test_task_show(runner: CliRunner) -> None:
    """The show command for tasks should return 0."""
    result = runner.invoke(tasks, ["show"])
    assert result.exit_code == 0


def test_task_show_FileNotFoundError(runner: CliRunner) -> None:
    """The show command for tasks but tasks.json doesn't existshould return -1."""
    os.rename(ROOT_PATH / "tasks.json", ROOT_PATH / "_tasks.json")
    result = runner.invoke(tasks, ["show"])
    assert result.exit_code == -1
    os.remove(ROOT_PATH / "tasks.json")
    os.rename(ROOT_PATH / "_tasks.json", ROOT_PATH / "tasks.json")


# Tests for add() (add task)

# because test_task_show runs before test_task_add, a new tasks.json is created already.
def test_task_add(runner: CliRunner) -> None:
    """Adding a task normally should return 0, if it is valid in nature."""
    result = runner.invoke(tasks, ["add", "New task.", ".", "low", "."])
    assert result.exit_code == 0


def test_task_add_with_date_and_groups(runner: CliRunner) -> None:
    """Adding a task with a date and a group should return 0, if it is valid in nature."""
    result = runner.invoke(tasks, ["add", "New task.", "+4d", "low", "@relax"])
    assert result.exit_code == 0


def test_task_add_with_groups(runner: CliRunner) -> None:
    """Adding a task with a group should return 0, if it is valid in nature."""
    result = runner.invoke(tasks, ["add", "New task.", ".", "low", "@relax"])
    assert result.exit_code == 0


# Tests for edit() (edit task)
def test_task_edit(runner: CliRunner) -> None:
    """Editing a task normally should return 0, if it is valid in nature."""
    result = runner.invoke(tasks, ["edit", "#1", "Modified task.", ".", "low", "."])
    assert result.exit_code == 0


def test_task_edit_FileNotFoundError(runner: CliRunner) -> None:
    """Editing a task normally but tasks.json doesn't exist should return 0, if it is valid in nature."""
    os.rename(ROOT_PATH / "tasks.json", ROOT_PATH / "_tasks.json")
    result = runner.invoke(tasks, ["edit", "#1", "Modified task.", ".", "low", "."])
    assert result.exit_code == 0
    os.remove(ROOT_PATH / "tasks.json")
    os.rename(ROOT_PATH / "_tasks.json", ROOT_PATH / "tasks.json")


def test_task_edit_with_date_and_groups(runner: CliRunner) -> None:
    """Editing a task with a date and groups should return 0, if it is valid in nature."""
    result = runner.invoke(
        tasks, ["edit", "#1", "Modified task.", "+4d", "low", "@relax @chill"]
    )
    assert result.exit_code == 0


def test_task_edit_with_groups(runner: CliRunner) -> None:
    """Editing a task with groups should return 0, if it is valid in nature."""
    result = runner.invoke(
        tasks, ["edit", "#1", "Modified task.", ".", ".", "@relax @chill"]
    )
    assert result.exit_code == 0


# Tests for delete() (delete task)
def test_task_delete(runner: CliRunner) -> None:
    """Deleting a task with the help of a ID should return 0, if it is valid in nature."""
    result = runner.invoke(tasks, ["delete", "#1"])
    assert result.exit_code == 0


def test_task_delete_FileNotFoundError(runner: CliRunner) -> None:
    """Deleting a task with the help of a ID but tasks.json doesn't existshould return 0, if it is valid in nature."""
    os.rename(ROOT_PATH / "tasks.json", ROOT_PATH / "_tasks.json")
    result = runner.invoke(tasks, ["delete", "#1"])
    assert result.exit_code == 0
    os.remove(ROOT_PATH / "tasks.json")
    os.rename(ROOT_PATH / "_tasks.json", ROOT_PATH / "tasks.json")
