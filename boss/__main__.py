import click
import traceback
from boss.generate import clients_by_BRAS_and_state, total_comsuption_by_state, adsl_clients_by_BRAS_and_state, mdu_clients_by_BRAS_and_state
from common.constant import filename

@click.group()
def cli():
    """MODULE REPORT BOSS

    This module is responsible for generating the total clients consumption data by state (and BRAS). 
    Both for ADSL and MDU equipment.
    """
    pass

@cli.command(help="Create the total ADSL consumption by state (and BRAS)")
@click.option("-fr", "--filereport", help="BOSS report file path", type=click.Path(exists=True))
@click.option("-fc", "--fileconsumption", help="Path of the file with the consumption by BRAS", type=click.Path(exists=True))
@click.option("-p", "--process", help="Allows you to save all files generated in execution", is_flag=True)
def adsl(filereport, fileconsumption, process):
    if filereport and fileconsumption:
        if process: df_porcentage = adsl_clients_by_BRAS_and_state(filereport, process=True)
        else: df_porcentage = adsl_clients_by_BRAS_and_state(filereport)
        total_comsuption_by_state(df_porcentage, fileconsumption, equipment="adsl")

@cli.command(help="Create the total MDU consumption by state (and BRAS)")
@click.option("-fr", "--filereport", help="BOSS report file path", type=click.Path(exists=True))
@click.option("-fc", "--fileconsumption", help="Path of the file with the consumption by BRAS", type=click.Path(exists=True))
@click.option("-p", "--process", help="Allows you to save all files generated in execution", is_flag=True)
def mdu(filereport, fileconsumption, process):
    if filereport and fileconsumption:
        if process: df_porcentage = mdu_clients_by_BRAS_and_state(filereport, process=True)
        else: df_porcentage = mdu_clients_by_BRAS_and_state(filereport)
        total_comsuption_by_state(df_porcentage, fileconsumption, equipment="mdu")

@cli.command(help="Manually create the total number of ADSL and MDU clients by state and BRAS")
@click.option("-fr", "--filereport", help="BOSS report file path", type=click.Path(exists=True))
def clients(filereport):
    if filereport:
        clients_by_BRAS_and_state(filereport)

@cli.command(help="Manually create the ADSL consumption total")
@click.option("-fp", "--fileporcentage", help="Total clients by state and bras file path", type=click.Path(exists=True))
@click.option("-fc", "--fileconsumption", help="Path of the file with the consumption by BRAS", type=click.Path(exists=True))
def adslmanual(fileporcentage, fileconsumption):
    if fileporcentage and fileconsumption:
        total_comsuption_by_state(fileporcentage, fileconsumption, equipment="adsl")

@cli.command(help="Manually create the MDU consumption total")
@click.option("-fp", "--fileporcentage", help="Total clients by state and bras file path", type=click.Path(exists=True))
@click.option("-fc", "--fileconsumption", help="Path of the file with the consumption by BRAS", type=click.Path(exists=True))
def mdumanual(fileporcentage, fileconsumption):
    if fileporcentage and fileconsumption:
        total_comsuption_by_state(fileporcentage, fileconsumption, equipment="mdu")

if __name__ == "__main__":
    try:
        cli()
    except Exception as error:
        # click.echo(error)
        traceback.print_exc()
