import pandas as pd
from state_consumption.constants import NameColumns, PathStderr
from state_consumption.utils import ExcelExport, terminal, logger


class Calculate:
    """Class to calculate the data."""

    _exported: bool = False
    missing_bras: pd.DataFrame = pd.DataFrame({NameColumns.BRAS: []})

    def _add_missing_bras(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add the missing bras to the data."""
        df = pd.concat([self.missing_bras, df], axis=0)
        self.missing_bras = df

    def export_missing_bras(self) -> None:
        """Export the missing bras to a .xlsx file."""
        if not self.missing_bras.empty:
            df = self.missing_bras.drop_duplicates()
            excel = ExcelExport(PathStderr().MISSING_CONSUMPTION)
            excel.export(data=df, sheet_name=NameColumns.BRAS)
            if self._exported:
                return
            self._exported = True
            logger.warning(
                f"Algunos consumos del agregador no se han encontrado. Información guardada en {PathStderr().MISSING_CONSUMPTION}"
            )
            terminal.print_spinner(
                f"[orange3]WARNING: Algunos consumos del agregador no se han encontrado. Información guardada en {PathStderr().MISSING_CONSUMPTION}"
            )

    def total_clients_adsl_mdu(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate the total of clients group by state and their bras in ADSL or MDU.

        :params data: Dataframe with the data to calcute. This data must have the following columns: Bras, State and Total Clients.
        :type data: DataFrame
        :returns DataFrame: Proccesed data.
        """
        try:
            df = data.copy()
            df = df.groupby([NameColumns.BRAS, NameColumns.STATE]).sum()
            df[NameColumns.TOTAL_CLIENTS] = df[NameColumns.TOTAL_CLIENTS].round(2)
            df = df.reset_index()
            return df
        except Exception as error:
            logger.error(
                f"Problemas al calcular el total de clientes ADSL y MDU - {error}"
            )
            terminal.print_spinner(
                f"[red3]ERROR: [default]Problemas al calcular el total de clientes ADSL y MDU - {error}"
            )
            exit(1)

    def total_clients_olt(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate the total of clients group by state and their bras in OLT.

        :params data: Dataframe with the data to calcute. This data must have the following columns: Bras, State and Total Clients.
        :type data: DataFrame
        :returns DataFrame: Proccesed data.
        """
        try:
            df = data.copy()
            df = (
                df.groupby([NameColumns.BRAS, NameColumns.STATE])
                .size()
                .reset_index(name=NameColumns.TOTAL_CLIENTS)
            )
            return df
        except Exception as error:
            logger.error(f"Problemas al calcular el total de clientes OLT - {error}")
            terminal.print_spinner(
                f"[red3]ERROR: [default]Problemas al calcular el total de clientes OLT - {error}"
            )
            exit(1)

    def total_clients_by_bras(self, df_total_clients: pd.DataFrame) -> pd.DataFrame:
        """Calculate the total of clients group by bras.

        :params df_total_clients: Dataframe with the data to calcute. This data must have the following columns: Bras, State and Total Clients.
        :type df_total_clients: DataFrame
        :returns DataFrame: Proccesed data.
        """
        try:
            df = df_total_clients.copy()
            df.drop(columns=[NameColumns.STATE], inplace=True)
            df = df.groupby(NameColumns.BRAS).sum()
            df[NameColumns.TOTAL_CLIENTS] = df[NameColumns.TOTAL_CLIENTS].round(2)
            df = df.reset_index()
            return df
        except Exception as error:
            logger.error(
                f"Problemas al calcular el total de clientes agrupados por agregador - {error}"
            )
            terminal.print_spinner(
                f"[red3]ERROR: [default]Problemas al calcular el total de clientes agrupados por agregador - {error}"
            )
            exit(1)

    def total_clients_by_state(self, df_total_clients: pd.DataFrame) -> pd.DataFrame:
        """Calculate the total of clients group by state.

        :params df_total_clients: Dataframe with the data to calcute. This data must have the following columns: Bras, State and Total Clients.
        :type df_total_clients: DataFrame
        :returns DataFrame: Proccesed data.
        """
        try:
            df = df_total_clients.copy()
            df.drop(columns=[NameColumns.BRAS], inplace=True)
            df = df.groupby(NameColumns.STATE).sum()
            df[NameColumns.TOTAL_CLIENTS] = df[NameColumns.TOTAL_CLIENTS].round(2)
            df = df.reset_index()
            return df
        except Exception as error:
            logger.error(
                f"Problemas al calcular el total de clientes agrupados por estado - {error}"
            )
            terminal.print_spinner(
                f"[red3]ERROR: [default]Problemas al calcular el total de clientes agrupados por estado - {error}"
            )
            exit(1)

    def total_consumption_equipment_by_bras(
        self,
        df_total_clients_equipment_by_bras: pd.DataFrame,
        df_total_clients_by_bras: pd.DataFrame,
        df_consumption: pd.DataFrame,
        brasnames: list,
    ) -> pd.DataFrame:
        """Calculate the total consumption of a equipment group by bras.

        :params df_total_clients_equipment_by_bras: A DataFrame with the total clients per equipment (ADSL, MDU or OLT) Bras only.
        :type df_total_clients_equipment_by_bras: DataFrame
        :params df_total_clients_by_bras: A DataFrame with the total global clients by bras.
        :type df_total_clients_by_bras: DataFrame
        :params df_consumption: A DataFrame with the global consumption by bras.
        :type df_consumption: DataFrame
        :params brasnames: A list with the bras names.
        :type brasnames: list
        :returns DataFrame: Proccesed data.
        """
        try:
            new_data = {NameColumns.BRAS: [], NameColumns.CONSUMPTION: []}
            bras_consumption_not_found = []
            for name in brasnames:
                if name in df_consumption[NameColumns.BRAS].unique():
                    total_clients = df_total_clients_equipment_by_bras[
                        df_total_clients_equipment_by_bras[NameColumns.BRAS] == name
                    ][NameColumns.TOTAL_CLIENTS].iloc[0]
                    total_clients_bras = df_total_clients_by_bras[
                        df_total_clients_by_bras[NameColumns.BRAS] == name
                    ][NameColumns.TOTAL_CLIENTS].iloc[0]
                    total_consumption_bras = (
                        df_consumption[df_consumption[NameColumns.BRAS] == name][
                            NameColumns.CONSUMPTION
                        ]
                        .iloc[0]
                        .round(2)
                    )
                    total_consumption = (
                        total_clients * total_consumption_bras
                    ) / total_clients_bras
                    new_data[NameColumns.BRAS].append(name)
                    new_data[NameColumns.CONSUMPTION].append(total_consumption.round(2))
                else:
                    bras_consumption_not_found.append(name)
            df = pd.DataFrame(new_data)
            if bras_consumption_not_found:
                df_missing = pd.DataFrame(
                    bras_consumption_not_found, columns=[NameColumns.BRAS]
                )
                self._add_missing_bras(df_missing)
        except Exception as error:
            logger.error(
                f"Problemas al calcular el total de consumo de equipos por agregador - {error}"
            )
            terminal.print_spinner(
                f"[red3]ERROR: [default]Problemas al calcular el total de consumo de equipos por agregador - {error}"
            )
            exit(1)
        else:
            return df

    def total_consumption_state_equipment_by_bras(
        self,
        df_consumption_equipment: pd.DataFrame,
        df_total_clients_equipment_by_state: pd.DataFrame,
        df_total_clients_equipment_by_bras: pd.DataFrame,
    ) -> pd.DataFrame:
        """Calculate the total consumption of a equipment of each state group by bras.

        :params df_consumption_equipment: A DataFrame with the consumption by equipment (ADSL, MDU or OLT) Bras only.
        :type df_consumption_equipment: pd.DataFrame
        :params df_total_clients_equipment_by_state: A DataFrame with the total clients by state and equipment (ADSL, MDU or OLT) Bras only.
        :type df_total_clients_equipment_by_state: pd.DataFrame
        :params df_total_clients_equipment_by_bras: A DataFrame with the total clients by bras.
        :type df_total_clients_equipment_by_bras: pd.DataFrame
        :returns DataFrame: Proccesed data.
        """
        try:
            new_data = {
                NameColumns.BRAS: [],
                NameColumns.STATE: [],
                NameColumns.CONSUMPTION: [],
            }
            bras_consumption_not_found = []
            for _index, row in df_total_clients_equipment_by_state.iterrows():
                bras = row[NameColumns.BRAS]
                state = row[NameColumns.STATE]
                total_clients = row[NameColumns.TOTAL_CLIENTS]
                if bras in df_consumption_equipment[NameColumns.BRAS].unique():
                    total_clients_bras = df_total_clients_equipment_by_bras[
                        df_total_clients_equipment_by_bras[NameColumns.BRAS] == bras
                    ][NameColumns.TOTAL_CLIENTS].iloc[0]
                    total_consumption = df_consumption_equipment[
                        df_consumption_equipment[NameColumns.BRAS] == bras
                    ][NameColumns.CONSUMPTION].iloc[0]
                    total_consumption_by_state = (
                        total_clients * total_consumption
                    ) / total_clients_bras
                    new_data[NameColumns.BRAS].append(bras)
                    new_data[NameColumns.STATE].append(state)
                    new_data[NameColumns.CONSUMPTION].append(
                        total_consumption_by_state.round(2)
                    )
                else:
                    bras_consumption_not_found.append(bras)
            df = pd.DataFrame(new_data)
            if bras_consumption_not_found:
                df_missing = pd.DataFrame(
                    bras_consumption_not_found, columns=[NameColumns.BRAS]
                )
                self._add_missing_bras(df_missing)
        except Exception as error:
            logger.error(
                f"Problemas al calcular el total de consumo por estado agrupados por agregador - {error}"
            )
            terminal.print_spinner(
                f"[red3]ERROR: [default]Problemas al calcular el total de consumo por estado agrupados por agregador - {error}"
            )
            exit(1)
        else:
            return df

    def total_consumption_equipment_by_state(
        self, df_total_consumption_equipment_by_state: pd.DataFrame
    ) -> pd.DataFrame:
        """Calculate the total consumption of a equipment group by state.

        :params df_total_consumption_equipment_by_state: A DataFrame with the total consumption by equipment (ADSL, MDU or OLT) Bras only.
        :type df_total_consumption_equipment_by_state: pd.DataFrame
        :returns DataFrame: Proccesed data.
        """
        try:
            df = df_total_consumption_equipment_by_state.copy()
            df = df.drop(columns=[NameColumns.BRAS])
            df = df.groupby(NameColumns.STATE)[NameColumns.CONSUMPTION].sum()
            df = df.reset_index()
            return df
        except Exception as error:
            logger.error(
                f"Problemas al calcular el total de consumo por estado - {error}"
            )
            terminal.print_spinner(
                f"[red3]ERROR: [default]Problemas al calcular el total de consumo por estado - {error}"
            )
            exit(1)

    def percentage_consumption_by_state(
        self, df_consumption_by_state: pd.DataFrame, total_consumption: float
    ) -> pd.DataFrame:
        """Calculate the percentage consumption of each state.

        :params df_consumption_by_state: A DataFrame with the consumption by state Bras only.
        :type df_consumption_by_state: pd.DataFrame
        :params total_consumption: Total consumption of the equipment.
        type total_consumption: float
        :returns DataFrame: Proccesed data.
        """
        try:
            df = df_consumption_by_state.copy()
            df[NameColumns.PERCENTAGE_CONSUMPTION] = (
                (df[NameColumns.CONSUMPTION] * 100) / total_consumption
            ).round(2)
            df = df.drop(columns=[NameColumns.CONSUMPTION])
            df = df.reset_index(drop=True)
            return df
        except Exception as error:
            logger.error(
                f"Problemas al calcular el porcentaje de consumo por estado - {error}"
            )
            terminal.print_spinner(
                f"[red3]ERROR: [default]Problemas al calcular el porcentaje de consumo por estado - {error}"
            )
            exit(1)
