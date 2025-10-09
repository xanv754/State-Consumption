import pandas as pd
from state_consumption.constants import NameColumns
from state_consumption.utils import FixFormat, terminal, logger
from state_consumption.libs.reader.reader import Reader


class ConsumptionTrafficReader(Reader):
    """Class to read the data from the consumption traffic file."""
    
    _process: bool

    def __init__(self, path: str, process: bool):
        self._process = process
        super().__init__(path)

    def _format_column_bras(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format the column of the Bras."""
        df = df.copy()
        df = FixFormat.column_word(df, NameColumns.BRAS)
        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
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
    
    def _transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform the data to delete model and capacity of bras name."""
        df = df.copy()
        df[NameColumns.BRAS] = df[NameColumns.BRAS].apply(lambda x: x.split("_")[0])
        df[NameColumns.BRAS] = df[NameColumns.BRAS].str.upper()
        return df

    def _totalize_consumption(self, df: pd.DataFrame) -> pd.DataFrame:
        """Totalize the consumption by bras."""
        df = df.copy()
        df = df.groupby(NameColumns.BRAS).sum()
        df = df.reset_index()
        return df

    def get_data(self) -> pd.DataFrame:
        try:
            terminal.spinner(text="Extrayendo data de consumo...")
            filename = self.get_filename()
            df = pd.read_excel(filename)
            df = self._rename_columns(df)
            if self._process: 
                df = self._transform_data(df)
                df = self._totalize_consumption(df)
            df = self._format_column_bras(df)
            terminal.spinner(stop=True)
        except Exception as error:
            logger.error(f"No se ha podido obtener la data de consumo del archivos de BRAS - {error}")
            terminal.print(f"[red3]ERROR: [default]No se ha podido obtener la data de consumo del archivo de BRAS - {error}")
            exit(1)
        else:
            return df
        
    def check_reader(self) -> bool:
        try:
            self.get_data()
        except Exception as error:
            logger.error(f"Problemas en la comprobación de la data de consumo del archivo de BRAS - {error}")
            terminal.print(f"[red3]ERROR: [default]Problemas en la comprobación de la data de consumo del archivo de BRAS - {error}")
            return False
        else:
            return True
        