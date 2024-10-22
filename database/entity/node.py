from pydantic import BaseModel

class Node(BaseModel):
    """Entity of nodes for the database.

    Notes
    -----
    These variables must be in line with the models and the constant node's.
    """
    state: str
    central: str
    ip: str | None
    account_code: str
    region: str | None
