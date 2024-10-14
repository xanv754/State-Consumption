from utils.db import open_connection, close_connection
from common.constant.collection import Collection
from models.node import NodeModel

def find_node(state: str, central: str, account_code: str) -> NodeModel:
    try:
        db = open_connection()
        collection = db.get_collection(Collection.NODE)
        node = collection.find_one({"state": state, "central": central, "account_code": account_code})
        if node: 
            res = NodeModel(
                id=str(node["_id"]),
                state=node["state"],
                central=node["central"],
                ip=node["ip"],
                account_code=node["account_code"],
                region=node["region"]
            )
        else: res = None
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
    
def find_node_by_ip(ip: str) -> NodeModel:
    try:
        db = open_connection()
        collection = db.get_collection(Collection.NODE)
        node = collection.find_one({"ip": ip})
        if node: 
            res = NodeModel(
                id=str(node["_id"]),
                state=node["state"],
                central=node["central"],
                ip=node["ip"],
                account_code=node["account_code"],
                region=node["region"]
            )
        else: res = None
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
    
def find_node_by_central(central: str) -> list[NodeModel]:
    try:
        central_div = central.split()
        if len(central_div) > 2: central_match = ' '.join(central_div[:2])
        else: central_match = central
        nodes: list[NodeModel] = []
        db = open_connection()
        collection = db.get_collection(Collection.NODE)
        res = collection.find_one({ "central": central_match })
        states = set()
        for doc in res:
            state = doc["state"]
            if state not in states:
                states.add(state)
                res = NodeModel(
                    id=str(doc["_id"]),
                    state=doc["state"],
                    central=doc["central"],
                    ip=doc["ip"],
                    account_code=doc["account_code"],
                    region=doc["region"]
                )
                nodes.append(res)
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return nodes

def find_node_by_account_code(account_code: str) -> list[NodeModel]:
    try:
        nodes: list[NodeModel] = []
        db = open_connection()
        collection = db.get_collection(Collection.NODE)
        res = collection.find({ "account_code": account_code })
        states = set()
        for doc in res:
            state = doc["state"]
            if state not in states:
                states.add(state)
                res = NodeModel(
                    id=str(doc["_id"]),
                    state=doc["state"],
                    central=doc["central"],
                    ip=doc["ip"],
                    account_code=doc["account_code"],
                    region=doc["region"]
                )
                nodes.append(res)
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return nodes
