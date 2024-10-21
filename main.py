import traceback
import pandas as pd
from typing import List
from tqdm import tqdm
from boss.lib.clients import ClientController
from boss.constant import columns as COLUMNS
from common.constant import file as FILE
from common.utils.file import File
from common.constant import bras as BRAS
from common.constant.states import states
from measurement.constant import interface as INTERFACE


PORCENTAGE = FILE.PORCENTAGE
MEASUREMENT = FILE.MEASUREMENT

def create_consumption_by_bras():
    try:
        df_porcentage = File.read_excel(PORCENTAGE)
        df_measurement = File.read_excel(MEASUREMENT)
        df_porcentage = df_porcentage.drop(df_porcentage.index[-1])
        df = pd.DataFrame({COLUMNS.NEW_STATE: states})
        if not df_porcentage.empty and not df_measurement.empty:
            for _index, row in tqdm(df_measurement.iterrows(), total=df_measurement.shape[0]):
                current_bras = str(row[BRAS.NAME]).lower()
                if current_bras in df_porcentage.columns.to_list():
                    total = row[INTERFACE.IN]
                    porcentage = df_porcentage[current_bras]
                    new_values: List[float] = []
                    for value in porcentage:
                        # new_porcentage = value * total
                        # new_values.append(round(new_porcentage, 2))
                        new_values.append(value * total)
                    df[current_bras] = new_values
        ClientController.add_total_sum_by_bras(df)
        ClientController.add_total_sum_by_state(df)
        total_porcentage = df[COLUMNS.TOTAL_BY_STATE]
        total = total_porcentage[len(total_porcentage) - 1]
        total_porcentage = total_porcentage[:-1]
        new_values: List[float] = []
        for value in total_porcentage:
            new_values.append(value / total * 100)
        df[COLUMNS.TOTAL_BY_USAGE] = new_values
        File.write_excel(df, filename=FILE.CONSUMPTION_BY_BRAS)
    except Exception as error:
        raise error
if __name__ == "__main__":
    try:
        create_consumption_by_bras()
    except:
        traceback.print_exc()