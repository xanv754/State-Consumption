import click
import traceback
from boss.generate import global_clients_by_BRAS, total_consumption_by_bras, clients_porcentages_by_bras, total_comsuption_by_state
from common import filename, FileController

@click.group()
def cli():
    """MODULE REPORT BOSS

    This module is responsible for generating the total clients consumption data by state (and BRAS). 
    Both for ADSL and MDU equipment.
    """
    pass

@cli.command(help="Generate the total consumption by state")
@click.option("-fr", "--filereport", help="BOSS report file path", type=click.Path(exists=True))
@click.option("-fc", "--fileconsumption", help="Path of the file with the consumption by BRAS", type=click.Path(exists=True))
@click.option("-p", "--process", help="Allows you to save all files generated in execution", is_flag=True)
def auto(filereport, fileconsumption, process):
    if filereport and fileconsumption:
        if process: clients_porcentages_by_bras(filereport, process=True)
        else: clients_porcentages_by_bras(filereport)
        df_adsl_clients = FileController.read_excel(filename.ADSL_CLIENTS)
        df_mdu_clients = FileController.read_excel(filename.MDU_CLIENTS)
        df_adsl_porcentage = FileController.read_excel(filename.ADSL_PORCENTAGE)
        df_mdu_porcentage = FileController.read_excel(filename.MDU_PORCENTAGE)
        df_consumption = FileController.read_excel(fileconsumption)
        df_adsl_consumption = total_consumption_by_bras(df_adsl_porcentage, df_consumption, "adsl")
        df_mdu_consumption = total_consumption_by_bras(df_mdu_porcentage, df_consumption, "mdu")
        total_comsuption_by_state(df_adsl_clients, df_adsl_consumption, df_mdu_clients, df_mdu_consumption)
        
@cli.command(help="Manually generate the total comsuption by state")
@click.option("-fac", "--fileadslclients", help="ADSL total clients file path", type=click.Path(exists=True))
@click.option("-fap", "--fileadslporcentage", help="ADSL total porcentage file path", type=click.Path(exists=True))
@click.option("-fmc", "--filemduclients", help="MDU total clients file path", type=click.Path(exists=True))
@click.option("-fmp", "--filemduporcentage", help="MDU total porcentage file path", type=click.Path(exists=True))
@click.option("-fc", "--fileconsumption", help="Path of the file with the consumption by BRAS", type=click.Path(exists=True))
def manual(fileadslclients, fileadslporcentage, filemduclients, filemduporcentage, fileconsumption):
    if fileadslclients and fileadslporcentage and filemduclients and filemduporcentage and fileconsumption:
        df_adsl_clients = FileController.read_excel(fileadslclients)
        df_mdu_clients = FileController.read_excel(filemduclients)
        df_adsl_porcentage = FileController.read_excel(fileadslporcentage)
        df_mdu_porcentage = FileController.read_excel(filemduporcentage)
        df_consumption = FileController.read_excel(fileconsumption)
        if not df_adsl_porcentage.empty and not df_mdu_porcentage.empty and not df_consumption.empty:
            df_adsl_consumption = total_consumption_by_bras(df_adsl_porcentage, df_consumption, "adsl")
            df_mdu_consumption = total_consumption_by_bras(df_mdu_porcentage, df_consumption, "mdu")
            total_comsuption_by_state(df_adsl_clients, df_adsl_consumption, df_mdu_clients, df_mdu_consumption)
        else:            
            raise Exception("Data ADSL or MDU not found")

@cli.command(help="Manually generate the total number of clients and porcentages by BRAS. In addition, generate the total comsuption by state.")
@click.option("-fr", "--filereport", help="BOSS report file path", type=click.Path(exists=True))
@click.option("-fc", "--fileconsumption", help="Path of the file with the consumption by BRAS", type=click.Path(exists=True))
def total(filereport, fileconsumption):
    if filereport and fileconsumption:
        global_clients_by_BRAS(filereport)
        df_adsl_clients = FileController.read_excel(filename.ADSL_CLIENTS)
        df_mdu_clients = FileController.read_excel(filename.MDU_CLIENTS)
        df_adsl_porcentage = FileController.read_excel(filename.ADSL_PORCENTAGE)
        df_mdu_porcentage = FileController.read_excel(filename.MDU_PORCENTAGE)
        df_consumption = FileController.read_excel(fileconsumption)
        df_adsl_consumption = total_consumption_by_bras(df_adsl_porcentage, df_consumption, "adsl")
        df_mdu_consumption = total_consumption_by_bras(df_mdu_porcentage, df_consumption, "mdu")
        total_comsuption_by_state(df_adsl_clients, df_adsl_consumption, df_mdu_clients, df_mdu_consumption)

if __name__ == "__main__":
    try:
        cli()
    except Exception as error:
        click.echo(error)
