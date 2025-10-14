import pandas as pd
from state_consumption.constants import (
    NameColumns,
    PathStderr,
    AsfNameColumns,
    StatusClients,
    asf_all_columns,
)
from state_consumption.utils import FixFormat, terminal, logger
from state_consumption.libs.reader.reader import Reader


class AsfReader(Reader):
    """Class to read the data from the ASF file."""

    def __init__(self, filename: str):
        super().__init__(filename)

    def _format_column_bras(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format the column of the Bras."""
        df = df.copy()
        df = FixFormat.column_word(df, NameColumns.BRAS)
        return df

    def _get_clients_active(self, df: pd.DataFrame) -> pd.DataFrame:
        """Get the clients active."""
        df = df.copy()
        df = df[df[AsfNameColumns.STATUS] == StatusClients.ASF_ACTIVE]
        return df

    def _check_data_state(self, df: pd.DataFrame) -> bool:
        """Check if all rows have a state.

        :returns bool: True if exists rows without state, False otherwise.
        """
        return df[NameColumns.STATE].isnull().any()

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rename the columns of the data."""
        df = df.copy()
        df.rename(
            columns={
                AsfNameColumns.BRAS: NameColumns.BRAS,
                AsfNameColumns.STATE: NameColumns.STATE,
            },
            inplace=True,
        )
        return df

    def _export_missing_nodes(self, df: pd.DataFrame) -> None:
        """Export the missing nodes to a .xlsx file."""
        try:
            logger.warning(
                "Algunos nodos no se han podido ubicar su estado. Guardando los nodos perdidos..."
            )
            terminal.print_spinner(
                f"[orange3]WARNING: Algunos nodos no se han podido ubicar su estado. Guardando los nodos perdidos..."
            )
            df = df[df[NameColumns.STATE].isnull()]
            df = df[df.nunique(axis=1) > 1]
            df.to_excel(PathStderr().MISSING_NODES_ASF, index=False)
            logger.warning(
                f"Nodos sin estados guardados en {PathStderr().MISSING_NODES_ASF}"
            )
            terminal.print_spinner(
                f"[orange3]WARNING: Nodos sin estados guardados en {PathStderr().MISSING_NODES_ASF}"
            )
        except Exception as error:
            logger.error(
                f"No se ha podido exportar los nodos sin estados del ASF - {error}"
            )
            terminal.print_spinner(
                f"[red3]ERROR: [default]No se ha podido exportar los nodos sin estados del ASF - {error}"
            )
            exit(1)

    def get_data(self) -> pd.DataFrame:
        try:
            terminal.spinner(text="Extrayendo data del ASF...")
            filename = self.get_filename()
            all_df = pd.read_excel(filename)
            df = all_df[asf_all_columns]
            df = self._rename_columns(df)
            if self._check_data_state(df):
                terminal.spinner(stop=True)
                self._export_missing_nodes(df)
                raise ValueError(
                    f"Nodos sin estados. Revise el archivo {PathStderr().MISSING_NODES_ASF} para más información"
                )
            df = self._format_column_bras(df)
            df = self._get_clients_active(df)
            df = df.reset_index(drop=True)
            terminal.spinner(stop=True)
        except Exception as error:
            logger.error(
                f"No se ha podido obtener la data del archivos del ASF - {error}"
            )
            terminal.print_spinner(
                f"[red3]ERROR: [default]No se ha podido obtener la data del archivos del ASF - {error}"
            )
            exit(1)
        else:
            return df

    def check_reader(self) -> bool:
        """Check if the data is valid."""
        try:
            self.get_data()
        except Exception as error:
            logger.error(f"Problemas en la comprobación de la data del ASF - {error}")
            terminal.print_spinner(
                f"[red3]ERROR: [default]Problemas en la comprobación de la data del ASF - {error}"
            )
            return False
        else:
            return True
