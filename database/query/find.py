from utils.db import open_connection, close_connection
from constant.collection import Collection

def find_node(state: str, central: str) -> dict:
    try:
        db = open_connection()
        collection = db.get_collection(Collection.node)
        node = collection.find_one({"state": state, "central": central})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return node
    
def find_node_by_ip(ip: str) -> dict:
    try:
        db = open_connection()
        collection = db.get_collection(Collection.node)
        node = collection.find_one({"ip": ip})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return node