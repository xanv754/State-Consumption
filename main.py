import click
import pandas as pd
from typing import List
from tqdm import tqdm
from boss import adsl_clients_by_BRAS_and_state, mdu_clients_by_BRAS_and_state, total_comsuption_by_state
from measurement import get_consumption_by_taccess, interface as INTERFACE
from common import states as GLOBAL, FileController, filename
from olt import total_by_state

CLIENTS_ADSL_MDU = "Total por Estado"
CLIENTS_OLT = "Clientes"
CONSUMPTION_ADSL_MDU = "Total por Estado"
CONSUMPTION_OLT = "Consumo"
STATE_ADSL_MDU = "Estado"
STATE_OLT = "Estado"

def generate_data(df_adsl_clients: pd.DataFrame, 
                  df_adsl_consumption: pd.DataFrame,
                  df_mdu_clients: pd.DataFrame, 
                  df_mdu_consumption: pd.DataFrame, 
                  df_olt: pd.DataFrame) -> pd.DataFrame:
    """Generate the VPI data."""
    try:
        print(df_adsl_clients, df_adsl_consumption, df_mdu_clients, df_mdu_consumption, df_olt)
    except Exception as error:
        raise error
    

@click.group()
def cli():
    """CONSUMPTION OF CLIENTS BY BRAS AND STATE

    This scripts is responsible for generating the total clients consumption data by state. 
    """
    pass

@cli.command(help="Generate the total clients consumption by state")
@click.option("-fr", "--filereport", help="BOSS report file path by ADSL and MDU equipment", type=click.Path(exists=True))
@click.option("-fo", "--fileolt", help="OLT report file path by OLT equipment", type=click.Path(exists=True))
@click.option("-fc", "--fileconsumption", help="Consumption file path by ADSL and MDU equipment", type=click.Path(exists=True))
@click.option("-p", "--process", help="Allows you to save all files generated in execution", is_flag=True)
def auto(filereport, fileolt, fileconsumption, process):
    """Generate the total clients consumption by state."""
    if filereport and fileolt:
        df_porcentage_adsl = adsl_clients_by_BRAS_and_state(filereport)
        df_porcentage_mdu = mdu_clients_by_BRAS_and_state(filereport)
        if not fileconsumption: 
            if process: df_bras_consumption = get_consumption_by_taccess(process=True)
            else: df_bras_consumption = get_consumption_by_taccess()
            total_comsuption_by_state(df_porcentage_adsl, df_bras_consumption, equipment="adsl")
            total_comsuption_by_state(df_porcentage_mdu, df_bras_consumption, equipment="mdu")
        else:
            total_comsuption_by_state(df_porcentage_adsl, fileconsumption, equipment="adsl")
            total_comsuption_by_state(df_porcentage_mdu, fileconsumption, equipment="mdu")
        total_by_state(fileolt)
        df_adsl_clients = FileController.read_excel(filename.ADSL_CLIENTS)
        if df_adsl_clients.empty: raise Exception("ADSL clients not found")
        df_adsl_consumption = FileController.read_excel(filename.ADSL_CONSUMPTION)
        if df_adsl_consumption.empty: raise Exception("ADSL consumption not found")
        df_mdu_clients = FileController.read_excel(filename.MDU_CLIENTS)
        if df_mdu_clients.empty: raise Exception("MDU clients not found")
        df_mdu_consumption = FileController.read_excel(filename.MDU_CONSUMPTION)
        if df_mdu_consumption.empty: raise Exception("MDU consumption not found")
        df_olt = FileController.read_excel(filename.OLT_TOTAL)
        if df_olt.empty: raise Exception("OLT data not found")
        generate_data(df_adsl_clients, df_adsl_consumption, df_mdu_clients, df_mdu_consumption, df_olt)

def manual():
    pass


if __name__ == "__main__":
    try:
        cli()
    except SystemExit as error:
        if error == 1:
            pass
    except Exception as error:
        click.echo(error)