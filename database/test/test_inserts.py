from entity.node import NodeEntity
from database.query.insert import insert_new_node, insert_new_nodes

# DOCS: The command to run the test is: py -m pytest test/test_inserts.py::[test function name]


def test_insert_new_nodo():
    CENTRAL = "Carapita"
    STATE = "Distrito Capital"

    new_node = NodeEntity(state=STATE, central=CENTRAL, ip="127.0.0.1")

    res = insert_new_node(new_node)
    assert res.acknowledged == True


def test_insert_new_nodes():
    CENTRAL_1 = "Carapita"
    CENTRAL_2 = "Caricuao"
    CENTRAL_3 = "La Pastora"
    CENTRAL_4 = "La Vega"
    STATE = "Distrito Capital"

    new_node = NodeEntity(state=STATE, central=CENTRAL_1, ip="127.0.0.1")
    new_node_2 = NodeEntity(state=STATE, central=CENTRAL_2, ip="127.0.0.1")
    new_node_3 = NodeEntity(state=STATE, central=CENTRAL_3, ip="127.0.0.1")
    new_node_4 = NodeEntity(state=STATE, central=CENTRAL_4, ip="127.0.0.1")

    new_nodes = [new_node, new_node_2, new_node_3, new_node_4]

    res = insert_new_nodes(new_nodes)
    assert res.acknowledged == True
