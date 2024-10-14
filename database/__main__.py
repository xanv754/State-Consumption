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
            if not nodes: print("There are no new nodes")
            else:
                updated_db = UpdateDatabase.save_new_nodes(nodes)
                print(f"The database was updated with {updated_db} nodes")
            UpdateDatabase.export_missing_nodes()
    except Exception as error:
        raise error
    
def update_nodo() -> None:
    try:
        print("Enter the information to search node...")
        central = str(input("Central node: "))
        state = str(input("State node: "))
        account_code = str(input("Account code node: "))
        node = UpdateDatabase.search_nodo(account_code, central, state)
        if node:
            id = node.id
            print("Enter the information of the node to be updated to the database")
            print("Current central node: ", node.central)
            central = str(input("New central node [current]: ")).upper()
            if not central: central = node.central
            print("Current state node [current]: ", node.state)
            state = str(input("New state node: ")).upper()
            if not state: state = node.state
            print("Current account code node [current]: ", node.account_code)
            account_code = str(input("New account code node: "))
            if not account_code: account_code = node.account_code
            print("Current IP node [current]: ", node.ip)
            ip = str(input("New IP node: "))
            if not ip: ip = node.ip
            print("Current region node [current]: ", node.region)
            region = str(input("New region node: ")).upper()
            if not region: region = node.region
            new_node = UpdateDatabase.create_new_node(
                central, 
                state, 
                account_code, 
                ip, 
                region
            )
            print("Data of node to be updated:")
            print("Central: ", central)
            print("State: ", state)
            print("Account code: ", account_code)
            print("IP: ", ip)
            print("Region: ", region)
            status = UpdateController.update_nodo(id, new_node)
            if status: print("Node updated")
            else: print("Node not updated")
        else: print("Node not found")
    except Exception as error:
        raise error
    
def create_new_node() -> None:
    try:
        print("Enter the information of the node to be added to the database")
        central = str(input("Central node: "))
        state = str(input("State node: "))
        account_code = str(input("Account code node: "))
        ip = str(input("IP node: "))
        region = str(input("Region node: "))
        node = UpdateDatabase.create_new_node(central, state, account_code, ip, region)
        if UpdateDatabase.save_new_node(node): print(f"The node {central} was updated")
        else: print(f"The node {central} existed")
    except Exception as error:
        raise error

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Update the database with the masternode file")
        parser.add_argument("-d", "--database", help="Update database with file", action="store_true")
        parser.add_argument("-n", "--node", help="Create new node to the database", action="store_true")
        parser.add_argument("-u", "--update", help="Update a node to the database", action="store_true")

        args = parser.parse_args()

        if args.database: update_db()
        elif args.node: create_new_node()
        elif args.update: update_nodo()
        else: 
            print("No arguments provided")
            parser.print_help()
    except SystemExit:
        parser.print_help()
    except:
        traceback.print_exc()
