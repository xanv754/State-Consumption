from pydantic import BaseModel


class InterfaceModel(BaseModel):
    name: str
    time: str
    in_: float
    out: float
    bandwidth: float
