import re

import click


@click.command()
@click.argument(
    "files",
    type=str,
    nargs=-1,
)
@click.option(
    "--verbose",
    "-v",
    default=False,
    is_flag=True,
    help="Show file creation notice and error messages.",
)
def cli(files: tuple[str, ...] = (), verbose: bool = False) -> None:
    """Create an empty file(s) with the specified name(s)."""
    for filename in files:
        try:
            if not is_valid_filename(filename):
                if verbose:
                    click.echo(f"Error: '{filename}' is not a valid filename.")
                continue

            with open(filename, "x") as fp:
                fp.write("")

            if verbose:
                click.echo(f"Created file: {filename}")
        except FileExistsError:
            if verbose:
                click.echo(f"Error: File '{filename}' already exists.")
        except Exception as e:
            if verbose:
                click.echo(f"Error: {e}")


def is_valid_filename(filename: str) -> bool:
    """Check if the filename contains any invalid characters or is a reserved name

    Args:
        filename (str): The filename to validate

    Returns:
        bool: True if valid, False otherwise
    """
    invalid_chars_pattern = r'[<>:"/\\|?*]'

    reserved_filenames = {
        ".",
        "..",
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }
    if re.search(invalid_chars_pattern, filename) or filename in reserved_filenames:
        return False

    return True


if __name__ == "__main__":
    cli()
