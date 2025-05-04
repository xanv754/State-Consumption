import os
import unittest
from libs.cli import ExportCLIHandler
from test import BossFileTest, ConsumptionFileTest, AsfFileTest


class TestExport(unittest.TestCase):
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

    def test_clients_consumption_adsl_by_state(self):
        """Test the get clients and consumption by state ADSL."""
        filepath = "./test_adsl.xlsx"
        boss_path = self.create_boss()
        asf_path = self.create_asf()
        consumption_path = self.create_consumption()
        export = ExportCLIHandler(boss_path=boss_path, asf_path=asf_path, bras_path=consumption_path, process_consumption=True)
        savedIn = export.clients_consumption_adsl_by_state(filepath=filepath)
        self.delete_files(filepath=filepath)

        self.assertIsNotNone(savedIn)

    def test_clients_consumption_mdu_by_state(self):
        """Test the get clients and consumption by state MDU."""
        filepath = "./test_mdu.xlsx"
        boss_path = self.create_boss()
        asf_path = self.create_asf()
        consumption_path = self.create_consumption()
        export = ExportCLIHandler(boss_path=boss_path, asf_path=asf_path, bras_path=consumption_path, process_consumption=True)
        savedIn = export.clients_consumption_mdu_by_state(filepath=filepath)
        self.delete_files(filepath=filepath)

        self.assertIsNotNone(savedIn)

    def test_clients_consumption_olt_by_state(self):
        """Test the get clients and consumption by state OLT."""
        filepath = "./test_olt.xlsx"
        boss_path = self.create_boss()
        asf_path = self.create_asf()
        consumption_path = self.create_consumption()
        export = ExportCLIHandler(boss_path=boss_path, asf_path=asf_path, bras_path=consumption_path, process_consumption=True)
        savedIn = export.clients_consumption_olt_by_state(filepath=filepath)
        self.delete_files(filepath=filepath)

        self.assertIsNotNone(savedIn)

    def test_clients_consumption_by_state(self):
        """Test the get clients and consumption by state."""
        filepath = "./test_by_state.xlsx"
        boss_path = self.create_boss()
        asf_path = self.create_asf()
        consumption_path = self.create_consumption()
        export = ExportCLIHandler(boss_path=boss_path, asf_path=asf_path, bras_path=consumption_path, process_consumption=True)
        savedIn = export.clients_consumption_by_state(filepath=filepath)
        self.delete_files(filepath=filepath)

        self.assertIsNotNone(savedIn)


if __name__ == "__main__":
    unittest.main()