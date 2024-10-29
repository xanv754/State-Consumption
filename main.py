import os
import traceback
import click
import pandas as pd
from typing import List
from tqdm import tqdm
from boss import adsl_clients_by_BRAS_and_state, mdu_clients_by_BRAS_and_state, total_porcentages_by_state
from measurement import get_consumption_by_taccess, interface as INTERFACE
from common import states as GLOBAL, FileController, filename
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

def generate_data(df_adsl_clients: pd.DataFrame, 
                  df_adsl_consumption: pd.DataFrame,
                  df_mdu_clients: pd.DataFrame, 
                  df_mdu_consumption: pd.DataFrame, 
                  df_olt: pd.DataFrame) -> pd.DataFrame:
    """Generate the VPI data."""
    try:
        states = []
        adsl_clients = []
        adsl_consumption = []
        mdu_clients = []
        mdu_consumption = []
        olt_clients = []
        olt_consumption = []
        for state in tqdm(GLOBAL.states, desc="Generating data by state..."):
            df_adsl_filtered = df_adsl_clients[df_adsl_clients[STATE_ADSL_MDU] == state.upper()]
            df_adsl_consumption_filtered = df_adsl_consumption[df_adsl_consumption[STATE_ADSL_MDU] == state.upper()]
            df_mdu_filtered = df_mdu_clients[df_mdu_clients[STATE_ADSL_MDU] == state.upper()]
            df_mdu_consumption_filtered = df_mdu_consumption[df_mdu_consumption[STATE_ADSL_MDU] == state.upper()]
            df_olt_filtered = df_olt[df_olt[STATE_OLT] == state.upper()]
            df_olt_consumption_filtered = df_olt[df_olt[STATE_OLT] == state.upper()]

            if not df_adsl_filtered.empty: adsl_clients.append(df_adsl_filtered[CLIENTS_ADSL_MDU].iloc[0])
            else: adsl_clients.append(0)
            if not df_adsl_consumption_filtered.empty: adsl_consumption.append(df_adsl_consumption_filtered[CONSUMPTION_ADSL_MDU].iloc[0])
            else: adsl_consumption.append(0)
            if not df_mdu_filtered.empty: mdu_clients.append(df_mdu_filtered[CLIENTS_ADSL_MDU].iloc[0])
            else: mdu_clients.append(0)
            if not df_mdu_consumption_filtered.empty: mdu_consumption.append(df_mdu_consumption_filtered[CONSUMPTION_ADSL_MDU].iloc[0])
            else: mdu_consumption.append(0)
            if not df_olt_filtered.empty: olt_clients.append(df_olt_filtered[CLIENTS_OLT].iloc[0])
            else: olt_clients.append(0)
            if not df_olt_consumption_filtered.empty: olt_consumption.append(df_olt_consumption_filtered[CONSUMPTION_OLT].iloc[0])
            else: olt_consumption.append(0)
            states.append(state)
        return pd.DataFrame({
            "Estado": states, 
            "Clientes ADSL": adsl_clients, 
            "Consumo ADSL": adsl_consumption, 
            "Clientes MDU": mdu_clients,
            "Consumo MDU": mdu_consumption,
            "Clientes OLT": olt_clients,
            "Consumo OLT": olt_consumption
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
        df_porcentage_adsl = adsl_clients_by_BRAS_and_state(filereport)
        df_porcentage_mdu = mdu_clients_by_BRAS_and_state(filereport)
        if not fileconsumption: 
            if process: df_bras_consumption = get_consumption_by_taccess(process=True)
            else: df_bras_consumption = get_consumption_by_taccess()
            total_porcentages_by_state(df_porcentage_adsl, df_bras_consumption, equipment="adsl")
            total_porcentages_by_state(df_porcentage_mdu, df_bras_consumption, equipment="mdu")
        else:
            total_porcentages_by_state(df_porcentage_adsl, fileconsumption, equipment="adsl")
            total_porcentages_by_state(df_porcentage_mdu, fileconsumption, equipment="mdu")
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
        df_data = generate_data(df_adsl_clients, df_adsl_consumption, df_mdu_clients, df_mdu_consumption, df_olt)
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