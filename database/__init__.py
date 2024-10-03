from query.node.insert import insert_new_state
from entity.node import Node, Central

if __name__ == "__main__":
    # Test:
    new_central = Central(
        central="Coche",
        ip="127.0.0.1"
    )
    new_node = Node(
        _id="1",
        state="Distrito Capital",
        central=[new_central]
    )
    insert_new_state(new_node)
    print("Finish!")
