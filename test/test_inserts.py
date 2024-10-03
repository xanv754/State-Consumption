from database.entity.node import Central, Node
from database.query.node.insert import insert_new_node, insert_new_nodes

# DOCS: The command to run the test is: py -m pytest test/test_inserts.py::[test function name]

def test_insert_new_nodo():
    CENTRAL = "Carapita"
    STATE = "Distrito Capital"

    new_central = Central(central=CENTRAL, ip="127.0.0.1")
    new_node = Node(state=STATE, central=[new_central])

    res = insert_new_node(new_node)
    assert res.acknowledged == True

def test_insert_new_nodes():
    CENTRAL_1 = "Carapita"
    CENTRAL_2 = "Caricuao"
    CENTRAL_3 = "La Pastora"
    CENTRAL_4 = "La Vega"
    STATE = "Distrito Capital"

    new_central_1 = Central(central=CENTRAL_1, ip="127.0.0.1")
    new_central_2 = Central(central=CENTRAL_2, ip="127.0.0.1")
    new_node = Node(state=STATE, central=[new_central_1, new_central_2])

    new_central_3 = Central(central=CENTRAL_3, ip="127.0.0.1")
    new_central_4 = Central(central=CENTRAL_4, ip="127.0.0.1")
    new_node_2 = Node(state=STATE, central=[new_central_3, new_central_4])

    new_nodes = [new_node, new_node_2]

    res = insert_new_nodes(new_nodes)
    assert res.acknowledged == True
