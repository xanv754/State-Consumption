import json
import pandas as pd
from typing import List
from database.constants.fields import NodesFieldCollection
from database.model.node import NodeModel
from database.querys.nodes import NodesQueryMongo
from database.utils.header import HeaderUpdater
from utils.format import FixFormat


class UpdaterDatabase:
    """Class to update the database."""
    header: HeaderUpdater = HeaderUpdater()
    data: pd.DataFrame

    def __init__(self, filepath: str, delimiter: str = ";") -> None:
        try:
            if filepath.endswith(".xlsx"): data = pd.read_excel(filepath)
            else: data = pd.read_csv(filepath, delimiter=delimiter)
            data.columns = [FixFormat.word(column) for column in data.columns]
            valida_data = self.header.validate(data.columns.to_list())
            if valida_data:
                self.data = data
            else:
                raise ValueError("The data header does not contain all the columns required to update the database. Please refer to the documentation for details of the required columns")
        except Exception as error:
            print(f"Error in: {__file__}\n {error}")
            exit(1)

    def __data_with_account_code(self) -> None:
        """Filter the data to get only the data with account code."""
        column_account_code = self.header.get_account_code_column(self.data.columns.to_list())
        self.data = self.data[self.data[column_account_code].notna()]

    def __data_with_state(self) -> None:
        """Filter the data to get only the data with state."""
        column_state = self.header.get_state_column(self.data.columns.to_list())
        self.data = self.data[self.data[column_state].notna()]

    def __data_with_central(self) -> None:
        """Filter the data to get only the data with central."""
        column_central = self.header.get_central_column(self.data.columns.to_list())
        self.data = self.data[self.data[column_central].notna()]

    def __get_data_required(self) -> None:
        """Get the data required to update the database."""
        column_state = self.header.get_state_column(self.data.columns.to_list())
        column_central = self.header.get_central_column(self.data.columns.to_list())
        column_account_code = self.header.get_account_code_column(self.data.columns.to_list())
        columns_required = [column_state, column_central, column_account_code]
        if "IP" in self.data.columns.to_list(): 
            columns_required.append("IP")
        else:
            self.data["IP"] = None
            columns_required.append("IP")
        if "REGION" in self.data.columns.to_list(): 
            columns_required.append("REGION")
        else:
            self.data["REGION"] = None
            columns_required.append("REGION")
        data = self.data[columns_required]
        data = data.drop_duplicates()
        data = data.reset_index(drop=True)
        data = data.sort_values(by=[column_state])
        self.data = data

    def __fix_columns(self) -> None:
        """Fix data of the columns required."""
        column_state = self.header.get_state_column(self.data.columns.to_list())
        column_central = self.header.get_central_column(self.data.columns.to_list())
        df_fixed = FixFormat.column_word(self.data, column_state)
        df_fixed = FixFormat.column_word(df_fixed, column_central)
        if "IP" in self.data.columns.to_list():
            df_fixed["IP"] = df_fixed["IP"].apply(lambda x: FixFormat.ip(x))
        if "REGION" in self.data.columns.to_list():
            df_fixed = FixFormat.column_word(df_fixed, "REGION")
        self.data = df_fixed

    def __rename_columns(self) -> None:
        """Rename the columns of the data."""
        column_state = self.header.get_state_column(self.data.columns.to_list())
        column_central = self.header.get_central_column(self.data.columns.to_list())
        column_account_code = self.header.get_account_code_column(self.data.columns.to_list())
        self.data.rename(
            columns={
                column_state: NodesFieldCollection.STATE,
                column_central: NodesFieldCollection.CENTRAL,
                column_account_code: NodesFieldCollection.ACCOUNT_CODE,
                "IP": NodesFieldCollection.IP,
                "REGION": NodesFieldCollection.REGION
            },
            inplace=True
        )
   
    def __convert_node_model(self) -> List[NodeModel]:
        """Convert the JSON to NodeModel."""
        self.data[NodesFieldCollection.ID] = None
        data_json = self.data.to_json(orient="records")
        data_json = data_json.replace("[", "")
        data_json = data_json.replace("]", ",")
        data_json = data_json.split("},")
        nodes: List[NodeModel] = []
        for data in data_json:
            if not data: continue
            data = data + "}"
            data = json.loads(data)
            nodes.append(NodeModel(**data))
        return nodes
    
    def update(self) -> bool:
        """Update the database."""
        self.__data_with_account_code()
        self.__data_with_state()
        self.__data_with_central()
        self.__get_data_required()
        self.__fix_columns()
        self.__rename_columns()
        nodes = self.__convert_node_model()
        return NodesQueryMongo.insert_many(nodes)