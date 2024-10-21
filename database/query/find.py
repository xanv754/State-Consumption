from database.utils.db import open_connection, close_connection
from database.models.node import NodeModel
from database.constant import collection as COLLECTION
from database.constant import node as NODE


def find_node(state: str, central: str, account_code: str) -> NodeModel:
    try:
        db = open_connection()
        collection = db.get_collection(COLLECTION.NODE)
        node = collection.find_one(
            {NODE.STATE: state, NODE.CENTRAL: central, NODE.ACCOUNT_CODE: account_code}
        )
        if node:
            res = NodeModel(
                id=str(node[NODE.ID]),
                state=node[NODE.STATE],
                central=node[NODE.CENTRAL],
                ip=node[NODE.IP],
                account_code=node[NODE.ACCOUNT_CODE],
                region=node[NODE.REGION],
            )
        else:
            res = None
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res


def find_node_by_ip(ip: str) -> NodeModel:
    try:
        db = open_connection()
        collection = db.get_collection(COLLECTION.NODE)
        node = collection.find_one({NODE.IP: ip})
        if node:
            res = NodeModel(
                id=str(node[NODE.ID]),
                state=node[NODE.STATE],
                central=node[NODE.CENTRAL],
                ip=node[NODE.IP],
                account_code=node[NODE.ACCOUNT_CODE],
                region=node[NODE.REGION],
            )
        else:
            res = None
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res


def find_node_by_central(central: str) -> list[NodeModel]:
    try:
        central_div = central.split()
        if len(central_div) > 2:
            central_match = " ".join(central_div[:2])
        else:
            central_match = central
        nodes: list[NodeModel] = []
        db = open_connection()
        collection = db.get_collection(COLLECTION.NODE)
        res = collection.find_one({NODE.CENTRAL: central_match})
        states = set()
        for node in res:
            state = node[NODE.STATE]
            if state not in states:
                states.add(state)
                res = NodeModel(
                    id=str(node[NODE.ID]),
                    state=node[NODE.STATE],
                    central=node[NODE.CENTRAL],
                    ip=node[NODE.IP],
                    account_code=node[NODE.ACCOUNT_CODE],
                    region=node[NODE.REGION],
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
        collection = db.get_collection(COLLECTION.NODE)
        res = collection.find({NODE.ACCOUNT_CODE: account_code})
        states = set()
        for node in res:
            state = node[NODE.STATE]
            if state not in states:
                states.add(state)
                res = NodeModel(
                    id=str(node[NODE.ID]),
                    state=node[NODE.STATE],
                    central=node[NODE.CENTRAL],
                    ip=node[NODE.IP],
                    account_code=node[NODE.ACCOUNT_CODE],
                    region=node[NODE.REGION],
                )
                nodes.append(res)
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return nodes
