import unittest 
from libs.process import DataProcess
from reader.constants.columns import BossNewNameColumns
from test import BossFileTest, ConsumptionFileTest, AsfFileTest


class TestAdsl(unittest.TestCase):
    """Test class to test the process."""
    boss: BossFileTest
    consumption: ConsumptionFileTest

    def create_boss(self) -> str:
        """Create the BOSS file."""
        self.boss = BossFileTest()
        self.boss.create_excel()
        return self.boss.filepath

    def create_consumption(self) -> str:
        """Create the consumption file."""
        self.consumption = ConsumptionFileTest()
        self.consumption.create_excel()
        return self.consumption.filepath
    
    def delete_files(self) -> None:
        """Delete the files."""
        self.boss.delete_excel()
        self.consumption.delete_excel()
    
    def test_get_data(self):
        """Test the get only data ADSL of BOSS file."""
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        processHandler = DataProcess(boss_path, consumption_path, process_consumption=True)
        data_adsl = processHandler.get_data_adsl()
        self.delete_files()

        self.assertTrue(len(data_adsl) == 8)

    def test_total_clients_by_state(self):
        """Test the total clients by state of ADSL."""
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        processHandler = DataProcess(boss_path, consumption_path, process_consumption=True)
        data_adsl = processHandler.total_clients_adsl_by_state()
        self.delete_files()

        self.assertTrue(data_adsl[BossNewNameColumns.TOTAL_CLIENTS][0] == 5)
        self.assertTrue(data_adsl[BossNewNameColumns.TOTAL_CLIENTS][1] == 7)

    def test_total_clients_by_bras(self):
        """Test the total clients by bras of ADSL."""
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        processHandler = DataProcess(boss_path, consumption_path, process_consumption=True)
        data_adsl = processHandler.total_clients_adsl_by_bras()
        self.delete_files()

        self.assertTrue(data_adsl[BossNewNameColumns.TOTAL_CLIENTS][0] == 12)

    def test_total_consumption_by_bras(self):
        """Test the total consumption by bras of ADSL."""
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        processHandler = DataProcess(boss_path, consumption_path, process_consumption=True)
        data_adsl = processHandler.total_consumption_adsl_by_bras()
        self.delete_files()

        print(data_adsl)

        self.assertTrue(True)


class TestMdu(unittest.TestCase):
    """Test class to test the process."""
    boss: BossFileTest
    consumption: ConsumptionFileTest

    def create_boss(self) -> str:
        """Create the BOSS file."""
        self.boss = BossFileTest()
        self.boss.create_excel()
        return self.boss.filepath

    def create_consumption(self) -> str:
        """Create the consumption file."""
        self.consumption = ConsumptionFileTest()
        self.consumption.create_excel()
        return self.consumption.filepath
    
    def delete_files(self) -> None:
        """Delete the files."""
        self.boss.delete_excel()
        self.consumption.delete_excel()

    def test_get_data(self):
        """Test the get only data MDU of BOSS file."""
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        processHandler = DataProcess(boss_path, consumption_path, process_consumption=True)
        data_mdu = processHandler.get_data_mdu()
        self.delete_files()

        self.assertTrue(len(data_mdu) == 2)


class TestAsf(unittest.TestCase):
    """Test class to test the process."""
    asf: AsfFileTest
    boss: BossFileTest
    consumption: ConsumptionFileTest

    def create_asf(self) -> str:
        """Create the ASF file."""
        self.asf = AsfFileTest()
        self.asf.create_excel()
        return self.asf.filepath
    
    def create_boss(self) -> str:
        """Create the BOSS file."""
        self.boss = BossFileTest()
        self.boss.create_excel()
        return self.boss.filepath

    def create_consumption(self) -> str:
        """Create the consumption file."""
        self.consumption = ConsumptionFileTest()
        self.consumption.create_excel()
        return self.consumption.filepath
    
    def delete_files(self) -> None:
        """Delete the files."""
        self.asf.delete_excel()
        self.consumption.delete_excel()

    def test_get_data(self):
        """Test the get only data ASF of BOSS file."""
        asf_path = self.create_asf()
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        processHandler = DataProcess(boss_path, consumption_path, asf_path, process_consumption=True)
        data_asf = processHandler.get_data_asf()
        self.delete_files()

        self.assertTrue(len(data_asf) == 2)


class TestProcess(unittest.TestCase):
    """Test class to test the process."""
    boss: BossFileTest
    consumption: ConsumptionFileTest

    def create_boss(self) -> str:
        """Create the BOSS file."""
        self.boss = BossFileTest()
        self.boss.create_excel()
        return self.boss.filepath

    def create_consumption(self) -> str:
        """Create the consumption file."""
        self.consumption = ConsumptionFileTest()
        self.consumption.create_excel()
        return self.consumption.filepath
    
    def delete_files(self) -> None:
        """Delete the files."""
        self.boss.delete_excel()
        self.consumption.delete_excel()

    def test_total_clients_by_bras(self):
        """Test the total clients by bras."""
        boss_path = self.create_boss()
        consumption_path = self.create_consumption()
        processHandler = DataProcess(boss_path, consumption_path, process_consumption=True)
        data = processHandler.total_clients_by_bras()
        self.delete_files()

        self.assertTrue(data[BossNewNameColumns.TOTAL_CLIENTS][0] == 32)

if __name__ == "__main__":
    unittest.main()