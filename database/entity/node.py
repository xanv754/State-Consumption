from pydantic import BaseModel
from bson.objectid import ObjectId

class Central(BaseModel):
    central: str
    ip: str

class Node(BaseModel):
    state: str
    central: list[Central]
