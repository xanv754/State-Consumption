import click
from measurement.generate import get_consumption_by_taccess, get_consumption_by_file
@click.group()
def cli():
    """MODULE DATABASE

    This module is used to get measurements from Taccess API or a external file.
    """
    pass


@cli.command(help="Get consumption from Taccess API.")
def taccess():
    get_consumption_by_taccess(process=True)

@cli.command(help="Get consumption from external file.")
@click.option("-f", "--file", type=click.Path(exists=True), help="File to be read.")
@click.option("-s", "--sheetname", default="" , help="Specify sheetname of file to be read")
def external(file, sheetname):
    if file and sheetname:
        get_consumption_by_file(file, sheetname=sheetname, process=True)
    elif file:
        get_consumption_by_file(file, process=True)

if __name__ == "__main__":
    try:
        cli()
    except SystemExit as error:
        if error == 1:
            pass
    except Exception as error:
        click.echo(error)