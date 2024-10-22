from pydantic import BaseModel

class NodeModel(BaseModel):
    """Model of nodes for the response database.

    Notes
    -----
    These variables must be in line with the entitys and the constant node's.
    """
    id: str
    state: str
    central: str
    ip: str | None
    account_code: str | None
    region: str | None
