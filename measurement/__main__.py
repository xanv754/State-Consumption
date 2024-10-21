import click
import pandas as pd
from taccess.measurement import MeasurementTaccess
from common.utils.file import File
from common.constant import file as FILE

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
    try:
        click.echo("Getting measurements...")
        Measurement = MeasurementTaccess()
        if not Measurement.err:
            click.echo("Measurements found")
            df = pd.DataFrame(Measurement.bras)
            File.write_excel(df, filename=FILE.MEASUREMENT)
    except Exception as error:
        raise error


@cli.command(help="Get measurements from a external file.")
@click.option("-f", "--file", help="Specifies the file to be used.")
def external(file):
    try:
        if file:
            click.echo("Getting measurements...")
        else:
            click.echo("Filepath is required")
    except Exception as error:
        raise error


if __name__ == "__main__":
    try:
        cli()
    except SystemExit as error:
        if error == 1:
            pass
    except Exception as error:
        click.echo(error)