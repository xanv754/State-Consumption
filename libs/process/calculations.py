import pandas as pd
from constants.columns import NameColumns


class Calculate:
    """Class to calculate the data."""

    @staticmethod
    def total_clients_adsl_mdu(data: pd.DataFrame) -> pd.DataFrame:
        """Calculate the total of clients group by state and their bras in ADSL or MDU.
        
        Parameters
        ----------
        data : pd.DataFrame
            Dataframe with the data to calcute. This data must have the following columns: Bras, State and Total Clients.
        """
        df = data.copy()
        df = df.groupby([NameColumns.BRAS, NameColumns.STATE]).sum()
        df[NameColumns.TOTAL_CLIENTS] = df[NameColumns.TOTAL_CLIENTS].round(2)
        df = df.reset_index()
        return df
    
    @staticmethod
    def total_clients_olt(data: pd.DataFrame) -> pd.DataFrame:
        """Calculate the total of clients group by state and their bras in OLT.
        
        Parameters
        ----------
        data : pd.DataFrame
            Dataframe with the data to calcute. This data must have the following columns: Bras, State and Total Clients.
        """
        df = data.copy()
        df = df.groupby([NameColumns.BRAS, NameColumns.STATE]).size().reset_index(name=NameColumns.TOTAL_CLIENTS)
        return df
    
    @staticmethod
    def total_clients_by_bras(df_total_clients: pd.DataFrame) -> pd.DataFrame:
        """Calculate the total of clients group by bras.

        Parameters
        ----------
        df_total_clients : pd.DataFrame
            Dataframe with the data to calcute. This data must have the following columns: Bras, State and Total Clients.
        """
        df = df_total_clients.copy()
        df.drop(columns=[NameColumns.STATE], inplace=True)
        df = df.groupby(NameColumns.BRAS).sum()
        df[NameColumns.TOTAL_CLIENTS] = df[NameColumns.TOTAL_CLIENTS].round(2)
        df = df.reset_index()
        return df
    
    @staticmethod
    def total_consumption_equipment_by_bras(df_total_clients_equipment_by_bras: pd.DataFrame, df_total_clients_by_bras: pd.DataFrame, df_consumption: pd.DataFrame, brasnames: list) -> pd.DataFrame:
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
            for name in brasnames:
                total_clients = df_total_clients_equipment_by_bras[df_total_clients_equipment_by_bras[NameColumns.BRAS] == name][NameColumns.TOTAL_CLIENTS].iloc[0]
                total_clients_bras = df_total_clients_by_bras[df_total_clients_by_bras[NameColumns.BRAS] == name][NameColumns.TOTAL_CLIENTS].iloc[0]
                total_consumption_bras = df_consumption[df_consumption[NameColumns.BRAS] == name][NameColumns.CONSUMPTION].iloc[0].round(2)
                total_consumption = (total_clients * total_consumption_bras) / total_clients_bras
                new_data[NameColumns.BRAS].append(name)
                new_data[NameColumns.CONSUMPTION].append(total_consumption.round(2))
            df = pd.DataFrame(new_data)
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df
        
    @staticmethod
    def total_consumption_state_equipment_by_bras(df_consumption_equipment: pd.DataFrame, df_total_clients_equipment_by_state: pd.DataFrame, df_total_clients_equipment_by_bras: pd.DataFrame) -> pd.DataFrame:
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
            for _index, row in df_total_clients_equipment_by_state.iterrows():
                bras = row[NameColumns.BRAS]
                state = row[NameColumns.STATE]
                total_clients = row[NameColumns.TOTAL_CLIENTS]
                total_clients_bras = df_total_clients_equipment_by_bras[df_total_clients_equipment_by_bras[NameColumns.BRAS] == bras][NameColumns.TOTAL_CLIENTS].iloc[0]
                total_consumption = df_consumption_equipment[df_consumption_equipment[NameColumns.BRAS] == bras][NameColumns.CONSUMPTION].iloc[0]
                total_consumption_by_state = (total_clients * total_consumption) / total_clients_bras
                new_data[NameColumns.BRAS].append(bras)
                new_data[NameColumns.STATE].append(state)
                new_data[NameColumns.CONSUMPTION].append(total_consumption_by_state.round(2))
            df = pd.DataFrame(new_data)
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df
        
    @staticmethod
    def total_consumption_equipment_by_state(df_total_consumption_equipment_by_state: pd.DataFrame) -> pd.DataFrame:
        """Calculate the total consumption of a equipment group by state.
        
        Parameters
        ----------
        df_total_consumption_equipment_by_state : pd.DataFrame
            A DataFrame with the total consumption by equipment (ADSL, MDU or OLT) Bras only.
        """
        df = df_total_consumption_equipment_by_state.copy()
        df = df.drop(columns=[NameColumns.BRAS])
        df = df.groupby(NameColumns.STATE)[NameColumns.CONSUMPTION].sum()
        df = df.reset_index()
        return df
    
    @staticmethod
    def percentage_consumption_state_equipment_by_bras(df_consumption_state_equipment_by_bras: pd.DataFrame, df_consumption_equipment_by_bras: pd.DataFrame) -> pd.DataFrame:
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
            for _index, row in df_consumption_state_equipment_by_bras.iterrows():
                bras = row[NameColumns.BRAS]
                state = row[NameColumns.STATE]
                total_consumption = row[NameColumns.CONSUMPTION]
                total_consumption_bras = df_consumption_equipment_by_bras[df_consumption_equipment_by_bras[NameColumns.BRAS] == bras][NameColumns.CONSUMPTION].iloc[0]
                total_percentage_bras_by_state = round((total_consumption * 100) / total_consumption_bras)
                new_data[NameColumns.BRAS].append(bras)
                new_data[NameColumns.STATE].append(state)
                new_data[NameColumns.PERCENTAGE_CONSUMPTION].append(total_percentage_bras_by_state)
            df = pd.DataFrame(new_data)
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df
        
    @staticmethod
    def percentage_consumption_equipment_by_state(df_percentage_consumption_state_equipment_by_bras: pd.DataFrame) -> pd.DataFrame:
        """Calculate the percentage consumption of a equipment group by state.
        
        Parameters
        ----------
        df_percentage_consumption_state_equipment_by_bras : pd.DataFrame
            A DataFrame with the percentage consumption of a equipment (ADSL, MDU or OLT) group by bras and state.
        """
        df = df_percentage_consumption_state_equipment_by_bras.copy()
        df = df.drop(columns=[NameColumns.BRAS])
        df = df.groupby(NameColumns.STATE)[NameColumns.PERCENTAGE_CONSUMPTION].sum()
        df = df.reset_index()
        return df