from typing import List
from database.constants.fields import NodesFieldCollection
from database.model.node import NodeModel


class AdapterMongo:
    """Adapter to convert the data from the database to the model."""

    @staticmethod
    def convert_to_node(data: List[dict]) -> List[NodeModel]:
        nodes: List[NodeModel] = []
        for node in data:
            nodes.append(
                NodeModel(
                    id=str(node["_id"]),
                    state=node[NodesFieldCollection.STATE],
                    central=node[NodesFieldCollection.CENTRAL],
                    ip=node[NodesFieldCollection.IP],
                    account_code=node[NodesFieldCollection.ACCOUNT_CODE],
                    region=node[NodesFieldCollection.REGION],
                )
            )
        return nodes