import unittest
import pandas as pd
from state_consumption.libs import Calculate
from state_consumption.test import FileToTesting
from state_consumption.constants import BossNameColumns, NameColumns

class TestCalculate(unittest.TestCase):
    data: FileToTesting = FileToTesting()
    
    def test_total_client_ADSL(self) -> None:
        boss = self.data.boss.get_data()
        adsl = boss[boss[BossNameColumns.EQUIPMENT] != "MDU_HW"]
        calculate = Calculate()
        response = calculate.total_clients_adsl_mdu(adsl)
        print("Clientes ADSL: \n", response)
        
        self.assertEqual(response.loc[0][NameColumns.TOTAL_CLIENTS], 20)
        self.assertEqual(response.loc[1][NameColumns.TOTAL_CLIENTS], 20)
        
    def test_total_client_MDU(self) -> None:
        boss = self.data.boss.get_data()
        adsl = boss[boss[BossNameColumns.EQUIPMENT] == "MDU_HW"]
        calculate = Calculate()
        response = calculate.total_clients_adsl_mdu(adsl)
        print("Clientes MDU: \n", response)
        
        self.assertEqual(response.loc[0][NameColumns.TOTAL_CLIENTS], 10)
        self.assertEqual(response.loc[1][NameColumns.TOTAL_CLIENTS], 40)
        
    def test_total_client_OLT(self) -> None:
        asf = self.data.asf.get_data()
        calculate = Calculate()
        response = calculate.total_clients_olt(asf)
        print("Clientes OLT: \n", response)
        
        self.assertEqual(response.loc[0][NameColumns.TOTAL_CLIENTS], 1)
        self.assertEqual(response.loc[1][NameColumns.TOTAL_CLIENTS], 1)
        self.assertEqual(response.loc[2][NameColumns.TOTAL_CLIENTS], 2)
        self.assertEqual(response.loc[3][NameColumns.TOTAL_CLIENTS], 2)

    def test_total_clients_by_bras(self) -> None:
        boss = self.data.boss.get_data()
        asf = self.data.asf.get_data()
        asf = asf.groupby([NameColumns.BRAS]).size().reset_index().rename(columns={0: NameColumns.TOTAL_CLIENTS})
        df = pd.concat([boss, asf], axis=0)
        calculate = Calculate()
        response = calculate.total_clients_by_bras(df)
        print("Clientes por Agregador: \n", response)
        
        self.assertEqual(response.loc[0][NameColumns.TOTAL_CLIENTS], 21)
        self.assertEqual(response.loc[1][NameColumns.TOTAL_CLIENTS], 11)
        self.assertEqual(response.loc[2][NameColumns.TOTAL_CLIENTS], 42)
        self.assertEqual(response.loc[3][NameColumns.TOTAL_CLIENTS], 22)
        
    def test_total_clients_by_state(self) -> None:
        boss = self.data.boss.get_data()
        asf = self.data.asf.get_data()
        asf = asf.groupby([NameColumns.STATE]).size().reset_index().rename(columns={0: NameColumns.TOTAL_CLIENTS})
        df = pd.concat([boss, asf], axis=0)
        calculate = Calculate()
        response = calculate.total_clients_by_state(df)
        print("Clientes por Estado: \n", response)
        
        self.assertEqual(response.loc[0][NameColumns.TOTAL_CLIENTS], 22)
        self.assertEqual(response.loc[1][NameColumns.TOTAL_CLIENTS], 32)
        self.assertEqual(response.loc[2][NameColumns.TOTAL_CLIENTS], 42)
        
    def total_consumption_equipment_by_bras(self) -> None:
        bras = self.data.consumption.get_data()

if __name__ == "__main__":
    unittest.main()