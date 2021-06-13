from absorb.core.tasks import commands as tasks_group
from absorb.core.kanban import commands as kanban_group
from absorb.core.idea import commands as idea_group

from pkg_resources import iter_entry_points

import click
from click_plugins import with_plugins


@with_plugins(iter_entry_points("absorb.plugins"))
@click.group()
def cli() -> None:
    """Creates the main click group for absorb."""
    pass


cli.add_command(tasks_group.tasks)
cli.add_command(kanban_group.kanban)
cli.add_command(idea_group.idea)

if __name__ == "__main__":
    cli()
