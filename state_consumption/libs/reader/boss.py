import pandas as pd
from state_consumption.constants import (
    NameColumns,
    PathStderr,
    BossNewNameColumns,
    BossNameColumns,
    StatusClients,
    boss_all_columns,
)
from state_consumption.utils import FixFormat, terminal, logger
from state_consumption.database import MongoDatabase, FindQuery
from state_consumption.libs.reader.reader import Reader


class BossReader(Reader):
    """Class to read the data from the BOSS file."""

    _database: MongoDatabase

    def __init__(self, filename: str, dev: bool = False, testing: bool = False):
        if dev:
            self._database = MongoDatabase(dev=True)
        elif testing:
            self._database = MongoDatabase(testing=True)
        else:
            self._database = MongoDatabase()
        super().__init__(filename)

    def _format_column_bras(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format the column of the Bras."""
        df = df.copy()
        df = FixFormat.column_word(df, NameColumns.BRAS)
        return df

    def _get_clients_active(self, df: pd.DataFrame) -> pd.DataFrame:
        """Get the clients active."""
        df = df.copy()
        df = df[df[BossNameColumns.STATUS] == StatusClients.BOSS_ACTIVE]
        return df

    def _check_format_data(self, df: pd.DataFrame) -> None:
        """Check if the data has been correctly to process."""
        for column in df.columns.to_list():
            if column.startswith("Unnamed"):
                raise Exception(
                    "The BOSS file has missing columns. Maybe the data has been moved"
                )

    def _check_column_state(self, df: pd.DataFrame) -> bool:
        """Check if the column state is in the data."""
        return NameColumns.STATE in df.columns.to_list()

    def _check_data_state(self, df: pd.DataFrame) -> bool:
        """Check if all rows have a state."""
        return df[NameColumns.STATE].isnull().any()

    def _unite_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Unite the columns of the data."""
        df = df.copy()
        df[NameColumns.BRAS] = (
            df[BossNameColumns.PREFIX_BRAS] + "-" + df[BossNameColumns.SUFFIX_BRAS]
        )
        df[NameColumns.BRAS] = df[NameColumns.BRAS].str.upper()
        df.drop(
            columns=[BossNameColumns.PREFIX_BRAS, BossNameColumns.SUFFIX_BRAS],
            inplace=True,
        )
        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rename the columns of the data."""
        df = df.copy()
        df.rename(
            columns={
                BossNameColumns.EQUIPMENT: BossNewNameColumns.EQUIPMENT,
                BossNameColumns.CENTRAL: BossNewNameColumns.CENTRAL,
                BossNameColumns.ACCOUNT_CODE: BossNewNameColumns.ACCOUNT_CODE,
                BossNameColumns.TOTAL_CLIENTS: NameColumns.TOTAL_CLIENTS,
            },
            inplace=True,
        )
        return df

    def _add_state(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add the state to the data."""
        df = df.copy()
        df[NameColumns.STATE] = None
        query = FindQuery(db=self._database)
        list_account_code = df[BossNewNameColumns.ACCOUNT_CODE].unique().tolist()
        for account_code in list_account_code:
            mask = df[BossNewNameColumns.ACCOUNT_CODE] == account_code
            state = query.find_state_by_cc(str(account_code))
            if state:
                df.loc[mask, NameColumns.STATE] = state
        return df

    def _fix_name_central(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fix the name of the central."""
        df = df.copy()
        df = FixFormat.column_word(df, BossNewNameColumns.CENTRAL)
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
            df.to_excel(PathStderr().MISSING_NODES_BOSS, index=False)
            logger.warning(
                f"Nodos sin estados guardados en {PathStderr().MISSING_NODES_BOSS}"
            )
            terminal.print_spinner(
                f"[orange3]WARNING: Nodos sin estados guardados en {PathStderr().MISSING_NODES_BOSS}"
            )
        except Exception as error:
            logger.error(
                f"No se ha podido exportar los nodos sin estados de BOSS - {error}"
            )
            terminal.print_spinner(
                f"[red3]ERROR: [default]No se ha podido exportar los nodos sin estados de BOSS - {error}"
            )
            exit(1)

    def get_data(self) -> pd.DataFrame:
        try:
            terminal.spinner(text="Extrayendo data de BOSS...")
            filename = self.get_filename()
            all_df = pd.read_excel(filename)
            self._check_format_data(all_df)
            if not self._check_column_state(all_df):
                df = all_df[boss_all_columns]
            else:
                columns = boss_all_columns + [NameColumns.STATE]
                df = all_df[columns]
            df = self._unite_columns(df)
            df = self._rename_columns(df)
            df = self._fix_name_central(df)
            if not self._check_column_state(df):
                df = self._add_state(df)
            if self._check_data_state(df):
                terminal.spinner(stop=True)
                self._export_missing_nodes(df)
                raise ValueError(
                    f"Nodos sin estados. Revise el archivo {PathStderr().MISSING_NODES_BOSS} para más información"
                )
            df = self._format_column_bras(df)
            df = self._get_clients_active(df)
            df = df.reset_index(drop=True)
            terminal.spinner(stop=True)
        except Exception as error:
            logger.error(
                f"No se ha podido obtener la data del archivos de BOSS - {error}"
            )
            terminal.print_spinner(
                f"[red3]ERROR: [default]No se ha podido obtener la data del archivos de BOSS - {error}"
            )
            exit(1)
        else:
            return df

    def check_reader(self) -> bool:
        """Check if the data is valid."""
        try:
            self.get_data()
        except Exception as error:
            logger.error(f"Problemas en la comprobación de la data de BOSS - {error}")
            terminal.print_spinner(
                f"[red3]ERROR: [default]Problemas en la comprobación de la data de BOSS - {error}"
            )
            return False
        else:
            return True
