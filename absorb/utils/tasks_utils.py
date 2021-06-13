from typing import Any
from rich.table import Table
from rich.console import Console
from datetime import datetime, timedelta
from collections import namedtuple

console = Console()


def convert_timedelta(duration: timedelta) -> namedtuple:
    """Converts a timedelta object into the custom ExtractedDate namedtuple.

    :param duration: Timedelta object for date.
    :type duration: timedelta
    :return: ExtractedDate namedtuple.
    :rtype: namedtuple
    """

    date_tuple = namedtuple("ExtractedDate", ["days", "hours", "minutes", "seconds"])
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return date_tuple(days, hours, minutes, seconds)


def parse_tasks(file_content: Any) -> None:
    """Prints the tasks table.

    :param file_content: File content containing tasks.
    :type file_content: Any
    :rtype: None
    """

    tasks_table = Table(show_header=True, header_style="bold")
    tasks_table.add_column("Task ID")
    tasks_table.add_column("Task Name")
    tasks_table.add_column("Date Added")
    tasks_table.add_column("Due Date")
    tasks_table.add_column("Priority")
    tasks_table.add_column("Group")

    for task in file_content:
        task_entry = task

        task_date = datetime.strptime(task_entry["date"], "%Y-%m-%d %H:%M:%S.%f")

        task_due_date = datetime.strptime(
            task_entry["due_date"], "%Y-%m-%d %H:%M:%S.%f"
        )
        curr_date = datetime.now()

        diff = task_due_date - curr_date
        diff_date = convert_timedelta(diff)

        due_display = ""
        if (diff_date.days == 0) and (diff_date.hours < 24):
            due_display = "Due today."
        elif diff_date.days < 0:
            due_display = str(abs(diff_date.days)) + " days overdue."
        elif diff_date.days > 0:
            due_display = str(diff_date.days) + " days to due date."

        due_date = (
            datetime.strftime(task_due_date, "%b %d, %Y at %I:%M%p")
            + f"\n({due_display})"
        )

        if task_entry["group"] == "":
            tasks_table.add_row(
                task_entry["id"],
                task_entry["name"],
                datetime.strftime(task_date, "%b %d, %Y at %I:%M%p"),
                due_date,
                task_entry["priority"],
            )
        else:
            tags = task_entry["group"]
            tasks_table.add_row(
                task_entry["id"],
                task_entry["name"],
                datetime.strftime(task_date, "%b %d, %Y at %I:%M%p"),
                due_date,
                task_entry["priority"],
                f"[bold yellow]tags: {tags}[/bold yellow]",
            )

    console.print(tasks_table)
