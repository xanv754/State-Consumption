from database.constants.fields import NodesFieldCollection

NODES_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            NodesFieldCollection.STATE,
            NodesFieldCollection.CENTRAL,
            NodesFieldCollection.ACCOUNT_CODE,
        ],
        "properties": {
            NodesFieldCollection.STATE: {
                "bsonType": "string",
                "description": "State of the node",
            },
            NodesFieldCollection.CENTRAL: {
                "bsonType": "string",
                "description": "Name of the node",
            },
            NodesFieldCollection.IP: {
                "bsonType": ["string", "null"],
                "description": "IP of the node",
            },
            NodesFieldCollection.ACCOUNT_CODE: {
                "bsonType": "string",
                "description": "Account code of the node",
            },
            NodesFieldCollection.REGION: {
                "bsonType": ["string", "null"],
                "description": "Region of the node",
            },
        }
    }
}