from pymongo.results import InsertOneResult, InsertManyResult
from database.utils.db import open_connection, close_connection
from database.entity.node import Node
from database.constant import collection as COLLECTION

def insert_new_node(node: Node) -> InsertOneResult:
    """Insert a new node in the database.
    
    Parameters
    ----------
    node: Node
        Node to be inserted.
    """
    try:
        db = open_connection()
        collection = db.get_collection(COLLECTION.NODE)
        res = collection.insert_one(node.model_dump())
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res


def insert_new_nodes(nodes: list[Node]) -> InsertManyResult:
    """Insert multiple nodes in the database.
    
    Parameters
    ----------
    nodes: list[Node]
        List of nodes to be inserted.
    """
    try:
        db = open_connection()
        collection = db.get_collection(COLLECTION.NODE)
        nodes_list = [node.model_dump() for node in nodes]
        res = collection.insert_many(nodes_list)
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
