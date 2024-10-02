from pydantic import BaseModel

class Central(BaseModel):
    _id: str
    central: str

class Node(BaseModel):
    state: str
    plants: list[Central]
