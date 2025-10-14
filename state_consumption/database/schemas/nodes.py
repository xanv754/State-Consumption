class NodesField:
    ID: str = "id"
    STATE: str = "state"
    CENTRAL: str = "central"
    ACCOUNT_CODE: str = "account_code"


NODES_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            NodesField.STATE,
            NodesField.CENTRAL,
            NodesField.ACCOUNT_CODE,
        ],
        "properties": {
            NodesField.STATE: {
                "bsonType": "string",
                "description": "State of the node",
            },
            NodesField.CENTRAL: {
                "bsonType": "string",
                "description": "Name of the node",
            },
            NodesField.ACCOUNT_CODE: {
                "bsonType": "string",
                "description": "Account code of the node",
            },
        },
    }
}
