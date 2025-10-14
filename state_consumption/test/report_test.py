import unittest
from state_consumption.constants.columns import ConsumptionStateColumns, NameColumns
from state_consumption.libs import ReportHandler, ProcessData
from state_consumption.test import FileToTesting


class TestReport(unittest.TestCase):
    """Test class to test the report."""

    def test_clients_consumption_by_state(self):
        """Test the get clients and consumption by state."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        process = ProcessData(
            boss_path,
            consumption_path,
            asf_path,
            process_consumption=True,
            testing=True,
        )
        data = ReportHandler(process)
        df = data.clients_consumption_by_state()
        columns = df.columns.to_list()
        file_handler.delete_files()

        print(df)

        self.assertFalse(df.empty)
        self.assertTrue(NameColumns.STATE in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_ADSL in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_ADSL in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_MDU in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_MDU in columns)
        self.assertTrue(ConsumptionStateColumns.TOTAL_CLIENTS_OLT in columns)
        self.assertTrue(ConsumptionStateColumns.CONSUMPTION_OLT in columns)

    def test_clients_consumption_by_state_with_percentage(self):
        """Test the get clients and consumption by state with percentage."""
        file_handler = FileToTesting()
        boss_path, asf_path, consumption_path = file_handler.get_files_path()
        process = ProcessData(
            boss_path,
            consumption_path,
            asf_path,
            process_consumption=True,
            testing=True,
        )
        data = ReportHandler(process)
        df = data.clients_consumption_by_state_with_percentage()
        columns = df.columns.to_list()
        file_handler.delete_files()

        print(df)

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
