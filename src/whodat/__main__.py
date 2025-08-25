"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """Whodat."""


if __name__ == "__main__":
    main(prog_name="whodat")  # pragma: no cover
