import pandas as pd
import numpy as np
from typing import List
from tqdm import tqdm
from common import colname, add_total_sum_by_col, add_total_sum_by_row
from common import colname, add_total_sum_by_col, add_total_sum_by_row, states as GLOBAL
from boss.lib.clients import ClientController
from boss.lib.report import ReportBossController
from boss.lib.data import save_data_clients, save_data_clients_adsl, save_data_clients_mdu, save_data_porcentage, save_data_porcentage_adsl, save_data_porcentage_mdu, save_data_consumption
from measurement import interface as INTERFACE

def clients_by_BRAS_and_state(filename: str):
    """Generate the file with the total clients by bras and state and the percentages."""
    try:
        ReportBoss = ReportBossController(filename)
        if ReportBoss.validate:
            df_data_total = ClientController.total_bras_by_state(
                ReportBoss.report
            )
            df_data_adsl = ClientController.total_bras_by_state(
                ReportBoss.data_adsl    
            )
            df_data_mdu = ClientController.total_bras_by_state(
                ReportBoss.data_mdu
            )
            if not df_data_total.empty:
                df_data_total = add_total_sum_by_col(df_data_total, name_col=colname.TOTAL_BY_BRAS)
                df_data_total = add_total_sum_by_row(df_data_total, name_row=colname.TOTAL_BY_STATE)
                save_data_clients(df_data_total)
                df_data_adsl = add_total_sum_by_col(df_data_adsl, name_col=colname.TOTAL_BY_BRAS)
                df_data_adsl = add_total_sum_by_row(df_data_adsl, name_row=colname.TOTAL_BY_STATE)
                save_data_clients_adsl(df_data_adsl)
                df_data_mdu = add_total_sum_by_col(df_data_mdu, name_col=colname.TOTAL_BY_BRAS)
                df_data_mdu = add_total_sum_by_row(df_data_mdu, name_row=colname.TOTAL_BY_STATE)
                save_data_clients_mdu(df_data_mdu)
                df_total_porcentage = ClientController.total_porcentage(df_data_total)
                df_total_porcentage = add_total_sum_by_col(df_total_porcentage, name_col=colname.TOTAL_BY_BRAS)
                df_total_porcentage = add_total_sum_by_row(df_total_porcentage, name_row=colname.TOTAL_BY_STATE)
                save_data_porcentage(df_total_porcentage)
                df_adsl_porcentage = ClientController.total_porcentage(df_data_adsl)
                df_adsl_porcentage = add_total_sum_by_col(df_adsl_porcentage, name_col=colname.TOTAL_BY_BRAS)
                df_adsl_porcentage = add_total_sum_by_row(df_adsl_porcentage, name_row=colname.TOTAL_BY_STATE)
                save_data_porcentage_adsl(df_adsl_porcentage)
                df_mdu_porcentage = ClientController.total_porcentage(df_data_mdu)
                df_mdu_porcentage = add_total_sum_by_col(df_mdu_porcentage, name_col=colname.TOTAL_BY_BRAS)
                df_mdu_porcentage = add_total_sum_by_row(df_mdu_porcentage, name_row=colname.TOTAL_BY_STATE)
                save_data_porcentage_mdu(df_mdu_porcentage)
            else:
                raise Exception("Nodes without state exist")
    except Exception as error:
        raise error

def total_clients_by_state(filename: str, process: bool = False) -> pd.DataFrame:
    """Generate the file with the total of clients by state.
    
    Parameters
    ----------
    filename: str
        Filepath of the report boss file to be read.
    """
    try:
        ReportBoss = ReportBossController(filename)
        if ReportBoss.validate:
            df_data_adsl = ClientController.total_bras_by_state(
                ReportBoss.data_adsl    
            )
            df_data_mdu = ClientController.total_bras_by_state(
                ReportBoss.data_mdu
            )
            if not df_data_adsl.empty and not df_data_mdu.empty:
                df_data_adsl = add_total_sum_by_col(df_data_adsl, name_col=colname.TOTAL_BY_BRAS)
                df_data_adsl = add_total_sum_by_row(df_data_adsl, name_row=colname.TOTAL_BY_STATE)
                save_data_clients_adsl(df_data_adsl)
                df_data_mdu = add_total_sum_by_col(df_data_mdu, name_col=colname.TOTAL_BY_BRAS)
                df_data_mdu = add_total_sum_by_row(df_data_mdu, name_row=colname.TOTAL_BY_STATE)
                save_data_clients_mdu(df_data_mdu)
                df_adsl_porcentage = ClientController.total_porcentage(df_data_adsl, df_data_mdu)
                df_adsl_porcentage = add_total_sum_by_col(df_adsl_porcentage, name_col=colname.TOTAL_BY_BRAS)
                df_adsl_porcentage = add_total_sum_by_row(df_adsl_porcentage, name_row=colname.TOTAL_BY_STATE)
                save_data_porcentage_adsl(df_adsl_porcentage)
                df_mdu_porcentage = ClientController.total_porcentage(df_data_mdu, df_data_adsl)
                df_mdu_porcentage = add_total_sum_by_col(df_mdu_porcentage, name_col=colname.TOTAL_BY_BRAS)
                df_mdu_porcentage = add_total_sum_by_row(df_mdu_porcentage, name_row=colname.TOTAL_BY_STATE)
                save_data_porcentage_mdu(df_mdu_porcentage)
            else:
                raise Exception("Nodes without state exist")
    except Exception as error:
        raise error

def total_porcentages_by_state(df: pd.DataFrame, df_consumption: pd.DataFrame, equipment: str) -> pd.DataFrame:
    """Generate the file with the total consumption by state.
    
    Parameters
    ----------  
    """
    try:
        df = df.drop(colname.TOTAL_BY_STATE, axis=1)
        df = df.drop(len(df) - 1, axis=0) 
        df_total_consumption = pd.DataFrame()
        df_total_consumption[colname.STATE] = df[colname.STATE]
        bras = df.columns.to_list()
        bras.pop(0)
        bras.pop(-1)
        states = df[colname.STATE].to_list()
        states.pop(-1)
        for bras_name in tqdm(bras, desc=f"Generating consumption by state {equipment}..."):
            values = []
            if bras_name.upper() in df_consumption[colname.BRAS].to_list():
                total_comsuption = df_consumption[df_consumption[colname.BRAS] == bras_name.upper()][INTERFACE.IN].iloc[0]
            else: total_comsuption = 0
            for i in range(0, len(df[bras_name])):
                porcentage = (df[bras_name][i] * total_comsuption) / 100
                values.append(round(porcentage, 2))
            df_total_consumption[bras_name] = values
        df_total_consumption = add_total_sum_by_col(df_total_consumption, name_col=colname.TOTAL_BY_BRAS)
        df_total_consumption = add_total_sum_by_row(df_total_consumption, name_row=colname.TOTAL_BY_STATE)
        return df_total_consumption
    except Exception as error:
        raise error

def total_comsuption_by_state(df_adsl_clients: pd.DataFrame, df_adsl_consumption: pd.DataFrame, df_mdu: pd.DataFrame, df_mdu_consumption: pd.DataFrame) -> None:
    """Generate the file with the total consumption by state.
    
    Parameters
    ----------  
    """
    try:
        clients_adsl = []
        consumption_adsl = []
        clients_mdu = []
        consumption_mdu = []
        for state in tqdm(GLOBAL.states, desc="Generating consumption by state..."):
            state = state.upper()
            df_adsl_clients_filtered = df_adsl_clients[df_adsl_clients[colname.STATE] == state]
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
        save_data_consumption(df)
    except Exception as error:
        raise error