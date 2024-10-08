from tqdm import tqdm
from os import getcwd
import pandas as pd
import traceback

class File:

    @staticmethod
    def read_csv(path: str, delimiter: str = ",") -> pd.DataFrame:
        try:
            tqdm.write("Loading file...")
            return pd.read_csv(path, delimiter=delimiter, encoding="latin-1", low_memory=False)
        except Exception as error:
            return pd.DataFrame()
    
    @staticmethod
    def read_excel(path: str, sheetname: (str | None)) -> pd.DataFrame:
        try:
            tqdm.write("Loading file...")
            if not sheetname: return pd.read_excel(path, index_col=None)
            else: return pd.read_excel(path, index_col=None, sheet_name=sheetname)
        except Exception as error:
            return pd.DataFrame()
    
    @staticmethod
    def write_excel(df: pd.DataFrame) -> None:
        try:
            pwd = getcwd()
            path = f"{pwd}/reporte_boss_save.xlsx"
            if not df.empty:
                tqdm.write("Save data a file .xlsx ...")
                if len(df) < 900000:
                    with pd.ExcelWriter(path, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name="Clientes ABA Registro", index=False, freeze_panes=(1,0))
                else:
                    total_records = len(df)
                    number_partitions = []
                    while total_records > 900000:
                        number_partitions.append(900000)
                        total_records -= 900000
                    number_partitions.append(total_records)
                    number_sheet = 1
                    with pd.ExcelWriter(path, engine='openpyxl') as writer:
                        for i in tqdm(number_partitions):
                            df_split = df[:i]
                            df_split.to_excel(writer, sheet_name=f'Hoja {number_sheet}', index=False, freeze_panes=(1,0))
                            df = df[i:]
                            number_sheet += 1
                tqdm.write(f"Saved data in {path}")
            else:
                tqdm.write(f"WARNING: Empty dataframe")
        except:
            traceback.print_exc()