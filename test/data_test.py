import unittest
from constants.columns import ConsumptionStateColumns, NameColumns
from libs.process.data import DataHandler
from libs.process.process import ProcessHandler
from test import BossFileTest, ConsumptionFileTest, AsfFileTest


class TestData(unittest.TestCase):
    """Test class to test the process."""
    boss: BossFileTest
    asf: AsfFileTest
    consumption: ConsumptionFileTest

    def create_boss(self) -> str:
        """Create the BOSS file."""
        self.boss = BossFileTest()
        self.boss.create_file()
        return self.boss.filepath
    
    def create_asf(self) -> str:
        """Create the ASF file."""
        self.asf = AsfFileTest()
        self.asf.create_file()
        return self.asf.filepath

    def create_consumption(self) -> str:
        """Create the consumption file."""
        self.consumption = ConsumptionFileTest()
        self.consumption.create_file()
        return self.consumption.filepath
    
    def delete_files(self) -> None:
        """Delete the files."""
        self.asf.delete_file()
        self.boss.delete_file()
        self.consumption.delete_file()

    def test_clients_consumption_adsl(self):
        """Test the get clients and consumption by state ADSL."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        process = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data = DataHandler(process)
        df = data.clients_consumption_adsl_by_state()
        columns = df.columns.to_list()
        self.delete_files()

        self.assertFalse(df.empty)
        self.assertTrue(NameColumns.STATE in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_ADSL in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_ADSL in columns)

    def test_clients_consumption_mdu(self):
        """Test the get clients and consumption by state MDU."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        process = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data = DataHandler(process)
        df = data.clients_consumption_mdu_by_state()
        columns = df.columns.to_list()
        self.delete_files()

        self.assertFalse(df.empty)
        self.assertTrue(NameColumns.STATE in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_MDU in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_MDU in columns)

    def test_clients_consumption_olt(self):
        """Test the get clients and consumption by state OLT."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        process = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data = DataHandler(process)
        df = data.clients_consumption_olt_by_state()
        columns = df.columns.to_list()
        self.delete_files()

        self.assertFalse(df.empty)
        self.assertTrue(NameColumns.STATE in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_OLT in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_OLT in columns)

    def test_clients_consumption_by_state(self):
        """Test the get clients and consumption by state."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        process = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data = DataHandler(process)
        df = data.clients_consumption_by_state()
        columns = df.columns.to_list()
        self.delete_files()

        self.assertFalse(df.empty)
        self.assertTrue(NameColumns.STATE in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_ADSL in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_ADSL in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_MDU in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_MDU in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_OLT in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_OLT in columns)

    def test_clients_consumption_adsl_percentage(self):
        """Test the get clients and consumption by state ADSL with percentage."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        process = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data = DataHandler(process)
        df = data.clients_consumption_adsl_by_state_with_percentage()
        columns = df.columns.to_list()
        self.delete_files()

        self.assertFalse(df.empty)
        self.assertTrue(NameColumns.STATE in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_ADSL in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_ADSL in columns)
        self.assertTrue(ConsumptionStateColumns.PERCENTAGE_CONSUMPTION_ADSL in columns)

    def test_clients_consumption_mdu_by_state_with_percentage(self):
        """Test the get clients and consumption by state MDU with percentage."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        process = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data = DataHandler(process)
        df = data.clients_consumption_mdu_by_state_with_percentage()
        columns = df.columns.to_list()
        self.delete_files()

        self.assertFalse(df.empty)
        self.assertTrue(NameColumns.STATE in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_MDU in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_MDU in columns)
        self.assertTrue(ConsumptionStateColumns.PERCENTAGE_CONSUMPTION_MDU in columns)

    def test_clients_consumption_olt_by_state_with_percentage(self):
        """Test the get clients and consumption by state OLT with percentage."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        process = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data = DataHandler(process)
        df = data.clients_consumption_olt_by_state_with_percentage()
        columns = df.columns.to_list()
        self.delete_files()

        self.assertFalse(df.empty)
        self.assertTrue(NameColumns.STATE in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_OLT in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_OLT in columns)
        self.assertTrue(ConsumptionStateColumns.PERCENTAGE_CONSUMPTION_OLT in columns)

    def test_clients_consumption_by_state_with_percentage(self):
        """Test the get clients and consumption by state with percentage."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        process = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data = DataHandler(process)
        df = data.clients_consumption_by_state_with_percentage()
        columns = df.columns.to_list()
        self.delete_files()

        self.assertFalse(df.empty)
        self.assertTrue(NameColumns.STATE in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_ADSL in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_ADSL in columns)
        self.assertTrue(ConsumptionStateColumns.PERCENTAGE_CONSUMPTION_ADSL in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_MDU in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_MDU in columns)
        self.assertTrue(ConsumptionStateColumns.PERCENTAGE_CONSUMPTION_MDU in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_OLT in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_OLT in columns)
        self.assertTrue(ConsumptionStateColumns.PERCENTAGE_CONSUMPTION_OLT in columns)


if __name__ == "__main__":
    unittest.main()
