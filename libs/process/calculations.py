import pandas as pd
from constants.path import PathStderr
from constants.columns import NameColumns
from utils.excel import Excel
from utils.console import terminal


class Calculate:
    """Class to calculate the data."""
    __exported: bool = False
    missing_bras: pd.DataFrame = pd.DataFrame({NameColumns.BRAS: []})

    def __add_missing_bras(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add the missing bras to the data."""
        df = pd.concat([self.missing_bras, df], axis=0)
        self.missing_bras = df

    def export_missing_bras(self) -> None:
        """Export the missing bras to a .xlsx file."""
        if not self.missing_bras.empty:
            df = self.missing_bras.drop_duplicates()
            excel = Excel(PathStderr.MISSING_CONSUMPTION)
            excel.export(data=df, sheet_name=NameColumns.BRAS)
            if self.__exported: return
            self.__exported = True
            terminal.print(f"Some Bras are missing the consumption. Bras name saved in {PathStderr.MISSING_CONSUMPTION}!")
    
    def total_clients_adsl_mdu(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate the total of clients group by state and their bras in ADSL or MDU.
        
        Parameters
        ----------
        data : pd.DataFrame
            Dataframe with the data to calcute. This data must have the following columns: Bras, State and Total Clients.
        """
        try:
            df = data.copy()
            df = df.groupby([NameColumns.BRAS, NameColumns.STATE]).sum()
            df[NameColumns.TOTAL_CLIENTS] = df[NameColumns.TOTAL_CLIENTS].round(2)
            df = df.reset_index()
            return df
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}, Method: total_clients_adsl_mdu\n {error}")
            exit(1)
    
    
    def total_clients_olt(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate the total of clients group by state and their bras in OLT.
        
        Parameters
        ----------
        data : pd.DataFrame
            Dataframe with the data to calcute. This data must have the following columns: Bras, State and Total Clients.
        """
        try:
            df = data.copy()
            df = df.groupby([NameColumns.BRAS, NameColumns.STATE]).size().reset_index(name=NameColumns.TOTAL_CLIENTS)
            return df
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}, Method: total_clients_olt\n {error}")
            exit(1)
    
    
    def total_clients_by_bras(self, df_total_clients: pd.DataFrame) -> pd.DataFrame:
        """Calculate the total of clients group by bras.

        Parameters
        ----------
        df_total_clients : pd.DataFrame
            Dataframe with the data to calcute. This data must have the following columns: Bras, State and Total Clients.
        """
        try:
            df = df_total_clients.copy()
            df.drop(columns=[NameColumns.STATE], inplace=True)
            df = df.groupby(NameColumns.BRAS).sum()
            df[NameColumns.TOTAL_CLIENTS] = df[NameColumns.TOTAL_CLIENTS].round(2)
            df = df.reset_index()
            return df
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}, Method: total_clients_by_bras\n {error}")
            exit(1)

    def total_clients_by_state(self, df_total_clients: pd.DataFrame) -> pd.DataFrame:
        """Calculate the total of clients group by state.

        Parameters
        ----------
        df_total_clients : pd.DataFrame
            Dataframe with the data to calcute. This data must have the following columns: Bras, State and Total Clients.
        """
        try:
            df = df_total_clients.copy()
            df.drop(columns=[NameColumns.BRAS], inplace=True)
            df = df.groupby(NameColumns.STATE).sum()
            df[NameColumns.TOTAL_CLIENTS] = df[NameColumns.TOTAL_CLIENTS].round(2)
            df = df.reset_index()
            return df
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}, Method: total_clients_by_state\n {error}")
            exit(1)
    
    
    def total_consumption_equipment_by_bras(self, df_total_clients_equipment_by_bras: pd.DataFrame, df_total_clients_by_bras: pd.DataFrame, df_consumption: pd.DataFrame, brasnames: list) -> pd.DataFrame:
        """Calculate the total consumption of a equipment group by bras.
        
        Parameters
        ----------
        df_total_clients_equipment_by_bras : pd.DataFrame
            A DataFrame with the total clients per equipment (ADSL, MDU or OLT) Bras only.
        df_total_clients_by_bras : pd.DataFrame
            A DataFrame with the total global clients by bras.
        df_consumption : pd.DataFrame
            A DataFrame with the global consumption by bras.
        brasnames : list
            A list with the bras names.
        """
        try:
            new_data = { NameColumns.BRAS: [], NameColumns.CONSUMPTION: [] }
            bras_consumption_not_found = []
            for name in brasnames:
                if name in df_consumption[NameColumns.BRAS].unique():
                    total_clients = df_total_clients_equipment_by_bras[df_total_clients_equipment_by_bras[NameColumns.BRAS] == name][NameColumns.TOTAL_CLIENTS].iloc[0]
                    total_clients_bras = df_total_clients_by_bras[df_total_clients_by_bras[NameColumns.BRAS] == name][NameColumns.TOTAL_CLIENTS].iloc[0]
                    total_consumption_bras = df_consumption[df_consumption[NameColumns.BRAS] == name][NameColumns.CONSUMPTION].iloc[0].round(2)
                    total_consumption = (total_clients * total_consumption_bras) / total_clients_bras
                    new_data[NameColumns.BRAS].append(name)
                    new_data[NameColumns.CONSUMPTION].append(total_consumption.round(2))
                else:
                    bras_consumption_not_found.append(name)
            df = pd.DataFrame(new_data)
            if bras_consumption_not_found:
                df_missing = pd.DataFrame(bras_consumption_not_found, columns=[NameColumns.BRAS])
                self.__add_missing_bras(df_missing)
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}, Method: total_consumption_equipment_by_bras\n {error}")
            exit(1)
        else:
            return df
        
    
    def total_consumption_state_equipment_by_bras(self, df_consumption_equipment: pd.DataFrame, df_total_clients_equipment_by_state: pd.DataFrame, df_total_clients_equipment_by_bras: pd.DataFrame) -> pd.DataFrame:
        """Calculate the total consumption of a equipment of each state group by bras.
        
        Parameters
        ----------
        df_consumption_equipment : pd.DataFrame
            A DataFrame with the consumption by equipment (ADSL, MDU or OLT) Bras only.
        df_total_clients_equipment_by_state : pd.DataFrame
            A DataFrame with the total clients by state and equipment (ADSL, MDU or OLT) Bras only.
        df_total_clients_equipment_by_bras : pd.DataFrame
            A DataFrame with the total clients by bras.
        """
        try:
            new_data = { NameColumns.BRAS: [], NameColumns.STATE: [], NameColumns.CONSUMPTION: [] }
            bras_consumption_not_found = []
            for _index, row in df_total_clients_equipment_by_state.iterrows():
                bras = row[NameColumns.BRAS]
                state = row[NameColumns.STATE]
                total_clients = row[NameColumns.TOTAL_CLIENTS]
                if bras in df_consumption_equipment[NameColumns.BRAS].unique():
                    total_clients_bras = df_total_clients_equipment_by_bras[df_total_clients_equipment_by_bras[NameColumns.BRAS] == bras][NameColumns.TOTAL_CLIENTS].iloc[0]
                    total_consumption = df_consumption_equipment[df_consumption_equipment[NameColumns.BRAS] == bras][NameColumns.CONSUMPTION].iloc[0]
                    total_consumption_by_state = (total_clients * total_consumption) / total_clients_bras
                    new_data[NameColumns.BRAS].append(bras)
                    new_data[NameColumns.STATE].append(state)
                    new_data[NameColumns.CONSUMPTION].append(total_consumption_by_state.round(2))
                else:
                    bras_consumption_not_found.append(bras)
            df = pd.DataFrame(new_data)
            if bras_consumption_not_found:
                df_missing = pd.DataFrame(bras_consumption_not_found, columns=[NameColumns.BRAS])
                self.__add_missing_bras(df_missing)
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}, Method: total_consumption_state_equipment_by_bras\n {error}")
            exit(1)
        else:
            return df
        
    
    def total_consumption_equipment_by_state(self, df_total_consumption_equipment_by_state: pd.DataFrame) -> pd.DataFrame:
        """Calculate the total consumption of a equipment group by state.
        
        Parameters
        ----------
        df_total_consumption_equipment_by_state : pd.DataFrame
            A DataFrame with the total consumption by equipment (ADSL, MDU or OLT) Bras only.
        """
        try:
            df = df_total_consumption_equipment_by_state.copy()
            df = df.drop(columns=[NameColumns.BRAS])
            df = df.groupby(NameColumns.STATE)[NameColumns.CONSUMPTION].sum()
            df = df.reset_index()
            return df
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}, Method: total_consumption_equipment_by_state\n {error}")
            exit(1)
    
    
    def percentage_consumption_state_equipment_by_bras(self, df_consumption_state_equipment_by_bras: pd.DataFrame, df_consumption_equipment_by_bras: pd.DataFrame) -> pd.DataFrame:
        """Calculate the percentage consumption of a equipment of each state group by bras.
        
        Parameters
        ----------
        df_consumption_state_equipment_by_bras : pd.DataFrame
            A DataFrame with the total consumption of a equipment (ADSL, MDU or OLT) group by bras and state.
        df_consumption_equipment_by_bras : pd.DataFrame
            A DataFrame with the total consumption of a equipment (ADSL, MDU or OLT) Bras only.
        """
        try:
            new_data = { NameColumns.BRAS: [], NameColumns.STATE: [], NameColumns.PERCENTAGE_CONSUMPTION: [] }
            bras_consumption_not_found = []
            for _index, row in df_consumption_state_equipment_by_bras.iterrows():
                bras = row[NameColumns.BRAS]
                state = row[NameColumns.STATE]
                total_consumption = row[NameColumns.CONSUMPTION]
                if bras in df_consumption_equipment_by_bras[NameColumns.BRAS].unique():
                    total_consumption_bras = df_consumption_equipment_by_bras[df_consumption_equipment_by_bras[NameColumns.BRAS] == bras][NameColumns.CONSUMPTION].iloc[0]
                    if total_consumption_bras != 0:
                        total_percentage_bras_by_state = round((total_consumption * 100) / total_consumption_bras)
                    else:
                        total_percentage_bras_by_state = 0
                    new_data[NameColumns.BRAS].append(bras)
                    new_data[NameColumns.STATE].append(state)
                    new_data[NameColumns.PERCENTAGE_CONSUMPTION].append(total_percentage_bras_by_state)
                else:
                    bras_consumption_not_found.append(bras)
            df = pd.DataFrame(new_data)
            if bras_consumption_not_found:
                df_missing = pd.DataFrame(bras_consumption_not_found, columns=[NameColumns.BRAS])
                self.__add_missing_bras(df_missing)
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}, Method: percentage_consumption_state_equipment_by_bras\n {error}")
            exit(1)
        else:
            return df
        
    
    def percentage_consumption_equipment_by_state(self, df_percentage_consumption_state_equipment_by_bras: pd.DataFrame) -> pd.DataFrame:
        """Calculate the percentage consumption of a equipment group by state.
        
        Parameters
        ----------
        df_percentage_consumption_state_equipment_by_bras : pd.DataFrame
            A DataFrame with the percentage consumption of a equipment (ADSL, MDU or OLT) group by bras and state.
        """
        try:
            df = df_percentage_consumption_state_equipment_by_bras.copy()
            df = df.drop(columns=[NameColumns.BRAS])
            df = df.groupby(NameColumns.STATE)[NameColumns.PERCENTAGE_CONSUMPTION].sum()
            df = df.reset_index()
            return df
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}, Method: percentage_consumption_equipment_by_state\n {error}")
            exit(1)