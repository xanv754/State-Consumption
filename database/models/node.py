from bson import ObjectId
from pydantic import BaseModel

class Node(BaseModel):
    _id: ObjectId
    state: str
    central: str
    ip: str
    account_code: str
