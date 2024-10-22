import traceback
import pandas as pd
from typing import List
from tqdm import tqdm
from common.constant import filename
from common.utils.file import FileController
from common.constant import colname
from common.constant.states import states
from common.utils.totalling import add_total_sum_by_col, add_total_sum_by_row
from measurement.constant import interface as INTERFACE

PORCENTAGE = filename.PORCENTAGE
MEASUREMENT = filename.MEASUREMENT

def create_consumption_by_bras():
    try:
        df_porcentage = FileController.read_excel(PORCENTAGE)
        df_measurement = FileController.read_excel(MEASUREMENT)
        df_porcentage = df_porcentage.drop(df_porcentage.index[-1])
        df = pd.DataFrame({colname.STATE: states})
        if not df_porcentage.empty and not df_measurement.empty:
            for _index, row in tqdm(df_measurement.iterrows(), total=df_measurement.shape[0]):
                current_bras = str(row[colname.BRAS]).lower()
                if current_bras in df_porcentage.columns.to_list():
                    total = row[INTERFACE.IN]
                    porcentage = df_porcentage[current_bras]
                    new_values: List[float] = []
                    for value in porcentage:
                        new_porcentage = value * total
                        new_values.append(round(new_porcentage, 2))
                    df[current_bras] = new_values
        df = add_total_sum_by_col(df, colname.TOTAL_BY_BRAS)
        df = add_total_sum_by_row(df, colname.TOTAL_BY_STATE)
        total_porcentage = df[colname.TOTAL_BY_STATE]
        total = total_porcentage[len(total_porcentage) - 1]
        total_porcentage = total_porcentage[:-1]
        new_values: List[float] = []
        for value in total_porcentage:
            new_values.append(round((value / total * 100), 2))
        new_values.append(sum(new_values))
        df[colname.TOTAL_BY_USAGE] = new_values
        FileController.write_excel(df, filename=filename.CONSUMPTION_BY_BRAS)
    except Exception as error:
        raise error
if __name__ == "__main__":
    try:
        create_consumption_by_bras()
    except:
        traceback.print_exc()