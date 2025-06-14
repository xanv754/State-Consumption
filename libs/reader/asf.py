import pandas as pd
from constants.columns import NameColumns
from constants.path import PathStderr
from libs.reader.constants.columns import asf_all_columns, AsfNameColumns
from libs.reader.constants.status import StatusClients
from libs.reader.reader import Reader
from utils.format import FixFormat
from utils.console import terminal


class AsfReader(Reader):
    """Class to read the data from the ASF file."""

    def __init__(self, filename: str):
        super().__init__(filename)


    def __format_column_bras(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format the column of the Bras."""
        df = df.copy()
        df = FixFormat.column_word(df, NameColumns.BRAS)
        return df
    
    def __get_clients_active(self, df: pd.DataFrame) -> pd.DataFrame:
        """Get the clients active."""
        df = df.copy()
        df = df[df[AsfNameColumns.STATUS] == StatusClients.ASF_ACTIVE]
        return df
        
    def __check_data_state(self, df: pd.DataFrame) -> bool:
        """Check if all rows have a state.
        
        Returns
        -------
        bool
            True if exists rows without state, False otherwise.
        """
        return df[NameColumns.STATE].isnull().any()
        
    def __rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rename the columns of the data."""
        df = df.copy()
        df.rename(
            columns={
                AsfNameColumns.BRAS: NameColumns.BRAS, 
                AsfNameColumns.STATE: NameColumns.STATE,
            }, 
            inplace=True
        )
        return df
    
    def __export_missing_nodes(self, df: pd.DataFrame) -> None:
        """Export the missing nodes to a .xlsx file."""
        try:
            terminal.print(f"Some nodes are missing the state. Saving nodes missing information...")
            df = df[df[NameColumns.STATE].isnull()]
            df = df[df.nunique(axis=1) > 1]
            df.to_excel(PathStderr.MISSING_NODES_ASF, index=False)
            terminal.print(f"Nodes missing saved in {PathStderr.MISSING_NODES_ASF}!")
        except Exception as error:
            raise error

    def get_data(self) -> pd.DataFrame:
        try:
            terminal.spinner(text="Reading data ASF...")
            filename = self.get_filename()
            all_df = pd.read_excel(filename)
            df = all_df[asf_all_columns]
            df = self.__rename_columns(df)
            if self.__check_data_state(df):
                terminal.spinner(stop=True)
                self.__export_missing_nodes(df)
                raise ValueError(f"Some nodes are missing the state. See the file in {PathStderr.MISSING_NODES_BOSS}")
            df = self.__format_column_bras(df)
            df = df.drop_duplicates(subset=[AsfNameColumns.DNI])
            df = self.__get_clients_active(df)
            df = df.reset_index(drop=True)
            terminal.spinner(stop=True)
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}\n {error}")
            exit(1)
        else:
            return df
        
    def check_reader(self) -> bool:
        """Check if the data is valid."""
        try:
            self.get_data()
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}\n {error}")
            return False
        else:
            return True