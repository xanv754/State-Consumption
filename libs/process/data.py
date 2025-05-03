import pandas as pd
from constants.columns import NameColumns, ConsumptionStateColumns
from constants.states import all_states
from libs.process.process import ProcessHandler


class DataHandler:
    """Class to get the data."""

    data: ProcessHandler

    def __init__(self, data: ProcessHandler) -> None:
        self.data = data


    def __merge_by_all_states(self, df_clients: pd.DataFrame, df_consumption: pd.DataFrame) -> pd.DataFrame:
        """Merge the clients and consumption by all states."""
        try:
            df_clients.drop(columns=[NameColumns.BRAS], inplace=True)
            df_merge = pd.merge(df_clients, df_consumption, on=NameColumns.STATE, how='inner')
            df_merge = df_merge.reset_index(drop=True)
            df_all_states = pd.DataFrame({NameColumns.STATE: all_states})
            df = pd.merge(df_all_states, df_merge, on=NameColumns.STATE, how='left')
            df[[NameColumns.TOTAL_CLIENTS, NameColumns.CONSUMPTION]] = df[[NameColumns.TOTAL_CLIENTS, NameColumns.CONSUMPTION]].fillna(0)
            df.sort_values(by=[NameColumns.STATE], inplace=True)
            df = df.reset_index(drop=True)
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df

    def clients_consumption_adsl_by_state(self) -> pd.DataFrame:
        """Get the clients and consumption ADSL by state."""
        try:
            df_total_clients = self.data.total_clients_adsl()
            df_total_consumption = self.data.total_consumption_adsl_by_state()
            df = self.__merge_by_all_states(df_total_clients, df_total_consumption)
            df.rename(columns={
                NameColumns.TOTAL_CLIENTS: ConsumptionStateColumns.TOTAL_CLIENTS_ADSL,
                NameColumns.CONSUMPTION: ConsumptionStateColumns.CONSUMPTION_ADSL
            }, inplace=True)
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df

    def clients_consumption_mdu_by_state(self) -> pd.DataFrame:
        """Get the clients and consumption MDU by state."""
        try:
            df_total_clients = self.data.total_clients_mdu()
            df_total_consumption = self.data.total_consumption_mdu_by_state()
            df = self.__merge_by_all_states(df_total_clients, df_total_consumption)
            df.rename(columns={
                NameColumns.TOTAL_CLIENTS: ConsumptionStateColumns.TOTAL_CLIENTS_MDU,
                NameColumns.CONSUMPTION: ConsumptionStateColumns.CONSUMPTION_MDU
            }, inplace=True)
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df
        
    def clients_consumption_olt_by_state(self) -> pd.DataFrame:
        """Get the clients and consumption OLT by state."""
        try:
            df_total_clients = self.data.total_clients_olt()
            df_total_consumption = self.data.total_consumption_olt_by_state()
            df = self.__merge_by_all_states(df_total_clients, df_total_consumption)
            df.rename(columns={
                NameColumns.TOTAL_CLIENTS: ConsumptionStateColumns.TOTAL_CLIENTS_OLT,
                NameColumns.CONSUMPTION: ConsumptionStateColumns.CONSUMPTION_OLT
            }, inplace=True)
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df
        
    def clients_consumption_by_state(self) -> pd.DataFrame:
        """Get the clients and consumption of ADSL, MDU and OLT by state."""
        try:
            df_adsl = self.clients_consumption_adsl_by_state()
            df_mdu = self.clients_consumption_mdu_by_state()
            df_olt = self.clients_consumption_olt_by_state()
            df_merge = pd.merge(df_adsl, df_mdu, on=NameColumns.STATE, how='inner')
            df_merge = df_merge.reset_index(drop=True)
            df_merge = pd.merge(df_merge, df_olt, on=NameColumns.STATE, how='inner')
            df_merge = df_merge.reset_index(drop=True)
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df_merge