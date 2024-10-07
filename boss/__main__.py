from tqdm import tqdm
from common.utils.file import File
from common.constant.columns import ColumnsReport
from database.query.find import find_node_by_central
from dotenv import load_dotenv
from os import getenv
import pandas as pd

load_dotenv(override=True)

REPORT_BOSS = getenv("REPORTBOSS_PATH")

class ReportBossController:
    def add_state(self, df: pd.DataFrame):
        try:
            if ColumnsReport.CENTRAL in df.columns.tolist():
                tqdm.write("Agregando detalles al reporte..")
                for _index, row in tqdm(df.iterrows(), total=df.shape[0]):
                    res = find_node_by_central(row[ColumnsReport.CENTRAL])
                    if res:
                        df["State"] = res.state
                        df["IP-node"] = res.ip
                        df["bras"] = row[ColumnsReport.ACRONYM_BRAS] + '-' + row[ColumnsReport.BRAS]
                df.pop(ColumnsReport.ACRONYM_BRAS)
                df.pop(ColumnsReport.BRAS)
                return df
            else: raise Exception(f"Column with the central data ({ColumnsReport.CENTRAL}) not found")
        except Exception as error:
            raise error

if __name__ == "__main__":
    try:
        ReportBoss = ReportBossController()
        if REPORT_BOSS:
            df = pd.DataFrame()
            if ".xlsx" in REPORT_BOSS: df = File.read_excel(REPORT_BOSS)
            if not df.empty:
                df = ReportBoss.add_state(df)
                # TODO: Save df to file .xlsx
                print(df)
            else: raise Exception("No data from the report boss")
        else: raise Exception("Report boss file not found")
    except Exception as error:
        print(error)
