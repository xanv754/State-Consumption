from pymongo.collection import Collection
from pymongo.operations import UpdateOne
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

    def insert_nodes(self, nodes: list[dict]):
        """
        Inserta o actualiza nodos en la base de datos usando upsert para evitar duplicados.
        Cada nodo debe tener un 'unique_id' generado (ej. account_code_central).
        """
        try:
            if not self._database.connected:
                logger.error("La conexión a la base de datos no está abierta.")
                return False

            operations = []
            for node in nodes:
                query = {
                    NodesField.ACCOUNT_CODE: node.get("CC"),
                    NodesField.CENTRAL: node.get("Nombre del Nodo")
                }
                update = {
                    "$set": {
                        NodesField.STATE: node.get("Estado"),
                        NodesField.ACCOUNT_CODE: node.get("CC"), # Reafirmamos las claves por seguridad
                        NodesField.CENTRAL: node.get("Nombre del Nodo")
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
            logger.info(f"Conteo real en BD después de operaciones: {actual_count}")
            expected_new_total = actual_count 
            if inserted > 0 or modified > 0:
                logger.info(f"Operaciones confirmadas: BD actualizada correctamente.")
            else:
                logger.warning("No se realizaron cambios en la BD; posibles duplicados o errores.")

            return result
        except Exception as error:
            logger.error(f"Error al insertar nodos: {error}")
            terminal.print(f"[red3]ERROR: [default]Error al insertar nodos: {error}")
            return False
        finally:
            self._database.close_connection()