import pandas as pd
from typing import List
from tqdm import tqdm
from common import colname, add_total_sum_by_col, add_total_sum_by_row
from common import filename, FileController, colname, add_total_sum_by_col, add_total_sum_by_row, states as GLOBAL
from boss.lib.clients import ClientController
from boss.lib.report import ReportBossController
from boss.lib.data import save_data_clients, save_data_clients_adsl, save_data_clients_mdu, save_data_porcentage, save_data_porcentage_adsl, save_data_porcentage_mdu
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
    
def adsl_clients_by_BRAS_and_state(filename: str, process: bool = False) -> pd.DataFrame:
    """Generate the file with the total of ADSL clients by bras and state and the percentages.
    
    Parameters
    ----------
    filename: str
        Filepath of the report boss file to be read.
    """
    try:
        ReportBoss = ReportBossController(filename, process=process, equipment="adsl")
        if ReportBoss.validate:
            df_data_adsl = ClientController.total_bras_by_state(
                ReportBoss.data_adsl    
            )
            if not df_data_adsl.empty:
                df_data_adsl = add_total_sum_by_col(df_data_adsl, name_col=colname.TOTAL_BY_BRAS)
                df_data_adsl = add_total_sum_by_row(df_data_adsl, name_row=colname.TOTAL_BY_STATE)
                save_data_clients_adsl(df_data_adsl)
                df_adsl_porcentage = ClientController.total_porcentage(df_data_adsl)
                df_adsl_porcentage = add_total_sum_by_col(df_adsl_porcentage, name_col=colname.TOTAL_BY_BRAS)
                df_adsl_porcentage = add_total_sum_by_row(df_adsl_porcentage, name_row=colname.TOTAL_BY_STATE)
                if process: save_data_porcentage_adsl(df_adsl_porcentage)
                return df_adsl_porcentage
            else:
                raise Exception("Nodes without state exist")
    except Exception as error:
        raise error
    
def mdu_clients_by_BRAS_and_state(filename: str, process: bool = False) -> pd.DataFrame:
    """Generate the file with the total of MDU clients by bras and state and the percentages.
    
    Parameters
    ----------
    filename: str
        Filepath of the report boss file to be read.
    """
    try:
        ReportBoss = ReportBossController(filename, process=process, equipment="mdu")
        if ReportBoss.validate:
            df_data_mdu = ClientController.total_bras_by_state(
                ReportBoss.data_mdu
            )
            if not df_data_mdu.empty:
                df_data_mdu = add_total_sum_by_col(df_data_mdu, name_col=colname.TOTAL_BY_BRAS)
                df_data_mdu = add_total_sum_by_row(df_data_mdu, name_row=colname.TOTAL_BY_STATE)
                save_data_clients_mdu(df_data_mdu)
                df_mdu_porcentage = ClientController.total_porcentage(df_data_mdu)
                df_mdu_porcentage = add_total_sum_by_col(df_mdu_porcentage, name_col=colname.TOTAL_BY_BRAS)
                df_mdu_porcentage = add_total_sum_by_row(df_mdu_porcentage, name_row=colname.TOTAL_BY_STATE)
                if process: save_data_porcentage_mdu(df_mdu_porcentage)
                return df_mdu_porcentage
            else:
                raise Exception("Nodes without state exist")
    except Exception as error:
        raise error

def total_comsuption_by_state(porcentage: str | pd.DataFrame, measurement: str | pd.DataFrame, equipment: str) -> None:
    """Generate the file with the total consumption by state.
    
    Parameters
    ----------
    porcentage: str | DataFrame
        Filepath or DataFrame of porcentage by ADSL or MDU file.
    measurement: str | DataFrame
        Filepath or DataFrame of consumption by BRAS file.
    type: str, default adsl
        Type of equipment to be used (ADSL o MDU).
    """
    try:
        if type(porcentage) == str: df_porcentage = FileController.read_excel(porcentage)
        else: df_porcentage = porcentage
        if type(measurement) == str: df_measurement = FileController.read_excel(measurement)
        else: df_measurement = measurement
        df_porcentage = df_porcentage.drop(df_porcentage.index[-1])
        df = pd.DataFrame({colname.STATE: df_porcentage[colname.STATE]})
        if not df_porcentage.empty and not df_measurement.empty:
            for _index, row in tqdm(df_measurement.iterrows(), total=df_measurement.shape[0], desc="Calculating total comsumption by state..."):
                current_bras = str(row[colname.BRAS]).lower()
                if current_bras in df_porcentage.columns.to_list():
                    total = row[INTERFACE.IN]
                    porcentage = df_porcentage[current_bras]
                    new_values: List[float] = []
                    for value in porcentage:
                        new_porcentage = value * total
                        new_values.append(round(new_porcentage, 2))
                    df[current_bras] = new_values
        df = add_total_sum_by_col(df, colname.TOTAL_BY_BRAS)
        df = add_total_sum_by_row(df, colname.TOTAL_BY_STATE)
        total_porcentage = df[colname.TOTAL_BY_STATE]
        total = total_porcentage[len(total_porcentage) - 1]
        total_porcentage = total_porcentage[:-1]
        new_values: List[float] = []
        for value in tqdm(total_porcentage, desc="Adding total comsumptions..."):
            new_values.append(round((value / total * 100), 2))
        new_values.append(sum(new_values))
        df[colname.TOTAL_BY_USAGE] = new_values
        if equipment == "adsl":
            FileController.write_excel(df, filename=filename.ADSL_CONSUMPTION)
        elif equipment == "mdu":
            FileController.write_excel(df, filename=filename.MDU_CONSUMPTION)
    except Exception as error:
        raise error