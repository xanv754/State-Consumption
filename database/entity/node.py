from pydantic import BaseModel

class Central(BaseModel):
    central: str
    ip: str

class Node(BaseModel):
    _id: str
    state: str
    central: list[Central]
