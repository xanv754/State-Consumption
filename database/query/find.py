from database import open_connection, close_connection, NodeModel
from database import collection as COLLECTION
from database import node as NODE

def find_node(state: str, central: str, account_code: str) -> NodeModel:
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

def find_node_by_account_code(account_code: str) -> list[NodeModel]:
    """Find all nodes that match the account code.
    
    Parameters
    ----------
    account_code: str
        Account code of the nodes.
    """
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
