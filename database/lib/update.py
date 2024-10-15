from lib.database import DatabaseController
from lib.upload import upload_file

class UpdateController:

    @staticmethod
    def update_by_file() -> int:
        try:
            df = upload_file()
            Database = DatabaseController(df)
            nodes_updated = Database.update_database()
            Database.export_missing_nodes()
            return nodes_updated
        except Exception as error:
            raise error

    @staticmethod
    def create_new_node(central: str, account_node: str, state: str, ip: (str | None)=None, region: (str | None)=None) -> bool:
        try:
            return DatabaseController.save_new_node(central, account_node, state, ip, region)
        except Exception as error:
            raise error
        
    @staticmethod
    def search_node(account_code: str, central: str, state: str) -> (dict | None):
        try:
            node = DatabaseController.get_node(account_code, central, state)
            if node: return node.model_dump()
            return None
        except Exception as error:
            raise error
        
    @staticmethod
    def update_node(id: str, central: str, account_node: str, state: str, ip: (str | None)=None, region: (str | None)=None) -> bool:
        try:
            return DatabaseController.update_nodo(id, central, account_node, state, ip, region)
        except Exception as error:
            raise error