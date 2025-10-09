import unittest
from state_consumption.database import InsertQuery, FindQuery
from state_consumption.test import DatabaseTest


class TestDatabase(unittest.TestCase):
    db_handler: DatabaseTest = DatabaseTest()
    state: str = "ESTADO_PRUEBA"
    cc: str = "CC_PRUEBA"
    central: str = "CENTRAL_PRUEBA"
    
    
    def test_a_insert(self) -> None:
        """Test to insert a new node."""
        database = self.db_handler.get_database()
        self.assertTrue(database.connected)
        query = InsertQuery(db=database)
        response = query.insert(state=self.state, central=self.central, cc=self.cc)
        self.assertTrue(response)
        
        
    def test_b_find(self) -> None:
        """Test to find a node by central name."""
        database = self.db_handler.get_database()
        self.assertTrue(database.connected)
        query = FindQuery(db=database)
        response = query.find_state_by_central(central=self.central)
        self.assertTrue(response)
        self.db_handler.clean_database()
        
        
if __name__ == "__main__":
    unittest.main()
        