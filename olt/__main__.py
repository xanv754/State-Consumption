import click
from olt.generate import total_by_state

@click.group()
def cli():
    """MODULE OLT

    This module is responsible for generating the total clients consumption data by state
    for OLT equipment.
    """
    pass


@cli.command(help="Create the total OLT consumption by state")
@click.option("-fr", "--filereport", help="OLT report file path", type=click.Path(exists=True))
def total(filereport):
    if filereport:
        total_by_state(filereport)

if __name__ == "__main__":
    try:
        cli()
    except Exception as error:
        click.echo(error)