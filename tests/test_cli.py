import click.testing
import pytest
from click.testing import CliRunner
from absorb.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return click.testing.CliRunner()


def test_app(runner: CliRunner) -> None:
    """The main group should return 0."""
    result = runner.invoke(cli)
    assert result.exit_code == 0
