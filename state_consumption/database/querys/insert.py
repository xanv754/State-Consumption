from typing import Literal
from pymongo.collection import Collection
from pymongo.operations import UpdateOne
from pymongo.results import BulkWriteResult
from state_consumption.constants import SSOMPScrappingColumns
from state_consumption.database.libs.mongo import MongoDatabase, NODES_COLLECTION
from state_consumption.database.schemas.nodes import NodesField
from state_consumption.utils import logger, terminal


class InsertQuery:
    _database: MongoDatabase
    _collection: Collection

    def __init__(self, dev: bool = False, testing: bool = False):
        self._database = MongoDatabase(dev=dev, testing=testing)
        self._database.open_connection()
        client = self._database.get_client()
        self._collection = client[NODES_COLLECTION]

    def insert_nodes(self, nodes: list[dict]) -> BulkWriteResult | Literal[False]:
        """Inserta o actualiza nodos en la base de datos usando upsert para evitar duplicados.
        
        Cada nodo debe tener un 'unique_id' generado (ej. account_code_central).
        """
        try:
            if not self._database.connected:
                logger.error("La conexión a la base de datos no está abierta.")
                return False

            operations = []
            for node in nodes:
                query = {
                    NodesField.ACCOUNT_CODE: node.get(SSOMPScrappingColumns.ACCOUNT_CODE),
                    NodesField.CENTRAL: node.get(SSOMPScrappingColumns.NAME_NODE)
                }
                update = {
                    "$set": {
                        NodesField.STATE: node.get(SSOMPScrappingColumns.STATE),
                        NodesField.ACCOUNT_CODE: node.get(SSOMPScrappingColumns.ACCOUNT_CODE),
                        NodesField.CENTRAL: node.get(SSOMPScrappingColumns.NAME_NODE)
                    }
                }
                operations.append(UpdateOne(query, update, upsert=True))

            if not operations:
                logger.warning("No hay operaciones válidas para insertar")
                return False

            result = self._collection.bulk_write(operations, ordered=False)
            inserted = result.upserted_count
            modified = result.modified_count
            total_operations = inserted + modified
            logger.info(f"Operaciones realizadas: {total_operations} (Inserciones nuevas: {inserted}, Modificaciones: {modified})")
            terminal.print(f"[green3]Operaciones realizadas: {total_operations} (Nuevos: {inserted}, Modificados: {modified})")

            actual_count = self._collection.count_documents({})
            logger.info(f"Total de registros actualmente tras la actualización: {actual_count}")
            if inserted > 0 or modified > 0:
                logger.info(f"La base de datos ha sido actualizada correctamente.")
            else:
                logger.warning("No se realizaron cambios en la base de datos")

            return result
        except Exception as error:
            logger.error(f"Error al insertar nodos - {error}")
            terminal.print(f"[red3]ERROR: [default]Error al insertar nodos - {error}")
            return False
        finally:
            self._database.close_connection()