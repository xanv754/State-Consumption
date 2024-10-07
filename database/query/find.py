from utils.db import open_connection, close_connection
from common.constant.collection import Collection
from models.node import Node

def find_node(state: str, central: str) -> Node:
    try:
        db = open_connection()
        collection = db.get_collection(Collection.NODE)
        node = collection.find_one({"state": state, "central": central})
        if node: res = Node(**node)
        else: res = None
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
    
def find_node_by_ip(ip: str) -> Node:
    try:
        db = open_connection()
        collection = db.get_collection(Collection.NODE)
        node = collection.find_one({"ip": ip})
        if node: res = Node(**node)
        else: res = None
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res

def find_node_by_central(central: str) -> Node:
    try:
        db = open_connection()
        collection = db.get_collection(Collection.NODE)
        node = collection.find_one({"central": central})
        if node: res = Node(**node)
        else: res = None
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
