import pandas as pd
from constants.columns import NameColumns
from constants.path import PathStderr
from database.querys.nodes import NodesQueryMongo
from libs.reader.constants.columns import boss_all_columns, BossNewNameColumns, BossNameColumns
from libs.reader.reader import Reader
from utils.format import FixFormat
from utils.console import terminal


class BossReader(Reader):
    """Class to read the data from the BOSS file."""

    def __init__(self, filename: str):
        super().__init__(filename)


    def __check_format_data(self, df: pd.DataFrame) -> None:
        """Check if the data has been correctly to process."""
        for column in df.columns.to_list():
            if column.startswith("Unnamed"):
                raise Exception("The BOSS file has missing columns. Maybe the data has been moved")
            
    def __check_column_state(self, df: pd.DataFrame) -> bool:
        """Check if the column state is in the data."""
        return NameColumns.STATE in df.columns.to_list()
    
    def __check_data_state(self, df: pd.DataFrame) -> bool:
        """Check if all rows have a state."""
        return df[NameColumns.STATE].isnull().any()
        
    def __unite_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Unite the columns of the data."""
        df = df.copy()
        df[NameColumns.BRAS] = df[BossNameColumns.PREFIX_BRAS] + "-" + df[BossNameColumns.SUFFIX_BRAS]
        df[NameColumns.BRAS] = df[NameColumns.BRAS].str.upper()
        df.drop(columns=[BossNameColumns.PREFIX_BRAS, BossNameColumns.SUFFIX_BRAS], inplace=True)
        return df
    
    def __rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rename the columns of the data."""
        df = df.copy()
        df.rename(
            columns={
                BossNameColumns.EQUIPMENT: BossNewNameColumns.EQUIPMENT,
                BossNameColumns.CENTRAL: BossNewNameColumns.CENTRAL, 
                BossNameColumns.ACCOUNT_CODE: BossNewNameColumns.ACCOUNT_CODE,
                BossNameColumns.TOTAL_CLIENTS: NameColumns.TOTAL_CLIENTS
            }, 
            inplace=True
        )
        return df
    
    def __add_state(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add the state to the data."""
        df = df.copy()
        df[NameColumns.STATE] = None
        list_account_code = df[BossNewNameColumns.ACCOUNT_CODE].unique().tolist()
        for account_code in list_account_code:
            mask = df[BossNewNameColumns.ACCOUNT_CODE] == account_code
            data_node = NodesQueryMongo.find_by_account_code(str(account_code))
            if data_node:
                df.loc[mask, NameColumns.STATE] = data_node[0].state
        return df
    
    def __fix_name_central(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fix the name of the central."""
        df = df.copy()
        df = FixFormat.column_word(df, BossNewNameColumns.CENTRAL)
        return df
    
    def __export_missing_nodes(self, df: pd.DataFrame) -> None:
        """Export the missing nodes to a .xlsx file."""
        try:
            terminal.print(f"Some nodes are missing the state. Saving nodes missing information...")
            df = df[df[NameColumns.STATE].isnull()]
            df = df[df.nunique(axis=1) > 1]
            df.to_excel(PathStderr.MISSING_NODES_BOSS, index=False)
            terminal.print(f"Nodes missing saved in {PathStderr.MISSING_NODES_BOSS}!")
        except Exception as error:
            exit(1)

    def get_data(self) -> pd.DataFrame:
        try:
            terminal.spinner(text="Reading data BOSS...")
            filename = self.get_filename()
            all_df = pd.read_excel(filename)
            self.__check_format_data(all_df)
            df = all_df[boss_all_columns]
            df = self.__unite_columns(df)
            df = self.__rename_columns(df)
            df = self.__fix_name_central(df)
            if not self.__check_column_state(df): 
                df = self.__add_state(df)
            if self.__check_data_state(df):
                terminal.spinner(stop=True)
                self.__export_missing_nodes(df)
                raise ValueError(f"Some nodes are missing the state. See the file in {PathStderr.MISSING_NODES_BOSS}")
            terminal.spinner(stop=True)
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}\n {error}")
            exit(1)
        else:
            return df