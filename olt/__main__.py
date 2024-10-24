import click
from olt.generate import clients_by_BRAS_and_state

@click.group()
def cli():
    pass


@cli.command(help="Create the clients report by BRAS and state")
@click.option("-f", "--filename", help="Name of the file to be read", type=click.Path(exists=True))
def clients(filename):
    if filename:
        clients_by_BRAS_and_state(filename)

if __name__ == "__main__":
    try:
        cli()
    except Exception as error:
        click.echo(error)