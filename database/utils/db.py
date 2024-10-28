from os import getenv
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

load_dotenv()

MONGO_URI = getenv("URI")
DB_NAME = getenv("DB")


def open_connection() -> Database:
    """Open connection to mongo database"""
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client.get_database(DB_NAME)
    return db


def close_connection() -> None:
    """Close connection to mongo database"""
    mongo_client = MongoClient(MONGO_URI)
    mongo_client.close()
