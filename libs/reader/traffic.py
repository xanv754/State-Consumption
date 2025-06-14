import pandas as pd
from constants.columns import NameColumns
from libs.reader.reader import Reader
from utils.format import FixFormat
from utils.console import terminal


class ConsumptionTrafficReader(Reader):
    """Class to read the data from the consumption traffic file."""
    
    __process: bool

    def __init__(self, path: str, process: bool):
        self.__process = process
        super().__init__(path)

    def __format_column_bras(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format the column of the Bras."""
        df = df.copy()
        df = FixFormat.column_word(df, NameColumns.BRAS)
        return df

    def __rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rename the columns of the data."""
        df = df.copy()
        old_columns = df.columns.to_list()
        df.rename(
            columns={
                old_columns[0]: NameColumns.BRAS,
                old_columns[1]: NameColumns.CONSUMPTION
            },
            inplace=True
        )
        return df
    
    def __transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform the data to delete model and capacity of bras name."""
        df = df.copy()
        df[NameColumns.BRAS] = df[NameColumns.BRAS].apply(lambda x: x.split("_")[0])
        df[NameColumns.BRAS] = df[NameColumns.BRAS].str.upper()
        return df

    def __totalize_consumption(self, df: pd.DataFrame) -> pd.DataFrame:
        """Totalize the consumption by bras."""
        df = df.copy()
        df = df.groupby(NameColumns.BRAS).sum()
        df = df.reset_index()
        return df

    def get_data(self) -> pd.DataFrame:
        try:
            terminal.spinner(text="Reading data consumption...")
            filename = self.get_filename()
            df = pd.read_excel(filename)
            df = self.__rename_columns(df)
            if self.__process: 
                df = self.__transform_data(df)
                df = self.__totalize_consumption(df)
            df = self.__format_column_bras(df)
            terminal.spinner(stop=True)
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}\n {error}")
            exit(1)
        else:
            return df
        
    def check_reader(self) -> bool:
        try:
            self.get_data()
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}\n {error}")
            return False
        else:
            return True
        