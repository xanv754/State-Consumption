from pydantic import BaseModel

class Node(BaseModel):
    state: str
    central: str
    ip: (str | None)
    account_code: (str | None)
    region: (str | None)
