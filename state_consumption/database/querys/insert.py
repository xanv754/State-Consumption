from pymongo.collection import Collection
from state_consumption.database.libs.mongo import MongoDatabase, NODES_COLLECTION
from state_consumption.database.schemas.nodes import NodesField
from state_consumption.utils import logger


class InsertQuery:
    _database: MongoDatabase
    _collection: Collection
    
    def __init__(self, db: MongoDatabase):
        self._database = db
        self._database.open_connection()
        client = self._database.get_client()
        self._collection = client[NODES_COLLECTION]
                
    def insert(self, state: str, central: str, cc: str) -> bool:
        """Insert a new node.
        
        :params state: State of the node.
        :type state: str
        :params central: Central of the node.
        :type central: str
        :params cc: Account code of the node.
        :type cc: str
        :returns bool: Returns True if the operation was completed successfully, otherwise False.
        """
        try:
            response = self._collection.insert_one({
                NodesField.STATE: state,
                NodesField.ACCOUNT_CODE: cc,
                NodesField.CENTRAL: central
            })
            return response.acknowledged
        except Exception as error:
            logger.error(f"Problema al insertar nuevo nodo: {central} - {error}")
            return False
        
    def insert_many(self) -> bool:
        #TODO: Implement.
        pass