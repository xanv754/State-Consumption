from database.lib.data import upload_file
from database.models.node import NodeModel
from database.lib.database import DatabaseController
from database.lib.masternode import MasternodeController

class Conductor:

    @staticmethod
    def add_nodes_by_file() -> int:
        """Add new nodes from a file."""
        try:
            df = upload_file()
            masternodo = MasternodeController(df)
            nodes_updated = DatabaseController.save_new_nodes(masternodo.data_nodes)
            return nodes_updated
        except Exception as error:
            raise error

    @staticmethod
    def add_node(
        central: str,
        account_node: str,
        state: str,
        ip: str | None = None,
        region: str | None = None,
    ) -> bool:
        """Add new node on the database."""
        try:
            return DatabaseController.save_new_node(
                central, account_node, state, ip, region
            )
        except Exception as error:
            raise error

    @staticmethod
    def search_node(account_code: str, central: str, state: str) -> NodeModel | None:
        """Search a node by their central, state and account code.
        
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
            node = DatabaseController.get_node(account_code, central, state)
            if node:
                return node
            return None
        except Exception as error:
            raise error

    @staticmethod
    def update_node(
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
        account_code: str
            Account code of the node.
        state: str
            State of the node.
        ip: str | None, default None
            IP of the node.
        region: str | None, default None
            Region of the node.
        """
        try:
            return DatabaseController.update_nodo(
                id, central, account_node, state, ip, region
            )
        except Exception as error:
            raise error
