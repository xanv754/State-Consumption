import pandas as pd
from common import colname
from measurement.constant import column, interface as INTERFACE
from measurement.lib.refactor import refactor_bras_name

class ExternalConsumption:
    data: pd.DataFrame
    err: bool = False
    bras_col_name: str | None = None
    consumption_col_name: str | None = None

    def __init__(self, df: pd.DataFrame):
        self.data = df
        self.__set_colnames()
        self.__refactor_data()
        self.__refactor_bras_name()
        self.__get_total_data()

    def __set_colnames(self) -> None:
        """Define column names of the data"""
        try:
            for name in self.data.columns.to_list():
                if name in column.BRAS and self.bras_col_name is None:
                    self.bras_col_name = name
                elif name in column.BRAS and self.bras_col_name is not None:
                    raise Exception(
                        f"There are two columns related to «Agregador» in its name"
                    )
                if name in column.CONSUMPTION and self.consumption_col_name is None:
                    self.consumption_col_name = name
                elif name in column.CONSUMPTION and self.consumption_col_name is not None:
                    raise Exception(
                        f"There are two columns related to «Consumo» in its name"
                    )
            if self.bras_col_name is None and self.consumption_col_name is None:
                raise Exception("Column with the bras and consumption data not found")
            elif self.bras_col_name is None:
                raise Exception("Column with the bras data not found")
            elif self.consumption_col_name is None:
                raise Exception("Column with the consumption data not found")
        except Exception as error:
            raise error

    def __refactor_data(self) -> None:
        """Refactor the data to the format required."""
        try:
            for colname in self.data.columns.to_list():
                if (not colname == self.bras_col_name
                        and not colname == self.consumption_col_name):
                    self.data.pop(colname)
            self.data = self.data.sort_values(by=self.bras_col_name, ascending=True)
        except Exception as error:    
            raise error
        
    def __refactor_bras_name(self) -> None:
        """Refactor the bras name to the format required."""
        try:
            self.data[self.bras_col_name] = self.data[self.bras_col_name].apply(
                lambda bras: refactor_bras_name(str(bras))
            )
        except Exception as error:
            raise error
    
    def __get_total_data(self) -> None:
        """Get the total data of the consumption."""
        try:
            total_data = []
            bras = self.data[self.bras_col_name].unique()
            for bras_name in bras:
                total_data.append(self.__get_total_consumption(bras_name))
            data = {colname.BRAS: bras, INTERFACE.IN: total_data}
            self.data = pd.DataFrame(data)
            self.data = self.data.sort_values(by=colname.BRAS, ascending=True)
        except Exception as error:
            raise error
        
    def __get_total_consumption(self, bras_name: str) -> float:
        """Get the total consumption of a bras."""
        try:
            df = self.data[self.data[self.bras_col_name] == bras_name]
            total_consumption = df[self.consumption_col_name].sum()
            return total_consumption
        except Exception as error:
            raise error