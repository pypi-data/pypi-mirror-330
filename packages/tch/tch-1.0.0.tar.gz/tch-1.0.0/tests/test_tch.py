import pytest
from click.testing import CliRunner

from tch.tch import cli


def test_cli_help() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage: cli [OPTIONS]" in result.output


@pytest.mark.parametrize(
    "files, expectation",
    [
        ("test.txt", "already exists"),
        ("snap.tmp config.py test.txt", "already exists"),
        ("test.txt test.txt test.txt", "already exists"),
    ],
)
def test_duplicate_file(files: str, expectation: str) -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.txt", "w") as f:
            f.write("")

        result = runner.invoke(cli, f"--verbose {files}")
        assert result.exit_code == 0
        assert expectation in result.output


@pytest.mark.parametrize(
    "files, expectation",
    [
        (".", "not a valid filename"),
        ("test.txt .. config.tmp", "not a valid filename"),
        ("fun.zone snap.tml COM9", "not a valid filename"),
        ("/", "not a valid filename"),
        ("fun.zone snap.tml * *", "not a valid filename"),
        ("| | || fun.zone snap.tml", "not a valid filename"),
    ],
)
def test_invalid_filename(files: str, expectation: str) -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, f"--verbose {files}")
        assert result.exit_code == 0
        assert expectation in result.output


@pytest.mark.parametrize(
    "files, option, expectation",
    [
        ("test.tmp", "", ""),
        ("test.tmp fun.zone config.py", "", ""),
        ("valid.txt", "--verbose", "Created file"),
        ("test.txt sample.tml", "--verbose", "Created file"),
    ],
)
def test_cli_options(files: str, option: str, expectation: str) -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, f"{option} {files}")
        assert result.exit_code == 0
        assert expectation in result.output
