from bson import ObjectId
from pymongo.results import UpdateResult
from database import open_connection, close_connection, NodeEntity
from database import collection as COLLECTION
from database import node as NODE

def update_nodo(id: str, nodo: NodeEntity) -> UpdateResult:
    """Update an node in the database.

    Parameters
    ----------
    id: str
        ID of the node in the database.
    node: Node
        Node with the update data.
    """
    try:
        db = open_connection()
        collection = db.get_collection(COLLECTION.NODE)
        res = collection.update_one(
            {NODE.ID: ObjectId(id)},
            {
                "$set": {
                    NODE.STATE: nodo.state,
                    NODE.CENTRAL: nodo.central,
                    NODE.IP: nodo.ip,
                    NODE.ACCOUNT_CODE: nodo.account_code,
                    NODE.REGION: nodo.region,
                }
            },
        )
    except Exception as error:
        raise error
    else:
        close_connection()
        return res
