import os
import traceback
import click
import pandas as pd
from typing import List
from tqdm import tqdm
from boss import clients_porcentages_by_bras, total_consumption_by_bras, total_comsuption_by_state 
from measurement import get_consumption_by_taccess, interface as INTERFACE
from common import states as GLOBAL, FileController, filename, colname
from olt import total_by_state

CLIENTS_ADSL_MDU = "Total por Estado"
CLIENTS_OLT = "Clientes"
CONSUMPTION_ADSL_MDU = "Total por Estado"
CONSUMPTION_OLT = "Consumo"
STATE_ADSL_MDU = "Estado"
STATE_OLT = "Estado"

def delete_files() -> None:
    path = os.getcwd()
    if os.path.exists(f"{path}/{filename.ADSL_REPORT_BOSS}"):
        os.remove(f"{path}/{filename.ADSL_REPORT_BOSS}")
    if os.path.exists(f"{path}/{filename.ADSL_CLIENTS}"):
        os.remove(f"{path}/{filename.ADSL_CLIENTS}")
    if os.path.exists(f"{path}/{filename.ADSL_PORCENTAGE}"):
        os.remove(f"{path}/{filename.ADSL_PORCENTAGE}")
    if os.path.exists(f"{path}/{filename.ADSL_CONSUMPTION}"):
        os.remove(f"{path}/{filename.ADSL_CONSUMPTION}")
    if os.path.exists(f"{path}/{filename.MDU_REPORT_BOSS}"):
        os.remove(f"{path}/{filename.MDU_REPORT_BOSS}")
    if os.path.exists(f"{path}/{filename.MDU_CLIENTS}"):
        os.remove(f"{path}/{filename.MDU_CLIENTS}")
    if os.path.exists(f"{path}/{filename.MDU_PORCENTAGE}"):
        os.remove(f"{path}/{filename.MDU_PORCENTAGE}")
    if os.path.exists(f"{path}/{filename.MDU_CONSUMPTION}"):
        os.remove(f"{path}/{filename.MDU_CONSUMPTION}")
    if os.path.exists(f"{path}/{filename.OLT_TOTAL}"):
        os.remove(f"{path}/{filename.OLT_TOTAL}")
    if os.path.exists(f"{path}/{filename.CLIENTS}"):
        os.remove(f"{path}/{filename.CLIENTS}")
    if os.path.exists(f"{path}/{filename.PORCENTAGE}"):
        os.remove(f"{path}/{filename.PORCENTAGE}")

def generate_data(df: pd.DataFrame, df_olt: pd.DataFrame) -> pd.DataFrame:
    """Generate the VPI data."""
    try:
        clients_adsl = []
        consumption_adsl = []
        clients_mdu = []
        consumption_mdu = []
        clients_olt = []
        consumption_olt = []
        for state in tqdm(GLOBAL.states, desc="Generating consumption by state..."):
            state = state.upper()

            df_adsl_clients_filtered = df[df[colname.STATE] == state]
            if not df_adsl_clients_filtered.empty:
                total_adsl_clients = df_adsl_clients_filtered[colname.TOTAL_BY_STATE].iloc[0]
            else: total_adsl_clients = 0
            df_mdu_clients_filtered = df_mdu[df_mdu[colname.STATE] == state]
            if not df_mdu_clients_filtered.empty:
                total_mdu_clients = df_mdu_clients_filtered[colname.TOTAL_BY_STATE].iloc[0]
            else: total_mdu_clients = 0
            df_adsl_comsumption_filtered = df_adsl_consumption[df_adsl_consumption[colname.STATE] == state]
            if not df_adsl_comsumption_filtered.empty:
                total_adsl_comsumption = df_adsl_comsumption_filtered[colname.TOTAL_BY_STATE].iloc[0]
            else: total_adsl_comsumption = 0
            df_mdu_filtered = df_mdu_consumption[df_mdu_consumption[colname.STATE] == state]
            if not df_mdu_filtered.empty:
                total_mdu_consumption = df_mdu_filtered[colname.TOTAL_BY_STATE].iloc[0]
            else: total_mdu_consumption = 0
            clients_adsl.append(total_adsl_clients)
            consumption_adsl.append(total_adsl_comsumption)
            clients_mdu.append(total_mdu_clients)
            consumption_mdu.append(total_mdu_consumption)
        df = pd.DataFrame({
            colname.STATE: GLOBAL.states, 
            colname.CLIENTS_ADSL: clients_adsl, 
            colname.CONSUMPTION_ADSL: consumption_adsl, 
            colname.CLIENTS_MDU: clients_mdu, 
            colname.CONSUMPTION_MDU: consumption_mdu
        })

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
        if process: clients_porcentages_by_bras(filereport, process=True)
        else: clients_porcentages_by_bras(filereport)
        df_adsl_clients = FileController.read_excel(filename.ADSL_CLIENTS)
        df_mdu_clients = FileController.read_excel(filename.MDU_CLIENTS)
        df_adsl_porcentage = FileController.read_excel(filename.ADSL_PORCENTAGE)
        df_mdu_porcentage = FileController.read_excel(filename.MDU_PORCENTAGE)
        if not fileconsumption: 
            if process: df_bras_consumption = get_consumption_by_taccess(process=True)
            else: df_bras_consumption = get_consumption_by_taccess()
            df_adsl_consumption = total_consumption_by_bras(df_adsl_porcentage, df_bras_consumption, equipment="adsl")
            df_mdu_consumption = total_consumption_by_bras(df_mdu_porcentage, df_bras_consumption, equipment="mdu")
        else:
            df_consumption = FileController.read_excel(fileconsumption)
            df_adsl_consumption = total_consumption_by_bras(df_adsl_porcentage, df_consumption, equipment="adsl")
            df_mdu_consumption = total_consumption_by_bras(df_mdu_porcentage, df_consumption, equipment="mdu")
        total_comsuption_by_state(df_adsl_clients, df_adsl_consumption, df_mdu_clients, df_mdu_consumption)
        total_by_state(fileolt)        
        df_olt = FileController.read_excel(filename.OLT_TOTAL)
        if df_olt.empty: raise Exception("OLT data not found")
        df_adsl_mdu = FileController.read_excel(filename.CONSUMPTION)
        if df_adsl_mdu.empty: raise Exception("ADSL and MDU consumption not found")
        df_data = generate_data(df_adsl_mdu, df_olt)
        FileController.write_excel(df_data, filename.VPTI)
        if not process: delete_files()

def manual():
    pass


if __name__ == "__main__":
    try:
        cli()
    except SystemExit as error:
        if error == 1:
            pass
    except Exception as error:
        # click.echo(error)
        traceback.print_exc()