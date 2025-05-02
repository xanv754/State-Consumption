import pandas as pd
from constants.columns import NameColumns
from reader.constants.columns import asf_all_columns, AsfNameColumns
from reader.constants.filepath import Filepath
from reader.reader import Reader



class AsfReader(Reader):
    """Class to read the data from the ASF file."""

    def __init__(self, filename: str):
        super().__init__(filename)

        
    def __check_data_state(self, df: pd.DataFrame) -> bool:
        """Check if all rows have a state."""
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
            df = df[df[NameColumns.STATE].isnull()]
            df = df[df.nunique(axis=1) > 1]
            if not df.empty:
                df.to_excel(Filepath.MISSING_NODES_ASF, index=False)
        except Exception as error:
            raise error

    def get_data(self) -> pd.DataFrame:
        try:
            filename = self.get_filename()
            all_df = pd.read_excel(filename)
            df = all_df[asf_all_columns]
            df = self.__rename_columns(df)
            if self.__check_data_state(df):
                self.__export_missing_nodes(df)
                raise ValueError(f"Some nodes are missing the state. See the file in {Filepath.MISSING_NODES_BOSS}")
            df = df.drop_duplicates(subset=[AsfNameColumns.DNI])
            df = df.reset_index(drop=True)
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            return df