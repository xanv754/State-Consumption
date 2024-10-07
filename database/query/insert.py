from utils.db import open_connection, close_connection
from entity.node import Node
from common.constant.collection import Collection
from pymongo.results import InsertOneResult, InsertManyResult

def insert_new_node(node: Node) -> InsertOneResult:
    try:
        db = open_connection()
        collection = db.get_collection(Collection.NODE)
        res = collection.insert_one(node.model_dump())
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res

def insert_new_nodes(nodes: list[Node]) -> InsertManyResult:
    try:
        db = open_connection()
        collection = db.get_collection(Collection.NODE)
        nodes_list = [node.model_dump() for node in nodes]
        res = collection.insert_many(nodes_list)
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res