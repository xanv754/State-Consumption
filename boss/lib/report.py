import pandas as pd
from tqdm import tqdm
from boss import colboss
from boss import load_report_boss, save_new_report_boss
from common.constant import colname, exportname
from common.utils.transform import transform_states
from common.utils.export import export_missing_nodes
from database import NodeEntity
from database import find_node_by_account_code

class ReportBossController:
    validate: bool = False
    report: pd.DataFrame
    states: dict

    def __init__(self):
        df = load_report_boss()
        if not df.empty:
            self.report = df
            self.states = {}
            self.__add_complete_bras()
            colname_state = self.__validate_state_column()
            if not colname_state:
                self.validate = self.__add_state()
                if self.validate: save_new_report_boss(self.report)
            else:
                self.__refactor_state_name(colname_state)
                self.validate = True

    def __validate_state_column(self) -> (str | None):
        """Checks for the presence of the 'Estado' column within the data frame."""
        try:
            for column in self.report.columns.tolist():
                if column in colboss.STATE: return column
            return None
        except Exception as error:
            raise error

    def __search_state(self, account_code: str) -> str:
        """Find the corresponding status in the database. Use the accounting code."""
        try:
            if account_code in self.states.keys():
                return self.states[account_code]
            else:
                res: list[NodeEntity] = find_node_by_account_code(account_code)
                if len(res) <= 0: return None
                elif len(res) == 1:
                    self.states[account_code] = res[0].state
                    return res[0].state
                else:
                    # Exceptions:
                    states = []
                    for node in res:
                        if node.state not in states:
                            states.append(node.state)
                    return states[0]
        except Exception as error:
            raise error

    def __add_state(self) -> bool:
        """Add the state to the node."""
        try:
            df = self.report
            missing_nodes = []
            if colboss.CENTRAL in df.columns.tolist():
                df.insert(len(df.columns.to_list()), colname.STATE, "")
                for index, row in tqdm(df.iterrows(), total=df.shape[0]):
                    state = self.__search_state(str(row[colboss.ACCOUNT_CODE]))
                    if state:
                        df.iloc[index, df.columns.get_loc(colname.STATE)] = state
                    else:
                        missing_nodes.append(
                            {
                                exportname.INDEX: index + 2,
                                exportname.CENTRAL: row[colboss.CENTRAL],
                                exportname.ACCOUNT_CODE: row[colboss.ACCOUNT_CODE],
                                exportname.BRAS: str(row[colboss.ACRONYM_BRAS])
                                + "-"
                                + str(row[colboss.BRAS]),
                            }
                        )
                if len(missing_nodes) > 0:
                    export_missing_nodes(missing_nodes)
                    return False
                else:
                    self.report = df
                    return True
            else:
                raise Exception(
                    f"Column with the central data ({colboss.CENTRAL}) not found"
                )
        except Exception as error:
            raise error

    def __add_complete_bras(self) -> None:
        """Add the complete bras name to the node."""
        try:
            df = self.report
            df.insert(len(df.columns.to_list()), colname.BRAS, "")
            for index, row in tqdm(df.iterrows(), total=df.shape[0]):
                df.iloc[index, df.columns.get_loc(colname.BRAS)] = (
                    str(row[colboss.ACRONYM_BRAS])
                    + "-"
                    + str(row[colboss.BRAS])
                )
            self.report = df
        except Exception as error:
            raise error
    
    def __refactor_state_name(self, colname_state: str) -> None:
        """Refactor the state name to the node."""
        try:
            df = self.report
            df[colname_state] = df[colname_state].apply(
                lambda state: transform_states(str(state))
            )
            df = df.rename(columns={colname_state:colname.STATE})
            self.report = df
        except Exception as error:
            raise error