import os
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
    
    def delete_files(self, filepath: str | None = None) -> None:
        """Delete the files."""
        self.asf.delete_excel()
        self.boss.delete_excel()
        self.consumption.delete_excel()
        if filepath:
            if os.path.exists(filepath):
                os.remove(filepath)

    def test_export_consumption_by_state_adsl(self):
        """Test the export consumption by state ADSL."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = DataHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        filepath = DataExport.consumption_adsl_by_state(dataHandler, filepath="./test.xlsx")
        self.delete_files(filepath="./test.xlsx")

        self.assertIsNotNone(filepath)

    def test_export_consumption_by_state_mdu(self):
        """Test the export consumption by state MDU."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = DataHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        filepath = DataExport.consumption_mdu_by_state(dataHandler, filepath="./test.xlsx")
        self.delete_files(filepath="./test.xlsx")

        self.assertIsNotNone(filepath)

    def test_export_consumption_by_state_olt(self):
        """Test the export consumption by state OLT."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = DataHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        filepath = DataExport.consumption_olt_by_state(dataHandler, filepath="./test.xlsx")
        self.delete_files(filepath="./test.xlsx")

        self.assertIsNotNone(filepath)

    def test_export_consumption_by_state(self):
        """Test the export consumption by state."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = DataHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        filepath = DataExport.consumption_by_state(dataHandler, filepath="./test.xlsx")
        self.delete_files(filepath="./test.xlsx")

        self.assertIsNotNone(filepath)


if __name__ == "__main__":
    test = TestData()
    test.test_export()

