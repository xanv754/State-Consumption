from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from database.constants.collection import NameCollection
from database.schemas.nodes import NODES_SCHEMA
from libs.settings import SettingHandler


class MongoDatabase:
    """Class to operate with the database."""

    __name_db: str
    __connnection: MongoClient
    __database: Database
    connected: bool = False

    def __init__(self, uri: str | None = None) -> None:
        if not uri:
            settings = SettingHandler()
            uri = settings.uri
        self.__connect(uri)

    def __connect(self, uri: str) -> None:
        """Connect to the database."""
        try:
            client = MongoClient(uri)
            name_db = uri.split("/")[-1]
            database = client[name_db]
        except Exception as error:
            print(error, __file__)
            exit(1)
        else:
            self.__name_db = name_db
            self.__connnection = client
            self.__database = database
            self.connected = True

    def __check_database(self) -> bool:
        """Check if the database exists."""
        db_list = self.__connnection.list_database_names()
        return self.__name_db in db_list and self.__name_db != "admin"
    
    def __check_collection(self, name: str) -> bool:
        """Check if the collection exists."""
        collection_list = self.__database.list_collection_names()
        return name in collection_list

    def get_connection(self) -> Database:
        """Get the database connection."""
        return self.__database

    def get_collection(self, name: str) -> Collection:
        """Get the collection."""
        return self.__database[name]

    def close_connection(self) -> None:
        """Close the connection to the database."""
        if self.connected:
            self.__connnection.close()
            self.connected = False

    def migration(self) -> bool:
        """Migration of the database."""
        try:
            if not self.__check_collection(NameCollection.NODES):
                self.__database.create_collection(
                    name=NameCollection.NODES,
                    validator=NODES_SCHEMA,
                )
        except Exception as error:
            print(error, __file__)
            return False
        else:
            return True
        finally:
            self.close_connection()

    def rollback(self) -> bool:
        """Rollback of the database."""
        try:
            if self.__check_database():
                self.__database.drop_collection(NameCollection.NODES)
                self.__connnection.drop_database(self.__name_db)
        except Exception as error:
            print(error, __file__)
            return False
        else:
            return True
        finally:
            self.close_connection()