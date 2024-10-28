import pandas as pd
from common import fix_format_word, colname
from olt.lib.data import load_data_olt
from olt.constant import columns as COLUMNS
from olt.constant.exception import DISTRIT

class ReportOLTController:
    validate: bool = False
    report: pd.DataFrame
    state_col_name: str | None = None
    clients_col_name: str | None = None
    consumption_col_name: str | None = None

    def __init__(self, filename: str):
        self.report = load_data_olt(filename)
        self.__set_columns()
        if self.__validate_columns():
            self.__refactor_states()
            self.__delete_columns()
            self.validate = True

    def __set_columns(self) -> None:
        """Set the columns of the dataframe."""
        try:
            for name in self.report.columns.to_list():
                if name in COLUMNS.STATE and self.state_col_name is None: 
                    self.state_col_name = name
                elif name in COLUMNS.STATE and self.state_col_name is not None:
                    raise Exception(f"There are two columns related to «Estado» in its name")
                if name in COLUMNS.CLIENTS and self.clients_col_name is None:
                    self.clients_col_name = name
                elif name in COLUMNS.CLIENTS and self.clients_col_name is not None:
                    raise Exception(f"There are two columns related to «Usuarios» in its name")
                if name in COLUMNS.CONSUMPTION and self.consumption_col_name is None:
                    self.consumption_col_name = name
                elif name in COLUMNS.CONSUMPTION and self.consumption_col_name is not None:
                    raise Exception(f"There are two columns related to «Consumo» in its name")
        except Exception as error:
            raise error
        
    def __validate_columns(self) -> bool:
        """Validate the existence of the columns."""
        if (self.state_col_name is not None 
                and self.clients_col_name is not None 
                and self.consumption_col_name is not None):
            return True
        else:
            return False
    
    def __refactor_states(self) -> None:
        """Refactor the state name to the olt."""
        try:
            df = self.report
            df[self.state_col_name] = df[self.state_col_name].apply(
                lambda state: fix_format_word(str(state))
            )
            df[self.state_col_name] = df[self.state_col_name].replace(DISTRIT, "DISTRITO CAPITAL")
            df.sort_values(by=self.state_col_name, ascending=True, inplace=True)
            self.report = df
        except Exception as error:
            raise error
        
    def __delete_columns(self) -> None:
        """Delete the columns that are not necessary."""
        try:
            df = self.report
            col_names = [self.state_col_name, self.clients_col_name, self.consumption_col_name]
            for column in df.columns.to_list():
                if column not in col_names:
                    df.drop(column, axis=1, inplace=True)
            df = df.dropna(how="any", axis=0)
            self.report = df
        except Exception as error:
            raise error
        
    def generate_totals(self) -> pd.DataFrame:
        """Generate the totals of the report.
        
        Returns
        -------
        DataFrame
            A dataframe with the totals of the report.
        """
        try:
            data_states = []
            data_clients = []
            data_consumption = []
            states = self.report[self.state_col_name].unique()
            for state in states:
                df = self.report[self.report[self.state_col_name] == state]
                total_clients = df[self.clients_col_name].sum()
                total_consumption = df[self.consumption_col_name].sum()
                data_states.append(state)
                data_clients.append(total_clients)
                data_consumption.append(round(total_consumption, 2))
            return pd.DataFrame({
                colname.STATE: data_states, 
                colname.CLIENTS: data_clients, 
                colname.CONSUMPTION: data_consumption
            })
        except Exception as error:
            raise error