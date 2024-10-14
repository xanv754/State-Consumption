from bson import ObjectId
from pydantic import BaseModel

class NodeModel(BaseModel):
    id: str
    state: str
    central: str
    ip: (str | None)
    account_code: (str | None)
    region: (str | None)
