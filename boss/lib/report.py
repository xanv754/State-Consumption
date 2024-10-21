import pandas as pd
from tqdm import tqdm
from common.constant import export as EXPORT
from common.utils.export import export_missing_nodes
from common.utils.transform import transform_states
from database.query.find import find_node_by_account_code
from database.entity.node import Node
from boss.lib.load import load_report_boss, save_new_report_boss
from boss.constant import columns as COLUMNS


class ReportBossController:
    validate: bool = False
    report: pd.DataFrame
    states: dict

    def __init__(self):
        df = load_report_boss()
        if not df.empty:
            self.report = df
            self.states = {}
            if not self.__validate_state_column():
                self.validate = self.__add_state()
                if self.validate:
                    save_new_report_boss(self.report)
            else:
                self.validate = True

    def __search_state(self, account_code: str) -> str:
        try:
            if account_code in self.states.keys():
                return self.states[account_code]
            else:
                res: list[Node] = find_node_by_account_code(account_code)
                if len(res) <= 0:
                    return None
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

    def __validate_state_column(self) -> bool:
        try:
            columns = self.report.columns.tolist()
            if columns in COLUMNS.STATE:
                return True
            else:
                return False
        except Exception as error:
            raise error

    def __add_state(self) -> bool:
        try:
            df = self.report
            missing_nodes = []
            if (
                COLUMNS.CENTRAL in df.columns.tolist()
                and not COLUMNS.NEW_STATE in df.columns.to_list()
            ):
                df.insert(len(df.columns.to_list()), COLUMNS.NEW_STATE, "")
                df.insert(len(df.columns.to_list()), COLUMNS.NEW_BRAS, "")
                for index, row in tqdm(df.iterrows(), total=df.shape[0]):
                    state = self.__search_state(str(row[COLUMNS.ACCOUNT_CODE]))
                    if state:
                        df.iloc[index, df.columns.get_loc(COLUMNS.NEW_STATE)] = state
                        df.iloc[index, df.columns.get_loc(COLUMNS.NEW_BRAS)] = (
                            str(row[COLUMNS.ACRONYM_BRAS])
                            + "-"
                            + str(row[COLUMNS.BRAS])
                        )
                    else:
                        missing_nodes.append(
                            {
                                EXPORT.INDEX: index + 2,
                                EXPORT.CENTRAL: row[COLUMNS.CENTRAL],
                                EXPORT.ACCOUNT_CODE: row[COLUMNS.ACCOUNT_CODE],
                                EXPORT.BRAS: str(row[COLUMNS.ACRONYM_BRAS])
                                + "-"
                                + str(row[COLUMNS.BRAS]),
                            }
                        )
                if len(missing_nodes) > 0:
                    export_missing_nodes(missing_nodes)
                    return False
                self.report = df
                return True
            elif (
                COLUMNS.CENTRAL in df.columns.tolist()
                and COLUMNS.NEW_STATE in df.columns.to_list()
            ):
                df[COLUMNS.NEW_STATE] = df[COLUMNS.NEW_STATE].apply(
                    lambda state: transform_states(str(state))
                )
                df.insert(len(df.columns.to_list()), COLUMNS.NEW_BRAS, "")
                for index, row in tqdm(df.iterrows(), total=df.shape[0]):
                    df.iloc[index, df.columns.get_loc(COLUMNS.NEW_BRAS)] = (
                        str(row[COLUMNS.ACRONYM_BRAS]) + "-" + str(row[COLUMNS.BRAS])
                    )
                self.report = df
                return True
            else:
                raise Exception(
                    f"Column with the central data ({COLUMNS.CENTRAL}) not found"
                )
        except Exception as error:
            raise error
