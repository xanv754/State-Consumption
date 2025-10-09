from pymongo.collection import Collection
from state_consumption.database.libs.mongo import MongoDatabase, NODES_COLLECTION
from state_consumption.database.schemas.nodes import NodesField
from state_consumption.utils import logger


class FindQuery:
    _database: MongoDatabase
    _collection: Collection
    
    def __init__(self, db: MongoDatabase):
        self._database = db
        client = self._database.get_client()
        self._collection = client[NODES_COLLECTION]
                
    def find_state_by_central(self, central: str) -> str | None:
        """Find a state by node name.
        
        :params central: Name of the node.
        :type central: str
        :returns str | None: Returns the state if the node is found.
        """
        try:
            response = self._collection.find_one({
                NodesField.CENTRAL: central
            })
            if response: return response[NodesField.STATE]
            return None
        except Exception as error:
            logger.error(f"Problema al buscar un registro en la colección - {error}")
            return None
        
    def find_state_by_cc(self, cc: str) -> str | None:
        """Find a state by account code of the node.
        
        :params cc: Account code of the node.
        :type cc: str
        :returns str | None: Returns the state if the node is found.
        """
        try:
            response = self._collection.find_one({
                NodesField.ACCOUNT_CODE: cc
            })
            if response: return response[NodesField.STATE]
            return None
        except Exception as error:
            logger.error(f"Problema al buscar un registro en la colección - {error}")
            return None