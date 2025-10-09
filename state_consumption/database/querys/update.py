from pymongo.collection import Collection
from state_consumption.database.libs.mongo import MongoDatabase, NODES_COLLECTION
from state_consumption.database.schemas.nodes import NodesField
from state_consumption.utils import logger


class UpdateQuery:
    _database: MongoDatabase
    _collection: Collection
    
    def __init__(self, db: MongoDatabase):
        self._database = db
        client = self._database.get_client()
        self._collection = client[NODES_COLLECTION]
                
    def update_state_by_central(self, new_state: str, central: str) -> bool:
        """Update a new node.
        
        :params new_state: New state of the node.
        :type state: str
        :params central: Central of the node.
        :type central: str
        :returns bool: Returns True if the operation was completed successfully, otherwise False.
        """
        try:
            response = self._collection.update_one(
                { NodesField.CENTRAL: central },
                { "$set": {NodesField.STATE: new_state } },
            )
            return response.acknowledged
        except Exception as error:
            logger.error(f"Problema al actualizar nodo: {central} - {error}")
            return False
        
    def update_state_by_central(self, new_state: str, cc: str) -> bool:
        """Update a new node.
        
        :params new_state: New state of the node.
        :type state: str
        :params cc: Account code of the node.
        :type cc: str
        :returns bool: Returns True if the operation was completed successfully, otherwise False.
        """
        try:
            response = self._collection.update_one(
                { NodesField.CC: cc },
                { "$set": {NodesField.STATE: new_state } },
            )
            return response.acknowledged
        except Exception as error:
            logger.error(f"Problema al actualizar nodo: {cc} - {error}")
            return False