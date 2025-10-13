import unittest 
from state_consumption.libs import ProcessData
from state_consumption.constants import NameColumns
from state_consumption.test import FileToTesting


class TestAdsl(unittest.TestCase):
    """Test class to test the process."""
    
    def test_get_data(self):
        """Test the get only data ADSL of BOSS file."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_adsl = dataHandler.get_data_adsl()
        file_handler.delete_files()
        self.assertTrue(len(data_adsl) == 8)

    def test_total_clients_by_state(self):
        """Test the total clients by state of ADSL."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_adsl = dataHandler.total_clients_adsl()
        file_handler.delete_files()
        
        print(data_adsl)

        self.assertFalse(data_adsl.empty)
        self.assertTrue(data_adsl[NameColumns.TOTAL_CLIENTS][0] == 5)
        self.assertTrue(data_adsl[NameColumns.TOTAL_CLIENTS][1] == 7)

    def test_total_clients_by_bras(self):
        """Test the total clients by bras of ADSL."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_adsl = dataHandler.total_clients_adsl_by_bras()
        file_handler.delete_files()
        
        print(data_adsl)

        self.assertFalse(data_adsl.empty)
        self.assertTrue(data_adsl[NameColumns.TOTAL_CLIENTS][0] == 22)

    def test_total_consumption_by_bras(self):
        """Test the total consumption by bras of ADSL."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_adsl = dataHandler.total_consumption_adsl_by_bras()
        file_handler.delete_files()
        
        print(data_adsl)

        self.assertFalse(data_adsl.empty)
        self.assertTrue(data_adsl[NameColumns.CONSUMPTION][0] == 5.42)

    def test_total_consumption_bras_by_state(self):
        """Test the total consumption of each bras by state of ADSL."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_adsl = dataHandler.total_consumption_state_adsl_by_bras()
        file_handler.delete_files()
        
        print(data_adsl)

        self.assertFalse(data_adsl.empty)
        self.assertTrue(data_adsl[NameColumns.CONSUMPTION][0] == 1.23)
        self.assertTrue(data_adsl[NameColumns.CONSUMPTION][1] == 1.72)

    def test_total_consumption_by_state(self):
        """Test the total consumption of ADSL by state."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_adsl = dataHandler.total_consumption_adsl_by_state()
        file_handler.delete_files()

        print(data_adsl)

        self.assertFalse(data_adsl.empty)
        self.assertTrue(data_adsl[NameColumns.CONSUMPTION][0] == 1.23)
        self.assertTrue(data_adsl[NameColumns.CONSUMPTION][1] == 1.72)


class TestMdu(unittest.TestCase):
    """Test class to test the process."""

    def test_get_data(self):
        """Test the get only data MDU of BOSS file."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_mdu = dataHandler.get_data_mdu()
        file_handler.delete_files()
        
        print(data_mdu)

        self.assertTrue(len(data_mdu) == 2)

    def test_total_clients_by_state(self):
        """Test the total clients by state of MDU."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_mdu = dataHandler.total_clients_mdu()
        file_handler.delete_files()
        
        print(data_mdu)

        self.assertFalse(data_mdu.empty)
        self.assertTrue(data_mdu[NameColumns.TOTAL_CLIENTS][0] == 10)
        self.assertTrue(data_mdu[NameColumns.TOTAL_CLIENTS][1] == 10)

    def test_total_clients_by_bras(self):
        """Test the total clients by bras of MDU."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_mdu = dataHandler.total_clients_mdu_by_bras()
        file_handler.delete_files()
        
        print(data_mdu)

        self.assertFalse(data_mdu.empty)
        self.assertTrue(data_mdu[NameColumns.TOTAL_CLIENTS][0] == 20)

    def test_total_consumption_by_bras(self):
        """Test the total consumption by bras of MDU."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_mdu = dataHandler.total_consumption_mdu_by_bras()
        file_handler.delete_files()

        print(data_mdu)

        self.assertFalse(data_mdu.empty)
        self.assertTrue(data_mdu[NameColumns.CONSUMPTION][0] == 4.93)

    def test_total_consumption_bras_by_state(self):
        """Test the total consumption of each bras by state of MDU."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_mdu = dataHandler.total_consumption_state_mdu_by_bras()
        file_handler.delete_files()
        
        print(data_mdu)

        self.assertFalse(data_mdu.empty)
        self.assertTrue(data_mdu[NameColumns.CONSUMPTION][0] == 2.46)
        self.assertTrue(data_mdu[NameColumns.CONSUMPTION][1] == 2.46)

    def test_total_consumption_by_state(self):
        """Test the total consumption of MDU by state."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_mdu = dataHandler.total_consumption_mdu_by_state()
        file_handler.delete_files()
        
        print(data_mdu)

        self.assertFalse(data_mdu.empty)
        self.assertTrue(data_mdu[NameColumns.CONSUMPTION][0] == 2.46)
        self.assertTrue(data_mdu[NameColumns.CONSUMPTION][1] == 2.46)


class TestOlt(unittest.TestCase):
    """Test class to test the process."""

    def test_get_data(self):
        """Test the get only data ASF of BOSS file."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_olt = dataHandler.get_data_asf()
        file_handler.delete_files()

        print(data_olt)

        self.assertTrue(len(data_olt) == 2)

    def test_total_clients_by_state(self):
        """Test the total clients by state of ASF."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_olt = dataHandler.total_clients_olt()
        file_handler.delete_files()
        
        print(data_olt)

        self.assertFalse(data_olt.empty)
        self.assertTrue(NameColumns.TOTAL_CLIENTS in data_olt.columns)
        self.assertTrue(data_olt[NameColumns.TOTAL_CLIENTS][0] == 2)

    def test_total_clients_by_bras(self):
        """Test the total clients by bras of MDU."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_olt = dataHandler.total_clients_olt_by_bras()
        file_handler.delete_files()
        
        print(data_olt)

        self.assertFalse(data_olt.empty)
        self.assertTrue(data_olt[NameColumns.TOTAL_CLIENTS][0] == 2)

    def test_total_consumption_by_bras(self):
        """Test the total consumption by bras of MDU."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_olt = dataHandler.total_consumption_olt_by_bras()
        file_handler.delete_files()
        
        print(data_olt)

        self.assertFalse(data_olt.empty)
        self.assertTrue(data_olt[NameColumns.CONSUMPTION][0] == 0.49)

    def test_total_consumption_bras_by_state(self):
        """Test the total consumption of each bras by state of ASF."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_olt = dataHandler.total_consumption_state_olt_by_bras()
        file_handler.delete_files()
        
        print(data_olt)

        self.assertFalse(data_olt.empty)
        self.assertTrue(data_olt[NameColumns.CONSUMPTION][0] == 0.49)

    def test_total_consumption_by_state(self):
        """Test the total consumption of MDU by state."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data_olt = dataHandler.total_consumption_olt_by_state()
        file_handler.delete_files()
        
        print(data_olt)

        self.assertFalse(data_olt.empty)
        self.assertTrue(data_olt[NameColumns.CONSUMPTION][0] == 0.49)


class TestData(unittest.TestCase):
    """Test class to test the process."""

    def test_total_clients_by_bras(self):
        """Test the total clients by bras."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        dataHandler = ProcessData(boss_path, consumption_path, asf_path, process_consumption=True, testing=True)
        data = dataHandler.total_clients_by_bras()
        file_handler.delete_files()
        
        print(data)

        self.assertFalse(data.empty)
        self.assertTrue(data[NameColumns.TOTAL_CLIENTS][0] == 44)


if __name__ == "__main__":
    unittest.main()