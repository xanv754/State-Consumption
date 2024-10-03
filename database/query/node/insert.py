from utils.db import open_connection, close_connection
from entity.node import Node
from constant.collection import Collection
from pymongo.results import InsertOneResult

def insert_new_state(node: Node) -> InsertOneResult:
    try:
        db = open_connection()
        collection = db.get_collection(Collection.node)
        res = collection.insert_one(node.model_dump())
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
