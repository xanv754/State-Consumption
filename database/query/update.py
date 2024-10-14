from database.utils.db import open_connection, close_connection
from common.constant.collection import Collection
from database.entity.node import Node
from pymongo.results import UpdateResult
from bson import ObjectId

def update_nodo(id: str, nodo: Node) -> UpdateResult:
    try:
        db = open_connection()
        collection = db.get_collection(Collection.NODE)
        res = collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": {
                "state": nodo.state,
                "central": nodo.central,
                "ip": nodo.ip,
                "account_code": nodo.account_code,
                "region": nodo.region
            }}
        )
    except Exception as error:
        raise error
    else:
        close_connection()
        return res