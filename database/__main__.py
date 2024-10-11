import traceback
from os import getenv
from tqdm import tqdm
from pandas import DataFrame
from dotenv import load_dotenv
from common.utils.file import File
from updater.update import UpdateController

load_dotenv(override=True)

MASTERNODO = getenv("MASTERNODO_PATH")
UpdateDatabase = UpdateController()

def read_update_file() -> DataFrame:
    if MASTERNODO:
        df = File.read_excel(MASTERNODO)
        if df.empty: raise Exception("Data not found")
        return df
    else: raise Exception("There is no file to update")

if __name__ == "__main__":
    try:
        df = read_update_file()
        if UpdateDatabase.get_columns_name_by_data(df):
            df = UpdateDatabase.get_data(df)
            df = UpdateDatabase.fix_data(df)
            nodes = UpdateDatabase.create_new_nodos(df)
            if not nodes: tqdm.write("There are no new nodes")
            else:
                updated_db = UpdateDatabase.save_new_nodes(nodes)
                tqdm.write(f"The database was updated with {updated_db} nodes")
            UpdateDatabase.export_missing_nodes()
    except Exception as error:
        traceback.print_exc()
