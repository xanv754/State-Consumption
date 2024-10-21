from pydantic import BaseModel


class Node(BaseModel):
    state: str
    central: str
    ip: str | None
    account_code: str
    region: str | None
