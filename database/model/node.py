from pydantic import BaseModel

class NodeModel(BaseModel):
    """Model of the node."""

    id: str | None = None
    state: str
    central: str
    ip: str | None = None
    account_code: str
    region: str | None = None