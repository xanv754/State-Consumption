from pandas import DataFrame
from os import getenv
from dotenv import load_dotenv
from common.utils.file import File

load_dotenv(override=True)

REPORT_BOSS = getenv("REPORTBOSS_PATH")
DATA_CLIENTS = "cruce_clientes_por_bras.xlsx"
NEW_REPORT_BOSS = "reporte_boss_save.xlsx"
DATA_PORCENTAJE = "cruce_porcentaje.xlsx"

def load_report_boss() -> DataFrame:
    try:
        if ".xlsx" in REPORT_BOSS: 
            df = File.read_excel(REPORT_BOSS)
            if df.empty: raise Exception("Report boss data not found")
            return df
        else: raise Exception("Report boss file not found")
    except Exception as error:
        raise error
    
def save_data_clients(data: DataFrame) -> None:
    try:
        File.write_excel(data, filename=DATA_CLIENTS)
    except Exception as error:
        raise error
    
def save_new_report_boss(data: DataFrame) -> None:
    try:
        File.write_excel(data, filename=NEW_REPORT_BOSS)
    except Exception as error:
        raise error
    
def save_data_porcentage(data: DataFrame) -> None:
    try:
        File.write_excel(data, filename=DATA_PORCENTAJE)
    except Exception as error:  
        raise error