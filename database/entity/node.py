from pydantic import BaseModel

class Node(BaseModel):
    state: str
    central: str
    ip: str
    account_code: str
