import nox
import tempfile
from nox.sessions import Session

nox.options.sessions = (
    "lint",
    "safety",
    "typeguard",
    "tests",
)


def install_with_constraints(session: Session, *args, **kwargs) -> None:
    """Install packages constrained by Poetry's lock file."""
    with tempfile.NamedTemporaryFile(delete=False) as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(
            f"--constraint={requirements.name}",
            *args,
            **kwargs,
        )


@nox.session(python=["3.7", "3.8"])
def tests(session: Session) -> None:
    """Run tests."""
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "coverage[toml]", "pytest", "pytest-cov")
    session.run("pytest", *args)


lint_locations = (
    "absorb",
    "tests",
    "noxfile.py",
    "docs/conf.py",
)


@nox.session(python=["3.7", "3.8"])
def black(session: Session) -> None:
    """Run black code format."""
    args = session.posargs or lint_locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python=["3.7", "3.8"])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or lint_locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-black",
        "flake8-bandit",
        "flake8-docstrings",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python=["3.7", "3.8"])
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    with tempfile.NamedTemporaryFile(delete=False) as requirements:
        # converts poetry lock to requirements
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run(
            "safety",
            "check",
            f"--file={requirements.name}",
            "--full-report",
        )


@nox.session(python=["3.7"])
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session,
        "sphinx",
        "faculty-sphinx-theme",
        "sphinx-click",
    )
    session.run("sphinx-build", "docs", "docs/_build")


# mypy currently doesn't work with click decorators
# @nox.session(python=["3.7"])
# def mypy(session: Session) -> None:
#     """Runs mypy session."""
#     args = session.posargs or lint_locations
#     install_with_constraints(session, "mypy")
#     session.run("mypy", *args)


# pytype currently doesn't work with Python 3.7
# @nox.session(python="3.7")
# def pytype(session: Session) -> None:
#     """Runs pytype static type checker."""
#     args = session.posargs or ["--disable=import-error", *lint_locations]
#     install_with_constraints(session, "pytype")
#     session.run("pytype", *args)


package = "absorb"


@nox.session(python=["3.7", "3.8"])
def typeguard(session: Session) -> None:
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}")


@nox.session(python=["3.7"])
def coverage(session: Session) -> None:
    """Upload coverage data."""
    install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
