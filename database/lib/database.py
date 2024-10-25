from typing import List
from tqdm import tqdm
from database.entity.node import NodeEntity
from database.models.node import NodeModel
from database.query.find import find_node
from database.query.insert import insert_new_node
from database.query.update import update_nodo

class DatabaseController:
    """Controller of the database to add, update and more functions."""
    
    @staticmethod
    def save_new_nodes(nodes: List[NodeEntity]) -> int:
        """Save nodes on the database.
        
        Parameters
        ----------
        nodes: List[Node]
            Nodes to be saved.

        Returns
        -------
            Return the number of nodes saved.
        """
        try:
            total_saved = 0
            for node in tqdm(nodes, desc="Saving nodes..."):
                node_saved = find_node(node.state, node.central, node.account_code)
                if not node_saved:
                    res = insert_new_node(node)
                    if res and res.acknowledged:
                        total_saved += 1
            return total_saved
        except Exception as error:
            raise error
        
    @staticmethod
    def get_node(account_code: str, central: str, state: str) -> NodeModel:
        """Find of a node by their central, state and account code.

        Parameters
        ----------
        account_code: str
            Account code of the node.
        central: str
            Central of the node.
        State: str
            State of the node.
        """
        try:
            res = find_node(state, central, account_code)
            return res
        except Exception as error:
            raise error

    @staticmethod
    def save_new_node(
        central: str,
        account_node: str,
        state: str,
        ip: str | None = None,
        region: str | None = None,
    ) -> bool:
        """Save a new node on the database.

        Parameters
        ----------
        central: str
            Central of the node.
        account_node: str
            Account code of the node.
        state: str
            State of the node.
        ip: str | None, default None
            IP of the node.
        region: str | None, default None
            Region of the node.
        """
        try:
            if find_node(state, central, account_node): return True
            else:
                new_node = NodeEntity(
                    state=state,
                    central=central,
                    ip=ip,
                    account_code=account_node,
                    region=region,
                )
                res = insert_new_node(new_node)
                if res:
                    return res.acknowledged
            return False
        except Exception as error:
            raise error

    @staticmethod
    def update_nodo(
        id: str,
        central: str,
        account_node: str,
        state: str,
        ip: str | None = None,
        region: str | None = None,
    ) -> bool:
        """Update data of an existing node.
        
        Parameters
        ----------
        id: str
            ID of the node on the database.
        central: str
            Central of the node.
        account_node: str
            Account code of the node.
        state: str
            State of the node.
        ip: str | None, default None
            IP of the node.
        region: str | None, default None
            Region of the node.
        """
        try:
            new_node = NodeEntity(
                state=state,
                central=central,
                ip=ip,
                account_code=account_node,
                region=region,
            )
            res = update_nodo(id, new_node)
            if res:
                return res.acknowledged
            return False
        except Exception as error:
            raise error
