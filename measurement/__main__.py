import click
from measurement.generate import get_consumption_by_taccess

@click.group()
def cli():
    """MODULE DATABASE

    This module is used to get measurements from Taccess API or a external file.

    \b
    external -f [FILEPATH]   Get measurements from a external filepath.
    """
    pass


@cli.command(help="Get measurements from Taccess API.")
def taccess():
    get_consumption_by_taccess(process=True)

if __name__ == "__main__":
    try:
        cli()
    except SystemExit as error:
        if error == 1:
            pass
    except Exception as error:
        click.echo(error)