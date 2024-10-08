import traceback
from os import getenv
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from common.utils.file import File
from entity.node import Node
from query.insert import insert_new_nodes
from query.find import find_node

load_dotenv(override=True)

MASTERNODO = getenv("MASTERNODO_PATH")

class DatabaseController:
    central_col_name: (str | None) = None
    state_col_name: (str | None) = None
    ip_col_name: (str | None) = None
    account_code_col_name: (str | None) = None

    def get_columns_name_by_data(self, df: pd.DataFrame) -> bool:
        try:
            columns_name = df.columns.tolist()
            for name in columns_name:
                if ('Estado' in name or 'estado' in name) and self.state_col_name is None: self.state_col_name = name
                elif ('Estado' in name or 'estado' in name) and (not self.state_col_name is None): raise Exception(f"There are two columns related to the «Estado» in its name")
                if ('Nodo' in name or 'nodo' in name) and self.central_col_name is None: self.central_col_name = name
                elif ('Nodo' in name or 'nodo' in name) and (not self.central_col_name is None): raise Exception(f"There are two columns related to «Nodo» in its name")
                if ('IP' in name or 'ip' in name) and self.ip_col_name is None: self.ip_col_name = name
                elif ('IP' in name or 'ip' in name) and (not self.ip_col_name is None): raise Exception(f"There are two columns related to «IP» in its name")
                if ('Codigo' in name or 'codigo' in name) and self.account_code_col_name is None: self.account_code_col_name = name
                elif ('Codigo' in name or 'codigo' in name) and (not self.account_code_col_name is None): raise Exception(f"There are two columns related to «Codigo» in its name")
        except Exception as error:
            raise error
        else:
            return True
        
    def get_data_by_columns_name(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            columns_name = df.columns.tolist()
            for name in columns_name:
                if (name != self.central_col_name) and (name != self.state_col_name) and (name != self.ip_col_name) and (name != self.account_code_col_name): df.pop(name)
            df = df.sort_values(by=self.state_col_name, ascending=True)
            return df
        except Exception as error:
            raise error
        
    def create_new_nodos(self, df: pd.DataFrame) -> list[Node]:
        if not df.empty:
            try:
                nodes: list[Node] = []
                for _index, row in df.iterrows():
                    current_state = str(row[self.state_col_name])
                    current_central = str(row[self.central_col_name])
                    current_ip = str(row[self.ip_col_name])
                    current_account_code = str(row[self.account_code_col_name])
                    new_node = Node(state=current_state, central=current_central, ip=current_ip, account_code=current_account_code)
                    nodes.append(new_node)
                return nodes
            except Exception as error:
                raise error
        else: raise Exception("Data empty")

    def save_new_nodes(self, nodes: list[Node]) -> int:
        try:
            if (nodes):
                new_nodes: list[Node] = []
                tqdm.write(f"Validating nodes exist in the database...")
                for node in tqdm(nodes):
                    if not find_node(node.state, node.central): new_nodes.append(node)
                if new_nodes: 
                    tqdm.write(f"Saving {len(new_nodes)} new nodes...")
                    res = insert_new_nodes(new_nodes)
                    if res and res.acknowledged: return len(new_nodes)
            return 0
        except Exception as error:
            raise error

if __name__ == "__main__":
    try:
        UploadDatabase = DatabaseController()
        if (MASTERNODO):
            df = File.read_excel(MASTERNODO, sheetname="master")
            if df.empty == False:
                if UploadDatabase.get_columns_name_by_data(df):
                    df = UploadDatabase.get_data_by_columns_name(df)
                    nodes = UploadDatabase.create_new_nodos(df)
                    updated_db = UploadDatabase.save_new_nodes(nodes)
                    if updated_db > 0: tqdm.write(f"The database was updated with {updated_db} nodes")
                    else: tqdm.write("There are no new nodes")
                else: raise Exception("There are not columns related to «Nodes» or «State»")
            else: raise Exception("Data not found")
        else: raise Exception("There is no file to update")
    except Exception as error:
        traceback.print_exc()        
