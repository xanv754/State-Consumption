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
@click.option("-p", "--process", help="Allows you to save all files generated in execution", is_flag=True)
def external(file, sheetname, process):
    if file and sheetname and process:
        get_consumption_by_file(file, sheetname=sheetname, process=process)
    elif file and sheetname:
        get_consumption_by_file(file, sheetname=sheetname)
    elif file:
        get_consumption_by_file(file)

if __name__ == "__main__":
    try:
        cli()
    except SystemExit as error:
        if error == 1:
            pass
    except Exception as error:
        click.echo(error)