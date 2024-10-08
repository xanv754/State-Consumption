from os import getenv
import traceback
from dotenv import load_dotenv
from tqdm import tqdm
import pandas as pd
import numpy as np
from database.query.find import find_node_by_central
from common.constant.columns import ColumnsReport
from common.utils.file import File

load_dotenv(override=True)

REPORT_BOSS = getenv("REPORTBOSS_PATH")

class ReportBossController:
    def add_state(self, df: pd.DataFrame):
        try:
            if ColumnsReport.CENTRAL in df.columns.tolist():
                df["Estado"] = str(np.nan)
                df["IP-nodo"] = str(np.nan)
                df["bras"] = str(np.nan)
                tqdm.write("Agregando detalles al reporte..")
                for index, row in tqdm(df.iterrows(), total=df.shape[0]):
                    res = find_node_by_central(row[ColumnsReport.CENTRAL], row[ColumnsReport.ACCOUNT_CODE])
                    if res:
                        df.loc[index, "Estado"] = res.state
                        df.loc[index, "IP-nodo"] = res.ip
                    else:
                        df.loc[index, "Estado"] = np.nan
                        df.loc[index, "IP-nodo"] = np.nan
                    df.loc[index, "bras"] = str(row[ColumnsReport.ACRONYM_BRAS]) + '-' + str(row[ColumnsReport.BRAS])
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
                File.write_excel(df)
            else: raise Exception("No data from the report boss")
        else: raise Exception("Report boss file not found")
    except Exception as error:
        traceback.print_exc()
