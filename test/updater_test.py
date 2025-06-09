import unittest 
from database.updater import UpdaterDatabase
from test import UpdaterDatabaseFileTest

class TestUpdater(unittest.TestCase):
    """Test class to test the updater."""
    updater: UpdaterDatabaseFileTest

    def create_updater(self) -> str:
        """Create the updater file."""
        self.updater = UpdaterDatabaseFileTest()
        self.updater.create_file()
        return self.updater.filepath
    
    def delete_files(self) -> None:
        """Delete the files."""
        self.updater.delete_file()

    def test_updater(self):
        """Test the updater."""
        filepath = self.create_updater()
        updaterHandler = UpdaterDatabase(filepath)
        status = updaterHandler.update()
        self.delete_files()

        self.assertTrue(status)


if __name__ == "__main__":
    unittest.main()