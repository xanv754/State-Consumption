from utils.db import open_connection, close_connection
from common.constant.collection import Collection
from models.node import Node

def find_node(state: str, central: str, account_code: str) -> Node:
    try:
        db = open_connection()
        collection = db.get_collection(Collection.NODE)
        node = collection.find_one({"state": state, "central": central, "account_code": account_code})
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
    
def find_node_by_central(central: str) -> list[Node]:
    try:
        central_div = central.split()
        if len(central_div) > 2: central_match = ' '.join(central_div[:2])
        else: central_match = central
        nodes: list[Node] = []
        db = open_connection()
        collection = db.get_collection(Collection.NODE)
        res = collection.find_one({ "central": central_match })
        states = set()
        for doc in res:
            state = doc["state"]
            if state not in states:
                states.add(state)
                nodes.append(Node(**doc))
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return nodes

def find_node_by_account_code(account_code: str) -> list[Node]:
    try:
        nodes: list[Node] = []
        db = open_connection()
        collection = db.get_collection(Collection.NODE)
        res = collection.find({ "account_code": account_code })
        states = set()
        for doc in res:
            state = doc["state"]
            if state not in states:
                states.add(state)
                nodes.append(Node(**doc))
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return nodes
