import unittest 
from libs.process.process import ProcessHandler
from constants.columns import NameColumns
from test import BossFileTest, ConsumptionFileTest, AsfFileTest


class TestAdsl(unittest.TestCase):
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
    
    def test_get_data(self):
        """Test the get only data ADSL of BOSS file."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_adsl = dataHandler.get_data_adsl()
        self.delete_files()

        self.assertTrue(len(data_adsl) == 8)

    def test_total_clients_by_state(self):
        """Test the total clients by state of ADSL."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_adsl = dataHandler.total_clients_adsl()
        self.delete_files()

        self.assertFalse(data_adsl.empty)
        self.assertTrue(data_adsl[NameColumns.TOTAL_CLIENTS][0] == 5)
        self.assertTrue(data_adsl[NameColumns.TOTAL_CLIENTS][1] == 7)

    def test_total_clients_by_bras(self):
        """Test the total clients by bras of ADSL."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_adsl = dataHandler.total_clients_adsl_by_bras()
        self.delete_files()

        self.assertFalse(data_adsl.empty)
        self.assertTrue(data_adsl[NameColumns.TOTAL_CLIENTS][0] == 12)

    def test_total_consumption_by_bras(self):
        """Test the total consumption by bras of ADSL."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_adsl = dataHandler.total_consumption_adsl_by_bras()
        self.delete_files()

        self.assertFalse(data_adsl.empty)
        self.assertTrue(data_adsl[NameColumns.CONSUMPTION][0] == 3.83)

    def test_total_consumption_bras_by_state(self):
        """Test the total consumption of each bras by state of ADSL."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_adsl = dataHandler.total_consumption_state_adsl_by_bras()
        self.delete_files()

        self.assertFalse(data_adsl.empty)
        self.assertTrue(data_adsl[NameColumns.CONSUMPTION][0] == 1.60)
        self.assertTrue(data_adsl[NameColumns.CONSUMPTION][1] == 2.23)

    def test_total_consumption_by_state(self):
        """Test the total consumption of ADSL by state."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_adsl = dataHandler.total_consumption_adsl_by_state()
        self.delete_files()

        self.assertFalse(data_adsl.empty)
        self.assertTrue(data_adsl[NameColumns.CONSUMPTION][0] == 1.60)
        self.assertTrue(data_adsl[NameColumns.CONSUMPTION][1] == 2.23)

    def test_percentage_consumption_by_bras(self):
        """Test the percentage consumption of ADSL by state."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_adsl = dataHandler.percentage_consumption_state_adsl_by_bras()
        self.delete_files()

        self.assertFalse(data_adsl.empty)
        self.assertTrue(data_adsl[NameColumns.PERCENTAGE_CONSUMPTION][0] == 42)
        self.assertTrue(data_adsl[NameColumns.PERCENTAGE_CONSUMPTION][1] == 58)

    def test_percentage_consumption_by_state(self):
        """Test the percentage consumption of ADSL by state."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_adsl = dataHandler.percentage_consumption_adsl_by_state()
        self.delete_files()

        self.assertFalse(data_adsl.empty)
        self.assertTrue(data_adsl[NameColumns.PERCENTAGE_CONSUMPTION][0] == 42)
        self.assertTrue(data_adsl[NameColumns.PERCENTAGE_CONSUMPTION][1] == 58)


class TestMdu(unittest.TestCase):
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

    def test_get_data(self):
        """Test the get only data MDU of BOSS file."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_mdu = dataHandler.get_data_mdu()
        self.delete_files()

        self.assertTrue(len(data_mdu) == 2)

    def test_total_clients_by_state(self):
        """Test the total clients by state of MDU."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_mdu = dataHandler.total_clients_mdu()
        self.delete_files()

        self.assertFalse(data_mdu.empty)
        self.assertTrue(data_mdu[NameColumns.TOTAL_CLIENTS][0] == 10)
        self.assertTrue(data_mdu[NameColumns.TOTAL_CLIENTS][1] == 10)

    def test_total_clients_by_bras(self):
        """Test the total clients by bras of MDU."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_mdu = dataHandler.total_clients_mdu_by_bras()
        self.delete_files()

        self.assertFalse(data_mdu.empty)
        self.assertTrue(data_mdu[NameColumns.TOTAL_CLIENTS][0] == 20)

    def test_total_consumption_by_bras(self):
        """Test the total consumption by bras of MDU."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_mdu = dataHandler.total_consumption_mdu_by_bras()
        self.delete_files()

        self.assertFalse(data_mdu.empty)
        self.assertTrue(data_mdu[NameColumns.CONSUMPTION][0] == 6.38)

    def test_total_consumption_bras_by_state(self):
        """Test the total consumption of each bras by state of MDU."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_mdu = dataHandler.total_consumption_state_mdu_by_bras()
        self.delete_files()

        self.assertFalse(data_mdu.empty)
        self.assertTrue(data_mdu[NameColumns.CONSUMPTION][0] == 3.19)
        self.assertTrue(data_mdu[NameColumns.CONSUMPTION][1] == 3.19)

    def test_total_consumption_by_state(self):
        """Test the total consumption of MDU by state."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_mdu = dataHandler.total_consumption_mdu_by_state()
        self.delete_files()

        self.assertFalse(data_mdu.empty)
        self.assertTrue(data_mdu[NameColumns.CONSUMPTION][0] == 3.19)
        self.assertTrue(data_mdu[NameColumns.CONSUMPTION][1] == 3.19)

    def test_percentage_consumption_by_bras(self):
        """Test the percentage consumption of MDU by state."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_mdu = dataHandler.percentage_consumption_state_mdu_by_bras()
        self.delete_files()

        self.assertFalse(data_mdu.empty)
        self.assertTrue(data_mdu[NameColumns.PERCENTAGE_CONSUMPTION][0] == 50)
        self.assertTrue(data_mdu[NameColumns.PERCENTAGE_CONSUMPTION][1] == 50)

    def test_percentage_consumption_by_state(self):
        """Test the percentage consumption of MDU by state."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_mdu = dataHandler.percentage_consumption_mdu_by_state()
        self.delete_files()

        self.assertFalse(data_mdu.empty)
        self.assertTrue(data_mdu[NameColumns.PERCENTAGE_CONSUMPTION][0] == 50)
        self.assertTrue(data_mdu[NameColumns.PERCENTAGE_CONSUMPTION][1] == 50)


class TestOlt(unittest.TestCase):
    """Test class to test the process."""
    asf: AsfFileTest
    boss: BossFileTest
    consumption: ConsumptionFileTest

    def create_asf(self) -> str:
        """Create the ASF file."""
        self.asf = AsfFileTest()
        self.asf.create_file()
        return self.asf.filepath
    
    def create_boss(self) -> str:
        """Create the BOSS file."""
        self.boss = BossFileTest()
        self.boss.create_file()
        return self.boss.filepath

    def create_consumption(self) -> str:
        """Create the consumption file."""
        self.consumption = ConsumptionFileTest()
        self.consumption.create_file()
        return self.consumption.filepath
    
    def delete_files(self) -> None:
        """Delete the files."""
        self.boss.delete_file()
        self.asf.delete_file()
        self.consumption.delete_file()

    def test_get_data(self):
        """Test the get only data ASF of BOSS file."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_olt = dataHandler.get_data_asf()
        self.delete_files()

        self.assertTrue(len(data_olt) == 2)

    def test_total_clients_by_state(self):
        """Test the total clients by state of ASF."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_olt = dataHandler.total_clients_olt()
        self.delete_files()

        self.assertFalse(data_olt.empty)
        self.assertTrue(NameColumns.TOTAL_CLIENTS in data_olt.columns)
        self.assertTrue(data_olt[NameColumns.TOTAL_CLIENTS][0] == 2)

    def test_total_clients_by_bras(self):
        """Test the total clients by bras of MDU."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_olt = dataHandler.total_clients_olt_by_bras()
        self.delete_files()

        self.assertFalse(data_olt.empty)
        self.assertTrue(data_olt[NameColumns.TOTAL_CLIENTS][0] == 2)

    def test_total_consumption_by_bras(self):
        """Test the total consumption by bras of MDU."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_olt = dataHandler.total_consumption_olt_by_bras()
        self.delete_files()

        self.assertFalse(data_olt.empty)
        self.assertTrue(data_olt[NameColumns.CONSUMPTION][0] == 0.64)

    def test_total_consumption_bras_by_state(self):
        """Test the total consumption of each bras by state of ASF."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_olt = dataHandler.total_consumption_state_olt_by_bras()
        self.delete_files()

        self.assertFalse(data_olt.empty)
        self.assertTrue(data_olt[NameColumns.CONSUMPTION][0] == 0.64)

    def test_total_consumption_by_state(self):
        """Test the total consumption of MDU by state."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_olt = dataHandler.total_consumption_olt_by_state()
        self.delete_files()

        self.assertFalse(data_olt.empty)
        self.assertTrue(data_olt[NameColumns.CONSUMPTION][0] == 0.64)

    def test_percentage_consumption_by_bras(self):
        """Test the percentage consumption of OLT by state."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_olt = dataHandler.percentage_consumption_state_olt_by_bras()
        self.delete_files()

        self.assertFalse(data_olt.empty)
        self.assertTrue(data_olt[NameColumns.PERCENTAGE_CONSUMPTION][0] == 100)

    def test_percentage_consumption_by_state(self):
        """Test the percentage consumption of OLT by state."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data_olt = dataHandler.percentage_consumption_olt_by_state()
        self.delete_files()

        self.assertFalse(data_olt.empty)
        self.assertTrue(data_olt[NameColumns.PERCENTAGE_CONSUMPTION][0] == 100)


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

    def test_total_clients_by_bras(self):
        """Test the total clients by bras."""
        boss_path = self.create_boss()
        asf_path = self.create_asf()
        consumption_path = self.create_consumption()
        dataHandler = ProcessHandler(boss_path, consumption_path, asf_path, process_consumption=True)
        data = dataHandler.total_clients_by_bras()
        self.delete_files()

        self.assertFalse(data.empty)
        self.assertTrue(data[NameColumns.TOTAL_CLIENTS][0] == 34)

if __name__ == "__main__":
    unittest.main()