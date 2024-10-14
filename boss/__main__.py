import traceback
import pandas as pd
from os import getenv
from tqdm import tqdm
from dotenv import load_dotenv
from common.utils.file import File
from common.utils.export import export_missing_nodes
from common.constant.columns import ReportColumns
from database.query.find import find_node_by_account_code
from database.entity.node import Node
from clients.clients import TableController

load_dotenv(override=True)

NEW_REPORT_BOSS = "reporte_boss_save.xlsx"
DATA_CLIENTS = "cruce_clientes_por_bras.xlsx"

REPORT_BOSS = getenv("REPORTBOSS_PATH")

class ReportBossController:
    report: pd.DataFrame
    states: dict

    def __init__(self):
        self.report = pd.DataFrame()
        self.states = {}

    def __search_state(self, account_code: str) -> str:
        try:
            if account_code in self.states.keys(): return self.states[account_code]
            else:
                res: list[Node] = find_node_by_account_code(account_code)
                if len(res) <= 0: return None
                elif len(res) == 1: 
                    self.states[account_code] = res[0].state
                    return res[0].state
                else:
                    # Exceptions:
                    states = []
                    for node in res:
                        if node.state not in states: states.append(node.state)
                    return states[0]
                    # if len(states) == 2:
                    #     if "DISTRITO CAPITAL" in states:
                    #         for state in states:
                    #             if state != "DISTRITO CAPITAL": return state
                    # return None
        except Exception as error:
            raise error

    def add_state(self) -> None:
        try:
            df = self.report
            missing_nodes = []
            if ReportColumns.CENTRAL in df.columns.tolist():
                df.insert(len(df.columns.to_list()), "Estado", "")
                df.insert(len(df.columns.to_list()), "bras", "")
                tqdm.write("Adding detail to the report...")
                for index, row in tqdm(df.iterrows(), total=df.shape[0]):
                    state = self.__search_state(str(row[ReportColumns.ACCOUNT_CODE]))
                    if state:
                        df.iloc[index, df.columns.get_loc("Estado")] = state
                        df.iloc[index, df.columns.get_loc("bras")] = str(row[ReportColumns.ACRONYM_BRAS]) + '-' + str(row[ReportColumns.BRAS])
                    else:
                        missing_nodes.append({
                            "Indice": index + 2, 
                            "Central": row[ReportColumns.CENTRAL], 
                            "Account Code": row[ReportColumns.ACCOUNT_CODE], 
                            "BRAS": str(row[ReportColumns.ACRONYM_BRAS]) + '-' + str(row[ReportColumns.BRAS])
                        })
                if len(missing_nodes) > 0:
                    export_missing_nodes(missing_nodes) 
                    return
                self.report = df
            else: raise Exception(f"Column with the central data ({ReportColumns.CENTRAL}) not found")
        except Exception as error:
            raise error
        
    def validate_state_column(self) -> bool:
        try:
            columns = self.report.columns.tolist()
            if "Estado" in columns or "ESTADO" in columns or "estado" in columns: return True
            else: return False
        except Exception as error:
            raise error

if __name__ == "__main__":
    try:
        ReportController = ReportBossController()
        if REPORT_BOSS:
            if ".xlsx" in REPORT_BOSS: ReportController.report = File.read_excel(REPORT_BOSS)
            if not ReportController.report.empty:
                if not ReportController.validate_state_column():
                    ReportController.add_state()
                if not ReportController.report.empty:
                    df_clients = TableController.create_usage_for_bras_by_state(ReportController.report)
                    if df_clients.empty: raise Exception("Nodes without state exist")
                    df_clients = TableController.add_total_sum_by_bras(df_clients)
                    df_clients = TableController.add_total_sum_by_state(df_clients)
                    File.write_excel(df_clients, filename=DATA_CLIENTS)
            else: raise Exception("No data from the report boss")
        else: raise Exception("Report boss file not found")
    except Exception as error:
        traceback.print_exc()
