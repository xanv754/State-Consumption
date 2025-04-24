import pandas as pd
from database.querys.nodes import NodesQueryMongo
from reader.constants.columns import boss_all_columns, BossNewNameColumns, BossNameColumns
from reader.constants.filepath import Filepath
from reader.reader import Reader



class BossReader(Reader):
    """Class to read the data from the BOSS file."""

    def __init__(self, filename: str):
        super().__init__(filename)


    def __check_data(self, df: pd.DataFrame) -> None:
        """Check if the data has been correctly to process."""
        for column in df.columns.to_list():
            if column.startswith("Unnamed"):
                raise Exception("The BOSS file has missing columns. Maybe the data has been moved")
            
    def __check_column_state(self, df: pd.DataFrame) -> None:
            """Check if the column state is in the data."""
            return BossNewNameColumns.STATE in df.columns.to_list()
    
    def __check_state(self, df: pd.DataFrame) -> None:
        """Check if all rows have a state."""
        return df[BossNewNameColumns.STATE].isnull().any()
        
    def __unite_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Unite the columns of the data."""
        df = df.copy()
        df[BossNewNameColumns.BRAS] = df[BossNameColumns.PREFIX_BRAS] + "-" + df[BossNameColumns.SUFFIX_BRAS]
        df[BossNewNameColumns.BRAS] = df[BossNewNameColumns.BRAS].str.upper()
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
                BossNameColumns.TOTAL_CLIENTS: BossNewNameColumns.TOTAL_CLIENTS
            }, 
            inplace=True
        )
        return df
    
    def __add_state(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add the state to the data."""
        df = df.copy()
        df[BossNewNameColumns.STATE] = None
        list_account_code = df[BossNewNameColumns.ACCOUNT_CODE].unique().tolist()
        for account_code in list_account_code:
            mask = df[BossNewNameColumns.ACCOUNT_CODE] == account_code
            data_node = NodesQueryMongo.find_by_account_code(str(account_code))
            if data_node:
                df.loc[mask, BossNewNameColumns.STATE] = data_node[0].state
        return df
    
    def __export_missing_nodes(self, df: pd.DataFrame) -> None:
        """Export the missing nodes to a .xlsx file."""
        try:
            df = df[df[BossNewNameColumns.STATE].isnull()]
            df = df[df.nunique(axis=1) > 1]
            if not df.empty:
                df.to_excel(Filepath.MISSING_NODES, index=False)
        except Exception as error:
            raise error

    def get_data(self) -> pd.DataFrame:
        try:
            filename = self.get_filename()
            all_df = pd.read_excel(filename)
            self.__check_data(all_df)
            df = all_df[boss_all_columns]
            df = self.__unite_columns(df)
            df = self.__rename_columns(df)
            if not self.__check_column_state(df): 
                df = self.__add_state(df)
            if self.__check_state(df):
                self.__export_missing_nodes(df)
                raise ValueError(f"Some nodes are missing the state. See the file in {Filepath.MISSING_NODES}")
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df