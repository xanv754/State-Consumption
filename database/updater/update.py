import pandas as pd
from tqdm import tqdm
from common.utils.fix import fix_column_word, fix_format_word, fix_ip
from common.utils.export import export_missing_nodes
from entity.node import Node
from query.find import find_node
from query.insert import insert_new_node

class UpdateController:
    central_col_name: (str | None) = None
    state_col_name: (str | None) = None
    ip_col_name: (str | None) = None
    account_code_col_name: (str | None) = None
    region_col_name: (str | None) = None
    missing_nodes: list[dict] = []
    nodes: list[Node] = []

    def _add_missing_nodes(self, index: int, central: str) -> None:
        node = {
            "Indice": index + 2, 
            "Central": central
        }
        self.missing_nodes.append(node)
       
    def fix_data(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            df = fix_column_word(df, self.central_col_name)
            return df
        except Exception as error:  
            raise error

    def get_columns_name_by_data(self, df: pd.DataFrame) -> bool:
        try:
            columns_name = df.columns.tolist()
            for name in columns_name:
                # Required
                if ((('Nodo' in name or 'nodo' in name or 'NODO' in name)
                        or ('Central' in name or 'central' in name or 'CENTRAL' in name)) 
                        and self.central_col_name is None): 
                    self.central_col_name = name
                elif ('Nodo' in name or 'nodo' in name or 'NODO' in name) and (not self.central_col_name is None): 
                    raise Exception(f"There are two columns related to «Nodo» or «Central» in its name")
                if ('Estado' in name or 'estado' in name or 'ESTADO' in name) and self.state_col_name is None: 
                    self.state_col_name = name
                elif ('Estado' in name or 'estado' in name or 'ESTADO' in name) and (not self.state_col_name is None): 
                    raise Exception(f"There are two columns related to the «Estado» in its name")
                if (('Codigo Cont' in name 
                        or 'codigo cont' in name 
                        or 'CODIGO CONT' in name 
                        or 'COD / CONT' in name
                        or 'cod / cont' in name
                        or 'Cod / Cont' in name
                        or 'cc' in name
                        or 'CC' in name) 
                        and self.account_code_col_name is None): 
                    self.account_code_col_name = name
                elif (('Codigo Cont' in name 
                        or 'codigo cont' in name 
                        or 'CODIGO CONT' in name 
                        or 'COD / CONT' in name
                        or 'cod / cont' in name
                        or 'Cod / Cont' in name
                        or 'cc' in name
                        or 'CC' in name) 
                        and (not self.account_code_col_name is None)): 
                    raise Exception(f"There are two columns related to the «Codigo Contable» in its name")
                
                # Optional
                if ('IP' in name or 'ip' in name or 'Ip' in name) and self.ip_col_name is None: 
                    self.ip_col_name = name
                if ('Region' in name or 'region' in name or 'REGION' in name):
                    self.region_col_name = name
                
            # Validation
            if not self.central_col_name: raise Exception("Central column not found")
            if not self.state_col_name: raise Exception("State column not found")
        except Exception as error:
            raise error
        else:
            return True
        
    def get_data(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            columns_name = df.columns.tolist()
            for name in columns_name:
                if ((name != self.central_col_name) 
                        and (name != self.state_col_name) 
                        and (name != self.ip_col_name) 
                        and (name != self.account_code_col_name)
                        and (name != self.region_col_name)):
                    df.pop(name)
            df = df.sort_values(by=self.state_col_name, ascending=True)
            return df
        except Exception as error:
            raise error
        
    def create_new_nodos(self, df: pd.DataFrame) -> list[Node]:
        if not df.empty:
            try:
                nodes: list[Node] = []
                for index, row in df.iterrows():
                    node_accepted = True
                    if self.central_col_name is not None:
                        current_central = str(row[self.central_col_name]).upper()
                        current_central = fix_format_word(current_central)
                    else: 
                        self._add_missing_nodes(index, "not found")
                        node_accepted = False
                    if self.state_col_name is not None:
                        current_state = str(row[self.state_col_name]).capitalize()
                        # Exception
                        if (current_state 
                                and "zona" in current_state 
                                or "ZONA" in current_state 
                                or "Zona" in current_state): 
                            current_state = "Distrito Capital"
                        current_state = fix_format_word(current_state)
                    else: 
                        self._add_missing_nodes(index, row[self.central_col_name])
                        node_accepted = False
                    if node_accepted and self.account_code_col_name is not None:
                            current_account_code = str(row[self.account_code_col_name])
                    else: 
                        self._add_missing_nodes(index, row[self.central_col_name])
                        node_accepted = False

                    if node_accepted and self.ip_col_name is not None:
                        if type(row[self.ip_col_name]) == int:
                            current_ip = fix_ip(current_ip)
                        else:
                            current_ip = str(row[self.ip_col_name])
                    else: 
                        current_ip = None
                    if node_accepted and self.region_col_name is not None:
                        current_region = str(row[self.region_col_name])
                        current_region = fix_format_word(current_region)
                    else: 
                        current_region = None
                    if node_accepted: 
                        new_node = Node(state=current_state, central=current_central, ip=current_ip, account_code=current_account_code, region=current_region)
                        nodes.append(new_node)
                return nodes
            except Exception as error:
                raise error
        else: raise Exception("Data empty")

    def save_new_nodes(self, nodes: list[Node]) -> int:
        try:
            tqdm.write(f"Saving nodes in the database...")
            total_saved = 0
            for node in tqdm(nodes):
                node_saved = find_node(node.state, node.central, node.account_code)
                if not node_saved:
                    res = insert_new_node(node)
                    if res and res.acknowledged: total_saved += 1
            return total_saved
        except Exception as error:
            raise error
    
    def export_missing_nodes(self) -> None:
        try:
            if len(self.missing_nodes) > 0:
                export_missing_nodes(self.missing_nodes, "missing_nodes_db.xlsx")
        except Exception as error:
            raise error