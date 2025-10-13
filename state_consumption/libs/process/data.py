import pandas as pd
from state_consumption.constants import NameColumns, ConsumptionStateColumns, all_states
from state_consumption.libs.process.process import ProcessData


class ReportHandler:
    """Class to get report of the data."""
    data: ProcessData

    def __init__(self, data: ProcessData) -> None:
        self.data = data

    def _merge_consumption_by_all_states(self, df_clients: pd.DataFrame, df_consumption: pd.DataFrame) -> pd.DataFrame:
        """Merge the data comsuption and clients (without percentage) by all states."""
        try:
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
        
    def _merge_percentage_by_all_states(self, df_data: pd.DataFrame, df_percentage: pd.DataFrame) -> pd.DataFrame:
        """Merge the data percentage and data (without percentage) by all states."""
        try:
            df_merge = pd.merge(df_data, df_percentage, on=NameColumns.STATE, how='left')
            df_merge = df_merge.reset_index(drop=True)
            df_merge[[NameColumns.PERCENTAGE_CONSUMPTION]] = df_merge[[NameColumns.PERCENTAGE_CONSUMPTION]].fillna(0)
            df_merge.sort_values(by=[NameColumns.STATE], inplace=True)
            df_merge = df_merge.reset_index(drop=True)
        except Exception as error:
            print(error, __file__)
            exit(1)
        else: 
            return df_merge

    def clients_consumption_adsl_by_state(self) -> pd.DataFrame:
        """Get the clients and consumption ADSL by state."""
        try:
            df_total_clients = self.data.total_clients_adsl_by_state()
            df_total_consumption = self.data.total_consumption_adsl_by_state()
            df = self._merge_consumption_by_all_states(df_total_clients, df_total_consumption)
            df.rename(columns={
                NameColumns.TOTAL_CLIENTS: ConsumptionStateColumns.TOTAL_CLIENTS_ADSL,
                NameColumns.CONSUMPTION: ConsumptionStateColumns.CONSUMPTION_ADSL
            }, inplace=True)
            self.data.export_missing_bras()
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df

    def clients_consumption_mdu_by_state(self) -> pd.DataFrame:
        """Get the clients and consumption MDU by state."""
        try:
            df_total_clients = self.data.total_clients_mdu_by_state()
            df_total_consumption = self.data.total_consumption_mdu_by_state()
            df = self._merge_consumption_by_all_states(df_total_clients, df_total_consumption)
            df.rename(columns={
                NameColumns.TOTAL_CLIENTS: ConsumptionStateColumns.TOTAL_CLIENTS_MDU,
                NameColumns.CONSUMPTION: ConsumptionStateColumns.CONSUMPTION_MDU
            }, inplace=True)
            self.data.export_missing_bras()
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df
        
    def clients_consumption_olt_by_state(self) -> pd.DataFrame:
        """Get the clients and consumption OLT by state."""
        try:
            df_total_clients = self.data.total_clients_olt_by_state()
            df_total_consumption = self.data.total_consumption_olt_by_state()
            df = self._merge_consumption_by_all_states(df_total_clients, df_total_consumption)
            df.rename(columns={
                NameColumns.TOTAL_CLIENTS: ConsumptionStateColumns.TOTAL_CLIENTS_OLT,
                NameColumns.CONSUMPTION: ConsumptionStateColumns.CONSUMPTION_OLT
            }, inplace=True)
            self.data.export_missing_bras()
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
        
    def clients_consumption_adsl_by_state_with_percentage(self) -> pd.DataFrame:
        """Get the clients and consumption ADSL by state with percentage."""
        try:
            df_adsl = self.clients_consumption_adsl_by_state()
            df_percentage = self.data.percentage_consumption_adsl_by_state()
            df_merge = self._merge_percentage_by_all_states(df_adsl, df_percentage)
            df_merge.rename(columns={
                NameColumns.PERCENTAGE_CONSUMPTION: ConsumptionStateColumns.PERCENTAGE_CONSUMPTION_ADSL
            }, inplace=True)
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df_merge
        
    def clients_consumption_mdu_by_state_with_percentage(self) -> pd.DataFrame:
        """Get the clients and consumption MDU by state with percentage."""
        try:
            df_mdu = self.clients_consumption_mdu_by_state()
            df_percentage = self.data.percentage_consumption_mdu_by_state()
            df_merge = self._merge_percentage_by_all_states(df_mdu, df_percentage)
            df_merge.rename(columns={
                NameColumns.PERCENTAGE_CONSUMPTION: ConsumptionStateColumns.PERCENTAGE_CONSUMPTION_MDU
            }, inplace=True)
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df_merge
        
    def clients_consumption_olt_by_state_with_percentage(self) -> pd.DataFrame:
        """Get the clients and consumption OLT by state with percentage."""
        try:
            df_olt = self.clients_consumption_olt_by_state()
            df_percentage = self.data.percentage_consumption_olt_by_state()
            df_merge = self._merge_percentage_by_all_states(df_olt, df_percentage)
            df_merge.rename(columns={
                NameColumns.PERCENTAGE_CONSUMPTION: ConsumptionStateColumns.PERCENTAGE_CONSUMPTION_OLT
            }, inplace=True)
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df_merge
        
    def clients_consumption_by_state_with_percentage(self) -> pd.DataFrame:
        """Get the clients and consumption by state with percentage."""
        try:
            df_adsl = self.clients_consumption_adsl_by_state_with_percentage()
            df_mdu = self.clients_consumption_mdu_by_state_with_percentage()
            df_olt = self.clients_consumption_olt_by_state_with_percentage()
            df_merge = pd.merge(df_adsl, df_mdu, on=NameColumns.STATE, how='inner')
            df_merge = df_merge.reset_index(drop=True)
            df_merge = pd.merge(df_merge, df_olt, on=NameColumns.STATE, how='inner')
            df_merge = df_merge.reset_index(drop=True)
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df_merge