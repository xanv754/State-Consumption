from typing import List
from bson import ObjectId
from database.constants.collection import NameCollection
from database.constants.fields import NodesFieldCollection
from database.libs.mongo import MongoDatabase
from database.model.node import NodeModel
from database.utils.adapter import AdapterMongo


class NodesQueryMongo:
    """Query to the nodes collection of the MongoDB."""

    @staticmethod
    def insert_one(node: NodeModel) -> bool:
        """Insert a new node in the database.
        
        Parameters
        ----------
        node: NodeModel
            Node to be inserted.

        Returns
        -------
            Return the boolean value of the operation. True if the operation was successful.
        """
        try:
            if not NodesQueryMongo.find_one(node.state, node.central, node.account_code):
                database = MongoDatabase()
                if database.connected:
                    query = database.get_collection(name=NameCollection.NODES)
                    response = query.insert_one(
                        node.model_dump(exclude={NodesFieldCollection.ID})
                    )
                    database.close_connection()
                    return response.acknowledged
                return False
            else:
                return True
        except Exception as error:
            print(error, __file__)
            return False

    @staticmethod
    def insert_many(nodes: List[NodeModel]) -> bool:
        """Insert multiple nodes in the database.
        
        Parameters
        ----------
        nodes: List[NodeModel]
            List of nodes to be inserted.

        Returns
        -------
            Return the boolean value of the operation. True if the operation was successful.
        """
        try:
            data: List[dict] = []
            for node in nodes:
                if not NodesQueryMongo.find_one(node.state, node.central, node.account_code):
                    data.append(node.model_dump(exclude={NodesFieldCollection.ID}))
            database = MongoDatabase()
            if database.connected:
                query = database.get_collection(name=NameCollection.NODES)
                response = query.insert_many(data)
                database.close_connection()
                return response.acknowledged
            return False
        except Exception as error:
            print(error, __file__)
            return False

    @staticmethod
    def find_one(state: str, central: str, account_code: str) -> NodeModel | None:
        """Find a node in the database.
        
        Parameters
        ----------
        state: str
            State of the node.
        central: str
            Central of the node.
        account_code: str
            Account code of the node.
        """
        try:
            database = MongoDatabase()
            if database.connected:
                query = database.get_collection(name=NameCollection.NODES)
                response = query.find_one({
                    NodesFieldCollection.STATE: state, 
                    NodesFieldCollection.CENTRAL: central, 
                    NodesFieldCollection.ACCOUNT_CODE: account_code
                })
                database.close_connection()
                if response:
                    data = AdapterMongo.convert_to_node([response])
                    if data: return data[0]
            return None
        except Exception as error:
            print(error, __file__)
            return None

    @staticmethod
    def find_by_account_code(account_code: str) -> List[NodeModel]:
        """Find all nodes that match the account code.
        
        Parameters
        ----------
        account_code: str
            Account code of the nodes.
        """
        try:
            database = MongoDatabase()
            if database.connected:
                query = database.get_collection(name=NameCollection.NODES)
                response = query.find(
                    {NodesFieldCollection.ACCOUNT_CODE: account_code}
                )
                if response:
                    data = AdapterMongo.convert_to_node(response)
                    database.close_connection()
                    if data: return data
            return []
        except Exception as error:
            print(error, __file__)
            return []

    @staticmethod
    def update_one(id: str, data: NodeModel) -> bool:
        """Update an existing node in the database.
        
        Parameters
        ----------
        id: str
            ID of the node in the database.
        data: NodeModel
            Node with the update data.
        """
        try:
            database = MongoDatabase()
            if database.connected:
                query = database.get_collection(name=NameCollection.NODES)
                response = query.update_one(
                    {NodesFieldCollection.ID: ObjectId(id)},
                    {
                        "$set": {
                            NodesFieldCollection.STATE: data.state,
                            NodesFieldCollection.CENTRAL: data.central,
                            NodesFieldCollection.IP: data.ip,
                            NodesFieldCollection.ACCOUNT_CODE: data.account_code,
                            NodesFieldCollection.REGION: data.region,
                        }
                    },
                )
                database.close_connection()
                return response.acknowledged
            return False
        except Exception as error:
            print(error, __file__)
            return False