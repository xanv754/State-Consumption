import pandas as pd
from tqdm import tqdm
from common import colname, exportname, FileController, transform_states, export_missing_nodes
from database import NodeEntity, find_node_by_account_code
from boss.constant import columns as colboss, equipment as EQUIPMENT
from boss.lib.data import save_new_report_boss, save_report_by_equipment

class ReportBossController:
    validate: bool = False
    report: pd.DataFrame
    states: dict
    data_adsl: pd.DataFrame
    data_mdu: pd.DataFrame

    def __init__(self, filename: str, process: bool = False, equipment: str = "all"):
        df = FileController.read_excel(filename)
        if not df.empty:
            self.report = df
            self.states = {}
            self.__add_complete_bras()
            colname_state = self.__validate_state_column()
            if not colname_state:
                self.validate = self.__add_state()
                if self.validate: 
                    self.__define_provider()
                    if process: 
                        save_new_report_boss(self.report)
                        if equipment == "all": save_report_by_equipment(self.data_adsl, self.data_mdu)
                        elif equipment == "adsl": save_report_by_equipment(data_adsl=self.data_adsl)
                        elif equipment == "mdu": save_report_by_equipment(data_mdu=self.data_mdu)
            else:
                self.__refactor_state_name(colname_state)
                self.__define_provider()
                if process and equipment == "all": save_report_by_equipment(self.data_adsl, self.data_mdu)
                elif process and equipment == "adsl": save_report_by_equipment(data_adsl=self.data_adsl)
                elif process and equipment == "mdu": save_report_by_equipment(data_mdu=self.data_mdu)    
                self.validate = True

    
    def __define_provider(self) -> None:
        """Define the data that is ADSL and the data that is MDU."""
        try:
            df_mdu = pd.DataFrame()
            df_adsl = pd.DataFrame()
            equipments = self.report[colboss.EQUIPMENT].unique()
            for equipment in tqdm(equipments, desc="Recognising equipment..."):
                df_filtered = self.report[self.report[colboss.EQUIPMENT] == equipment]
                if equipment in EQUIPMENT.MDU:
                    df_mdu = pd.concat([df_mdu, df_filtered], axis=0)
                else:
                    df_adsl = pd.concat([df_adsl, df_filtered], axis=0)
            self.data_adsl = df_adsl
            self.data_mdu = df_mdu
        except Exception as error:
            raise error

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
                for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Adding state to report..."):
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
            for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Adding complete bras name to report..."):
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