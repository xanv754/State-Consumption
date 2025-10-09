from pymongo import MongoClient, ASCENDING
from state_consumption.utils import URIEnvironment, terminal, logger
from state_consumption.database.schemas.nodes import NODES_SCHEMA, NodesField


NODES_COLLECTION = "NODES"


class MongoDatabase:
    """Class to operate with the database."""

    _uri: str
    _name_db: str
    _client: MongoClient
    connected: bool = False

    def __init__(self, dev: bool = False, testing: bool = False) -> None:
        if dev: env = URIEnvironment(dev=True)
        elif testing: env = URIEnvironment(testing=True)
        else: env = URIEnvironment(prod=True)
        self._uri = env.get_uri_db()
        self._name_db = self._uri.split("/")[-1]
        self.open_connection()

    def _check_collection(self, name: str) -> bool:
        """Check if the collection exists.
        
        :param name: Collection name
        :type name: str
        :return bool: True if the collection exists, False otherwise.
        """
        db = self._client[self._name_db]
        collection_list = db.list_collection_names()
        return name in collection_list
        
    def get_uri(self) -> str:
        return self._uri
    
    def get_client(self) -> MongoClient:
        return self._client[self._name_db]
        
    def open_connection(self) -> bool:
        try:
            if not self.connected:
                self._client = MongoClient(self._uri)
        except Exception as error:
            logger.error(f"No se ha podido establecer conexión la base de datos - {error}")
            terminal.print(f"[red3]ERROR: [default]No se ha podido establecer conexión la base de datos - {error}")
            self.connected = False
            return False
        else:
            self.connected = True
            return True
        
    def close_connection(self) -> None:
        if self.connected:
            self._client.close()
            self.connected = False
            
    def initialize_collection(self) -> None:
        try:
            if self.open_connection():
                database = self._client[self._name_db]
                if not self._check_collection(NODES_COLLECTION):
                    database.create_collection(NODES_COLLECTION, validator=NODES_SCHEMA)
                    collection = database[NODES_COLLECTION]
                    collection.create_index(
                        [
                            (NodesField.ACCOUNT_CODE, ASCENDING),
                            (NodesField.CENTRAL, ASCENDING),
                            (NodesField.STATE, ASCENDING)
                        ],
                        unique=True,
                        name="unique_nodes_index"
                    )
                self.close_connection()
        except Exception as error:
            logger.error(f"No se ha podido crear correctamente los esquemas de las colecciones - {error}")
            terminal.print(f"[red3]ERROR: [default]No se ha podido crear correctamente los esquemas de las colecciones - {error}")
            
    def drop_collection(self) -> None:
        try:
            if self.open_connection():
                database = self._client[self._name_db]
                collection = database[NODES_COLLECTION]
                collection.delete_many({})
                collection.drop()
                self.close_connection()
        except Exception as error:
            logger.error(f"No se ha podido eliminar correctamente las colecciones - {error}")
            terminal.print(f"[red3]ERROR: [default]No se ha podido eliminar correctamente las colecciones - {error}")