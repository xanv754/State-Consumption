import argparse
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

def update_db() -> None:
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
        raise error
    
def update_node() -> None:
    try:
        UpdateDatabase = UpdateController()
        tqdm.write("Enter the information of the node to be added to the database")
        name_node = str(input("Name node: "))
        state_node = str(input("State node: "))
        account_code_node = str(input("Account code node: "))
        ip_node = str(input("IP node: "))
        region_node = str(input("Region node: "))
        node = UpdateDatabase.create_new_node(name_node, state_node, account_code_node, ip_node, region_node)
        if UpdateDatabase.save_new_node(node): tqdm.write(f"The node {name_node} was updated")
        else: tqdm.write(f"The node {name_node} existed")
    except Exception as error:
        raise error

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Update the database with the masternode file")
        parser.add_argument("-u", "--update", help="Update database with file", action="store_true")
        parser.add_argument("-n", "--node", help="Create new node to the database", action="store_true")

        args = parser.parse_args()

        if args.update: update_db()
        elif args.node: update_node()
        else: 
            tqdm.write("No arguments provided")
            parser.print_help()
    except SystemExit:
        parser.print_help()
    except:
        traceback.print_exc()
