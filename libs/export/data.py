import os
from datetime import datetime
import pandas as pd
from constants.columns import NameColumns, ConsumptionStateColumns
from constants.states import all_states
from libs.export.excel import Excel
from libs.process.data import DataHandler


class DataExport:
    """Class to export the data."""

    @staticmethod
    def consumption_adsl_by_state(data: DataHandler, filepath: str | None = None) -> str | None:
        """Export the consumption ADSL by state.
        
        Returns
        -------
        str
            The path of the file. None if the data was not exported.
        """
        try:
            df_total_clients = data.total_clients_adsl()
            df_total_clients.drop(columns=[NameColumns.BRAS], inplace=True)
            df_total_consumption = data.total_consumption_adsl_by_state()
            df_merge = pd.merge(df_total_clients, df_total_consumption, on=NameColumns.STATE, how='inner')
            df_merge = df_merge.reset_index(drop=True)
            df_states = pd.DataFrame({NameColumns.STATE: all_states})
            df = pd.merge(df_states, df_merge, on=NameColumns.STATE, how='left')
            df[[NameColumns.TOTAL_CLIENTS, NameColumns.CONSUMPTION]] = df[[NameColumns.TOTAL_CLIENTS, NameColumns.CONSUMPTION]].fillna(0)
            df.sort_values(by=[NameColumns.STATE], inplace=True)

            if not filepath:
                home = os.path.expanduser('~')
                if os.path.exists(f"{home}/Descargas"):
                    filepath = f"{home}/Descargas/consumo_adsl_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
                elif os.path.exists(f"{home}/Downloads"):
                    filepath = f"{home}/Downloads/consumo_adsl_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
                else:
                    filepath = f"./consumo_adsl.xlsx"
            excel = Excel(filepath, df)
            if excel.export(): return filepath
            else: return None
        except Exception as error:
            print(error, __file__)
            return None
        
    @staticmethod
    def consumption_mdu_by_state(data: DataHandler, filepath: str | None = None) -> str | None:
        """Export the consumption MDU by state.
        
        Returns
        -------
        str
            The path of the file. None if the data was not exported.
        """
        try:
            df_total_clients = data.total_clients_mdu()
            df_total_clients.drop(columns=[NameColumns.BRAS], inplace=True)
            df_total_consumption = data.total_consumption_mdu_by_state()
            df_merge = pd.merge(df_total_clients, df_total_consumption, on=NameColumns.STATE, how='inner')
            df_merge = df_merge.reset_index(drop=True)
            df_states = pd.DataFrame({NameColumns.STATE: all_states})
            df = pd.merge(df_states, df_merge, on=NameColumns.STATE, how='left')
            df[[NameColumns.TOTAL_CLIENTS, NameColumns.CONSUMPTION]] = df[[NameColumns.TOTAL_CLIENTS, NameColumns.CONSUMPTION]].fillna(0)
            df.sort_values(by=[NameColumns.STATE], inplace=True)

            if not filepath:
                home = os.path.expanduser('~')
                if os.path.exists(f"{home}/Descargas"):
                    filepath = f"{home}/Descargas/consumo_mdu_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
                elif os.path.exists(f"{home}/Downloads"):
                    filepath = f"{home}/Downloads/consumo_mdu_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
                else:
                    filepath = f"./consumo_mdu.xlsx"
            excel = Excel(filepath, df)
            if excel.export(): return filepath
            else: return None
        except Exception as error:
            print(error, __file__)
            return None
        
    @staticmethod
    def consumption_olt_by_state(data: DataHandler, filepath: str | None = None) -> str | None:
        """Export the consumption OLT by state.

        Returns
        -------
        str
            The path of the file. None if the data was not exported.
        """
        try:
            df_total_clients = data.total_clients_olt()
            df_total_clients.drop(columns=[NameColumns.BRAS], inplace=True)
            df_total_consumption = data.total_consumption_olt_by_state()
            df_merge = pd.merge(df_total_clients, df_total_consumption, on=NameColumns.STATE, how='inner')
            df_merge = df_merge.reset_index(drop=True)
            df_states = pd.DataFrame({NameColumns.STATE: all_states})
            df = pd.merge(df_states, df_merge, on=NameColumns.STATE, how='left')
            df[[NameColumns.TOTAL_CLIENTS, NameColumns.CONSUMPTION]] = df[[NameColumns.TOTAL_CLIENTS, NameColumns.CONSUMPTION]].fillna(0)
            df.sort_values(by=[NameColumns.STATE], inplace=True)

            if not filepath:
                home = os.path.expanduser('~')
                if os.path.exists(f"{home}/Descargas"):
                    filepath = f"{home}/Descargas/consumo_olt_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
                elif os.path.exists(f"{home}/Downloads"):
                    filepath = f"{home}/Downloads/consumo_olt_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
                else:
                    filepath = f"./consumo_olt.xlsx"
            excel = Excel(filepath, df)
            if excel.export(): return filepath
            else: return None
        except Exception as error:
            print(error, __file__)
            return None
        
    @staticmethod
    def consumption_by_state(data: DataHandler, filepath: str | None = None) -> str | None:
        """Export the consumption by state.
        
        Returns
        -------
        str
            The path of the file. None if the data was not exported.
        """
        try:
            df_states = pd.DataFrame({NameColumns.STATE: all_states})
            df_total_clients_adsl = data.total_clients_adsl()
            df_total_clients_adsl.drop(columns=[NameColumns.BRAS], inplace=True)
            df_total_consumption_adsl = data.total_consumption_adsl_by_state()
            df_merge_adsl = pd.merge(df_total_clients_adsl, df_total_consumption_adsl, on=NameColumns.STATE, how='inner')
            df_merge_adsl = df_merge_adsl.reset_index(drop=True)
            df_adsl = pd.merge(df_states, df_merge_adsl, on=NameColumns.STATE, how='left')
            df_adsl[[NameColumns.TOTAL_CLIENTS, NameColumns.CONSUMPTION]] = df_adsl[[NameColumns.TOTAL_CLIENTS, NameColumns.CONSUMPTION]].fillna(0)
            df_adsl.sort_values(by=[NameColumns.STATE], inplace=True)
            df_adsl.rename(columns={
                NameColumns.TOTAL_CLIENTS: ConsumptionStateColumns.TOTAL_CLIENTS_ADSL,
                NameColumns.CONSUMPTION: ConsumptionStateColumns.CONSUMPTION_ADSL
            }, inplace=True)

            df_total_clients_mdu = data.total_clients_mdu()
            df_total_clients_mdu.drop(columns=[NameColumns.BRAS], inplace=True)
            df_total_consumption_mdu = data.total_consumption_mdu_by_state()
            df_merge_mdu = pd.merge(df_total_clients_mdu, df_total_consumption_mdu, on=NameColumns.STATE, how='inner')
            df_merge_mdu = df_merge_mdu.reset_index(drop=True)
            df_mdu = pd.merge(df_states, df_merge_mdu, on=NameColumns.STATE, how='left')
            df_mdu[[NameColumns.TOTAL_CLIENTS, NameColumns.CONSUMPTION]] = df_mdu[[NameColumns.TOTAL_CLIENTS, NameColumns.CONSUMPTION]].fillna(0)
            df_mdu.sort_values(by=[NameColumns.STATE], inplace=True)
            df_mdu.rename(columns={
                NameColumns.TOTAL_CLIENTS: ConsumptionStateColumns.TOTAL_CLIENTS_MDU,
                NameColumns.CONSUMPTION: ConsumptionStateColumns.CONSUMPTION_MDU
            }, inplace=True)

            df_total_clients_olt = data.total_clients_olt()
            df_total_clients_olt.drop(columns=[NameColumns.BRAS], inplace=True)
            df_total_consumption_olt = data.total_consumption_olt_by_state()
            df_merge_olt = pd.merge(df_total_clients_olt, df_total_consumption_olt, on=NameColumns.STATE, how='inner')
            df_merge_olt = df_merge_olt.reset_index(drop=True)
            df_olt = pd.merge(df_states, df_merge_olt, on=NameColumns.STATE, how='left')
            df_olt[[NameColumns.TOTAL_CLIENTS, NameColumns.CONSUMPTION]] = df_olt[[NameColumns.TOTAL_CLIENTS, NameColumns.CONSUMPTION]].fillna(0)
            df_olt.sort_values(by=[NameColumns.STATE], inplace=True)
            df_olt.rename(columns={
                NameColumns.TOTAL_CLIENTS: ConsumptionStateColumns.TOTAL_CLIENTS_OLT,
                NameColumns.CONSUMPTION: ConsumptionStateColumns.CONSUMPTION_OLT
            }, inplace=True)

            df_merge = pd.merge(df_adsl, df_mdu, on=NameColumns.STATE, how='inner')
            df_merge = df_merge.reset_index(drop=True)
            df_merge = pd.merge(df_merge, df_olt, on=NameColumns.STATE, how='inner')
            df_merge = df_merge.reset_index(drop=True)  

            if not filepath:
                home = os.path.expanduser('~')
                if os.path.exists(f"{home}/Descargas"):
                    filepath = f"{home}/Descargas/consumo_por_estado_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
                elif os.path.exists(f"{home}/Downloads"):
                    filepath = f"{home}/Downloads/consumo_por_estado_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
                else:
                    filepath = f"./consumo_por_estado.xlsx"
            excel = Excel(filepath, df_merge)
            if excel.export(): return filepath
            else: return None
        except Exception as error:
            print(error, __file__)
            return None