import pandas as pd
from common.constant import exception, exportname, filename, states
from common.utils.fix import fix_column_word, fix_format_word, fix_ip
from common.utils.export import export_missing_nodes
from database import NodeEntity, columns

class MasternodeController:
    """Node driver for database updates.

    Attributes
    ----------
    validate: bool, default False
        Variable private to know if the data has been loaded correctly.
    data: DataFrame
        Dataframe with the original masternodo .xslx.
    data_nodes: list[Node]
        List of nodes to be saved in the database.
    missing_nodes: list[dict]
        List of missing nodes to be exported and fixed.
    central_col_name: str | None
        Name of the column with the central data in the masternodo .xlsx.
    state_col_name: str | None
        Name of the column with the state data in the masternodo .xlsx.
    ip_col_name: str | None
        Name of the column with the ip data in the masternodo .xlsx.
    account_code_col_name: str | None
        Name of the column with the account code data in the masternodo .xlsx.
    region_col_name: str | None
        Name of the column with the region data in the masternodo .xlsx.
    """
    _validate: bool = False
    data: pd.DataFrame
    data_nodes: list[NodeEntity] = []
    missing_nodes: list[dict] = []
    central_col_name: str | None = None
    state_col_name: str | None = None
    ip_col_name: str | None = None
    account_code_col_name: str | None = None
    region_col_name: str | None = None

    def __init__(self, df: pd.DataFrame):
        validate = self.__get_columns_name(df)
        if validate:
            new_df = self.__formatter_data(df)
            if not new_df.empty:
                self.data = new_df
                self.__create_new_nodes()
                self.__export_missing_nodes()
                self._validate = True

    def __add_missing_nodes(self, index: int, central: str) -> None:
        """Add a node to be exported and fixed."""
        node = {exportname.INDEX: index + 2, exportname.CENTRAL: central}
        self.missing_nodes.append(node)

    def __export_missing_nodes(self) -> None:
        """Exports the missing nodes to a .xlsx file."""
        try:
            if len(self.missing_nodes) > 0:
                export_missing_nodes(self.missing_nodes, filename.MISSING_NODES)
        except Exception as error:
            raise error

    def __get_columns_name(self, df: pd.DataFrame) -> bool:
        """Returns the current required names of the columns in the dataframe."""
        try:
            columns_name = df.columns.tolist()
            for name in columns_name:
                # Required Columns
                if (
                    self.central_col_name is None
                    and name in columns.NODE
                    or name in columns.CENTRAL
                ):
                    self.central_col_name = name
                elif self.central_col_name is not None:
                    raise Exception(
                        f"There are two columns related to «Nodo» or «Central» in its name"
                    )
                if self.state_col_name is None and name in columns.STATE:
                    self.state_col_name = name
                elif self.state_col_name is not None:
                    raise Exception(
                        f"There are two columns related to the «Estado» in its name"
                    )
                if self.account_code_col_name is None and name in columns.ACCOUNT_CODE:
                    self.account_code_col_name = name
                elif self.account_code_col_name is not None:
                    raise Exception(
                        f"There are two columns related to the «Codigo Contable» in its name"
                    )
                # Optional Columns
                if self.ip_col_name is None and name in columns.IP:
                    self.ip_col_name = name
                if self.region_col_name is None and name in columns.REGION:
                    self.region_col_name = name
            # Validation of the existence of all required columns
            if not self.central_col_name:
                raise Exception("Central column not found")
            if not self.state_col_name:
                raise Exception("State column not found")
            if not self.account_code_col_name:
                raise Exception("Account code column not found")
        except Exception as error:
            raise error
        else:
            return True

    def __create_new_nodes(self) -> None:
        """Creates new node models from previously loaded data."""
        try:
            for index, row in self.data.iterrows():
                node_accepted = True
                if self.central_col_name is not None:
                    current_central = str(row[self.central_col_name]).upper()
                    current_central = fix_format_word(current_central)
                else:
                    self.__add_missing_nodes(index, "not found")
                    node_accepted = False
                if node_accepted and self.state_col_name is not None:
                    current_state = str(row[self.state_col_name]).capitalize()
                    # Exception
                    if current_state and current_state in exception.ZONE:
                        current_state = states.DISTRITO_CAPITAL
                    current_state = fix_format_word(current_state)
                else:
                    self.__add_missing_nodes(index, row[self.central_col_name])
                    node_accepted = False
                if node_accepted and self.account_code_col_name is not None:
                    current_account_code = str(row[self.account_code_col_name])
                else:
                    self.__add_missing_nodes(index, row[self.central_col_name])
                    node_accepted = False
                if node_accepted and self.ip_col_name is not None:
                    if type(row[self.ip_col_name]) == int:
                        current_ip = fix_ip(current_ip)
                    else:
                        current_ip = str(row[self.ip_col_name])
                else:
                    current_ip = None
                if node_accepted and self.region_col_name is not None:
                    current_region = str(row[self.region_col_name])
                    current_region = fix_format_word(current_region)
                else:
                    current_region = None

                if node_accepted:
                    new_node = NodeEntity(
                        state=current_state,
                        central=current_central,
                        ip=current_ip,
                        account_code=current_account_code,
                        region=current_region,
                    )
                    self.data_nodes.append(new_node)
        except Exception as error:
            raise error

    def __formatter_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Data formatter to get only the necessary data and fixed."""
        try:
            columns_name = df.columns.tolist()
            for name in columns_name:
                if ((name != self.central_col_name)
                        and (name != self.state_col_name)
                        and (name != self.ip_col_name)
                        and (name != self.account_code_col_name)
                        and (name != self.region_col_name)):
                    df.pop(name)
            df = df.sort_values(by=self.state_col_name, ascending=True)
            df = fix_column_word(df, self.central_col_name)
            return df
        except Exception as error:
            raise error

