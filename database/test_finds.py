from query.find import find_node_by_state, find_node_by_ip

STATE = "Distrito Capital"
CENTRAL = "Carapita"
IP = "127.0.0.1"

def test_find_node():
    res = find_node_by_state(STATE, CENTRAL)
    assert res != None

def test_find_node_by_ip():
    res = find_node_by_ip(IP)
    assert res != None

