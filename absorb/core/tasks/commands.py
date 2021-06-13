import click
import json
import git
import sys
from json.decoder import JSONDecodeError
from datetime import datetime, timedelta
from rich.console import Console
from typing import Any, TextIO
from ...config.paths import ROOT_PATH, REPO_PATH
from ...utils import tasks_utils, log_utils

repo = git.Repo.init(str(REPO_PATH))
logger = log_utils.get_logger()

console = Console()

tasks_path = ROOT_PATH / "tasks.json"


@click.group()
def tasks() -> None:
    """The main click group for tasks."""
    pass


def parse_date(date_str: str, *args: str) -> datetime:
    """Parses a date string and returns a datetime object after parsing the date string. The date string might contain some values which tells the function to shift the date by a particular period.

    :param date_str: Date string.
    :type date_str: str
    :param args: Optional arguments.
    :type args: str
    :return: Datetime object.
    :rtype: datetime
    """
    days_filtered = 0
    hours_filtered = 0
    minutes_filtered = 0
    seconds_filtered = 0

    if date_str == ".":
        return datetime.now()
    elif date_str[0] == "+" and len(date_str) > 1:
        token_list = date_str[1:].split()
        for token in token_list:
            if token[-1] == "d":
                days_filtered = int(token[:-1])
            elif token[-1] == "h":
                hours_filtered = int(token[:-1])
            elif token[-1] == "m":
                minutes_filtered = int(token[:-1])
            elif token[-1] == "s":
                seconds_filtered = int(token[:-1])
            else:
                pass

        if len(args) > 0:
            task_due_str = args[0]
            task_due_date = datetime.strptime(task_due_str, "%Y-%m-%d %H:%M:%S.%f")
            shifted_date = task_due_date + timedelta(
                days=float(days_filtered),
                hours=float(hours_filtered),
                minutes=float(minutes_filtered),
                seconds=float(seconds_filtered),
            )
        else:
            shifted_date = datetime.now() + timedelta(
                days=float(days_filtered),
                hours=float(hours_filtered),
                minutes=float(minutes_filtered),
                seconds=float(seconds_filtered),
            )

        return shifted_date
    elif len(date_str) > 1:
        try:
            task_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
            return task_date
        except ValueError as e:
            logger.warning("Date string provided: " + date_str)
            logger.error(e)
            console.print(
                ":cross_mark: Invalid date string provided. Continued with current date as the due date. Check the logs in the home directory to know more."
            )
            return datetime.now()
    else:
        logger.warning("Date string provided: " + date_str)
        console.print(
            ":cross_mark: Invalid date string provided. Continued with current date as the due date. Check the logs in the home directory to know more."
        )
        return datetime.now()


def load_json(tasks_file: TextIO) -> Any:
    """Loads a file pointer and returns a JSON object. Used as a utility for checking any encoding/decoding while reading a JSON file.

    :param tasks_file: File pointer for the JSON file.
    :type tasks_file: TextIO
    :return: JSON object.
    :rtype: Any
    """
    tasks_json = None
    try:
        tasks_json = json.load(tasks_file)
        return tasks_json
    except JSONDecodeError as e:
        logger.error(e)
        console.print(
            ":cross_mark: Failed to read from the file! This might be due to corruption of the file. Please backup from the previous commits in the git repository, if possible."
        )

        # return -1 to sys.exit(-1)
        return -1


@tasks.command()
@click.argument("name")
@click.argument("due_date")
@click.argument("priority")
@click.argument("group")
def add(name: str, due_date: str, priority: str, group: str) -> None:
    """Adds a new task to tasks.json and commits the task to the git repository.

    :param name: Name of the task.
    :type name: str
    :param due_date: Due date for the task.
    :type due_date: str
    :param priority: Priority for the task.
    :type priority: str
    :param group: Group for the task.
    :type group: str
    :rtype: None
    """

    words = group.split(" ")
    extracted_groups = [word[1:] for word in words if word[0] == "@"]

    task_date = parse_date(due_date)

    try:
        with tasks_path.open("r") as tasks_file:
            tasks_json = load_json(tasks_file)
            if tasks_json == -1:
                sys.exit(-1)

            task_id = len([task for task in tasks_json]) + 1
            content = {
                "id": ("#" + str(task_id)),
                "name": name,
                "date": str(datetime.now()),
                "due_date": str(task_date),
                "priority": priority.lower(),
                "group": extracted_groups,
            }

            tasks_json.append(content)

            with tasks_path.open("w") as tasks_file:
                tasks_json = json.dump(tasks_json, tasks_file)
                console.print(
                    f':white_check_mark: "{name}" has been added to the list!'
                )
                repo.index.add([str(tasks_path)])
                repo.index.commit(f'Added "{name}" in tasks.')
                console.print(
                    f':white_check_mark: "{name}" has been added to the git repository!'
                )

    except FileNotFoundError as e:
        with tasks_path.open("a") as tasks_file:
            tasks_file.write("[]")
        logger.error(e)
        console.print(
            ":cross_mark: Failed to write to the file! Please check the logs in the home directory."
        )


@tasks.command()
@click.argument("id")
@click.argument("name")
@click.argument("date")
@click.argument("priority")
@click.argument("group")
def edit(id: str, name: str, date: str, priority: str, group: str) -> None:
    """Edits an existing task in tasks.json and commits the changes in the git repository.

    :param id: ID of the task.
    :type id: str
    :param name: Name of the task.
    :type name: str
    :param date: Due date for the task.
    :type date: str
    :param priority: Priority for the task.
    :type priority: str
    :param group: Group for the task.
    :type group: str
    :rtype: None
    """

    words = group.split(" ")
    extracted_groups = [word[1:] for word in words if word[0] == "@"]

    try:
        with tasks_path.open("r") as tasks_file:
            tasks_json = load_json(tasks_file)
            if tasks_json == -1:
                sys.exit(-1)
            filtered_tasks = tasks_json

            for task in filtered_tasks:
                if task["id"] == id:
                    if date.strip() != ".":
                        task["due_date"] = str(parse_date(date, task["due_date"]))
                    if name.strip() != ".":
                        task["name"] = name

                    if priority.strip() != ".":
                        task["priority"] = priority

                    if group.strip() != ".":
                        task["group"] = extracted_groups

            with tasks_path.open("w") as tasks_file:
                filtered_tasks = json.dump(filtered_tasks, tasks_file)
                console.print(
                    f":white_check_mark: Task {id} has been modified in the list!"
                )
                repo.index.add([str(tasks_path)])
                repo.index.commit(f"Modified Task {id} in tasks.")
                console.print(
                    f":white_check_mark: Task {id} has been modified in the git repository!"
                )

    except FileNotFoundError as e:
        with tasks_path.open("a") as tasks_file:
            tasks_file.write("[]")
        logger.error(e)
        console.print(
            ":cross_mark: Failed to write to the file! Please check the logs in the home directory."
        )


@tasks.command()
@click.argument("id")
def delete(id: str) -> None:
    """Deletes a task from tasks.json

    :param id: ID of the task.
    :type id: str
    """

    try:
        tasks_json = None
        with tasks_path.open("r") as tasks_file:
            tasks_json = load_json(tasks_file)
            if tasks_json == -1:
                sys.exit(-1)

        filtered_tasks = [task for task in tasks_json if task["id"] != id]

        try:
            with tasks_path.open("w") as tasks_file:
                filtered_tasks = json.dump(filtered_tasks, tasks_file)
                repo.index.add([str(tasks_path)])
                repo.index.commit(f"Deleted Task {id} from tasks.")
                console.print(
                    f":white_check_mark: Task {id} has been removed from the git repository!"
                )
        except FileNotFoundError as e:
            logger.error(e)
            console.print(
                ":cross_mark: Failed to write to the file! Please check the logs in the home directory."
            )

    except FileNotFoundError as e:
        with tasks_path.open("a") as tasks_file:
            tasks_file.write("[]")
        logger.error(e)
        console.print(
            ":cross_mark: Failed to read from the file! Please check the logs in the home directory."
        )


@tasks.command()
def show() -> None:
    """Shows all tasks present in tasks.json"""

    try:
        with tasks_path.open("r") as tasks_file:
            file_content = load_json(tasks_file)
            if file_content == -1:
                sys.exit(-1)
            tasks_utils.parse_tasks(file_content)
    except FileNotFoundError as e:
        with tasks_path.open("a") as tasks_file:
            tasks_file.write("[]")
        logger.error(e)
        console.print(
            ":cross_mark: Failed to read from the file! Please check the logs in the home directory."
        )
        sys.exit(-1)


@tasks.command()
@click.argument("group_name")
def show_group(group_name: str) -> None:
    """Shows all tasks belonging to `group_name`

    :param group_name: Group name to which the task belongs.
    :type group_name: str
    :rtype: None
    """

    try:
        with tasks_path.open("r") as tasks_file:
            file_content = load_json(tasks_file)
            if file_content == -1:
                sys.exit(-1)

            filtered_tasks = []
            for task in file_content:
                for group in task["group"]:
                    if group_name[1:] == group:
                        filtered_tasks.append(task)

            # should return -1 for passing tests
            if filtered_tasks == []:
                sys.exit(-1)

            tasks_utils.parse_tasks(filtered_tasks)

    except FileNotFoundError as e:
        with tasks_path.open("a") as tasks_file:
            tasks_file.write("[]")
        logger.error(e)
        console.print(
            ":cross_mark: Failed to read from the file! Please check the logs in the home directory."
        )
        sys.exit(-1)
