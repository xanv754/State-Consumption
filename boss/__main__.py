import click
from boss import clients_by_BRAS_and_state

@click.group()
def cli():
    """MODULE BOSS

    This module is in charge of generating new reports from the boss report.
    """
    pass

@cli.command(help="Create the total clients report by state and bras")
def clients():
    clients_by_BRAS_and_state()

if __name__ == "__main__":
    try:
        cli()
    except Exception as error:
        click.echo(error)
