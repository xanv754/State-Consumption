from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv

load_dotenv()

MONGO_URI = getenv("URI")
DB_NAME = getenv("DB")

mongo_client = MongoClient(MONGO_URI)

def open_connection() -> MongoClient:
    db = mongo_client.get_database(DB_NAME)
    return db

def close_connection() -> None:
    mongo_client.close()

