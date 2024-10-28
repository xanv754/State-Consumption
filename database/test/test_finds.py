from database.query.find import find_node

STATE = "Distrito Capital"
CENTRAL = "Carapita"

def test_find_node():
    res = find_node(STATE, CENTRAL)
    assert res != None