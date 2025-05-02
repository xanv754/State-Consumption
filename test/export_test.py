import unittest
from libs.export.data import DataExport
from libs.process.data import DataHandler
from test import BossFileTest, ConsumptionFileTest, AsfFileTest


class TestData(unittest.TestCase):
    """Test class to test the process."""
    boss: BossFileTest
    asf: AsfFileTest
    consumption: ConsumptionFileTest

    def create_boss(self) -> str:
        """Create the BOSS file."""
        self.boss = BossFileTest()
        self.boss.create_excel()
        return self.boss.filepath
    
    def create_asf(self) -> str:
        """Create the ASF file."""
        self.asf = AsfFileTest()
        self.asf.create_excel()
        return self.asf.filepath

    def create_consumption(self) -> str:
        """Create the consumption file."""
        self.consumption = ConsumptionFileTest()
        self.consumption.create_excel()
        return self.consumption.filepath
    
    def delete_files(self) -> None:
        """Delete the files."""
        self.asf.delete_excel()
        self.boss.delete_excel()
        self.consumption.delete_excel()

    def test_export(self):
        """Test the export."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = DataHandler(boss_path, consumption_path, asf_path, process_consumption=False)
        status = DataExport.consumption_by_state(dataHandler)
        self.delete_files()

        self.assertTrue(status)



if __name__ == "__main__":
    unittest.main()

