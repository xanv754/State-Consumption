import os
import pandas as pd
from typing import Dict, Tuple
from abc import ABC, abstractmethod
from state_consumption.constants import NameColumns, StatusClients, BossNameColumns, AsfNameColumns
from state_consumption.database import MongoDatabase
from state_consumption.utils import terminal


class DatabaseTest:
    database: MongoDatabase
    
    def __init__(self):
        self.database = MongoDatabase(testing=True)
    
    def get_database(self) -> MongoDatabase:
        try:
            self.database.initialize_collection()
            self.database.open_connection()
            if not self.database.connected: raise Exception("No se pudo establecer conexión")
            return self.database
        except Exception as error:
            terminal.print_spinner(f"[red3]ERROR: [default]Unit test error. Problema con la base de datos - {error}")
            exit(1)
        
    def clean_database(self) -> None:
        self.database.drop_collection()
        self.database.close_connection()


class FileHandler(ABC):
    """Class to test file."""
    filepath: str

    @abstractmethod
    def create_file(self) -> None:
        """Create the file to testing."""
        pass
    
    @abstractmethod
    def get_data(self) -> pd.DataFrame:
        """Get data to testing."""
        pass

    def delete_file(self) -> None:
        """Delete the file."""
        if os.path.exists(self.filepath):
            os.remove(self.filepath)


class BossFile(FileHandler):
    """Class to test BOSS file."""

    def __init__(self, filepath: str | None = None) -> None:
        if not filepath:
            filepath = f"./clientes.xlsx"
        self.filepath = filepath
        
    def get_example_to_export(self) -> Dict[str, list[str | int]]:
        return {
            BossNameColumns.SUFFIX_BRAS: ["bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00"],
            BossNameColumns.PREFIX_BRAS: ["cnt", "cnt", "cnt", "cnt", "cnt", "cnt", "cnt", "cnt", "cnt", "cnt"],
            BossNameColumns.EQUIPMENT: ["JUNIPER", "JUNIPER", "JUNIPER", "JUNIPER", "MDU_HW", "JUNIPER", "JUNIPER", "MDU_HW", "JUNIPER", "JUNIPER"],
            BossNameColumns.CENTRAL: ["nodo 1", "nodo 2", "nodo 3", "nodo 4", "nodo 5", "nodo 6", "nodo 7", "nodo 8", "nodo 9", "nodo 10"],
            BossNameColumns.ACCOUNT_CODE: [2316, 2316, 2229, 2229, 2229, 2229, 2229, 3307, 3608, 3608],
            BossNameColumns.STATUS: [StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE],
            BossNameColumns.TOTAL_CLIENTS: [5, 7, 2, 1, 10, 1, 1, 10, 1, 4],
            NameColumns.STATE: ["AMAZONAS", "APURE", "MIRANDA", "ZULIA", "ANZOATEGUI", "MERIDA", "TRUJILLO", "BARINAS", "GUARICO", "SUCRE"],
        }
        
    def get_example(self) -> Dict[str, list[str | int]]:
        return {
            NameColumns.BRAS: ["CNT-BRAS-00", "CNT-BRAS-00", "CNT-BRAS-00", "CNT-BRAS-00", "CNT-BRAS-00", "CNT-BRAS-00", "CNT-BRAS-00", "CNT-BRAS-00", "CNT-BRAS-00", "CNT-BRAS-00"],
            BossNameColumns.EQUIPMENT: ["JUNIPER", "JUNIPER", "JUNIPER", "JUNIPER", "MDU_HW", "JUNIPER", "JUNIPER", "MDU_HW", "JUNIPER", "JUNIPER"],
            BossNameColumns.CENTRAL: ["nodo 1", "nodo 2", "nodo 3", "nodo 4", "nodo 5", "nodo 6", "nodo 7", "nodo 8", "nodo 9", "nodo 10"],
            BossNameColumns.ACCOUNT_CODE: [2316, 2316, 2229, 2229, 2229, 2229, 2229, 3307, 3608, 3608],
            NameColumns.STATE: ["AMAZONAS", "APURE", "MIRANDA", "ZULIA", "ANZOATEGUI", "MERIDA", "TRUJILLO", "BARINAS", "GUARICO", "SUCRE"],
            NameColumns.TOTAL_CLIENTS: [5, 7, 2, 1, 10, 1, 1, 10, 1, 4]
        }

    def create_file(self) -> None:
        data = self.get_example_to_export()
        df = pd.DataFrame(data)
        df.to_excel(self.filepath, index=False) # type: ignore
        
    def get_data(self) -> pd.DataFrame:
        data = self.get_example()
        df = pd.DataFrame(data)
        return df


class ConsumptionFile(FileHandler):
    """Class to test consumption file."""
    
    def __init__(self, filepath: str | None = None) -> None:
        if not filepath:
            filepath = f"./consumo.xlsx"
        self.filepath = filepath
        
    def get_example(self) -> Dict[str, list[str | float]]:
        return {
            NameColumns.BRAS: ["CNT-BRAS-00_Huawei_10GB_GE_100", "CNT-BRAS-00_Huawei_10GB_GE_101"],
            NameColumns.CONSUMPTION: [5.43, 5.42]
        }

    def create_file(self) -> None:
        data = self.get_example()
        df = pd.DataFrame(data)
        df.to_excel(self.filepath, index=False) # type: ignore

    def get_data(self) -> pd.DataFrame:
        data = self.get_example()
        df = pd.DataFrame(data)
        return df
        
class AsfFile(FileHandler):
    """Class to test ASF file."""

    def __init__(self, filepath: str | None = None) -> None:
        if not filepath:
            filepath = f"./asf.xlsx"
        self.filepath = filepath
        
    def get_example_to_export(self) -> Dict[str, list[str]]:
        return {
            AsfNameColumns.BRAS: ["CNT-BRAS-00", "CNT-BRAS-00"],
            AsfNameColumns.STATE: ["AMAZONAS", "AMAZONAS"],
            AsfNameColumns.STATUS: [StatusClients.ASF_ACTIVE, StatusClients.ASF_ACTIVE]
        }
        
    def get_example(self) -> Dict[str, list[str]]:
        return {
            AsfNameColumns.BRAS: ["CNT-BRAS-00", "CNT-BRAS-00"],
            AsfNameColumns.STATE: ["AMAZONAS", "AMAZONAS"],
            AsfNameColumns.STATUS: [StatusClients.ASF_ACTIVE, StatusClients.ASF_ACTIVE]
        }

    def create_file(self) -> None:
        data = self.get_example_to_export()
        df = pd.DataFrame(data)
        df.to_excel(self.filepath, index=False) # type: ignore
        
    def get_data(self) -> pd.DataFrame:
        data = self.get_example()
        df = pd.DataFrame(data)
        return df
    
        
class FileToTesting:
    boss: BossFile
    asf: AsfFile
    consumption: ConsumptionFile
    
    def __init__(self) -> None:
        self.boss = BossFile()
        self.asf = AsfFile()
        self.consumption = ConsumptionFile()
    
    def get_files_path(self) -> Tuple[str, str, str]:
        """Get path of testing files.
        
        :returns Tuple[str, str, str]: BOSS path, ASF path and BRAS path.
        """
        self.boss.create_file()
        self.asf.create_file()
        self.consumption.create_file()
        return self.boss.filepath, self.asf.filepath, self.consumption.filepath
    
    def delete_files(self) -> None:
        self.asf.delete_file()
        self.boss.delete_file()
        self.consumption.delete_file()


if __name__ == "__main__":
    data = FileToTesting()
    boss, asf, bras = data.get_files_path()
    df = pd.read_excel(boss) # type: ignore
    print(df)
    df = pd.read_excel(bras) # type: ignore
    print(df)
    df = pd.read_excel(asf) # type: ignore
    print(df)
    data.delete_files()    
    print(data.boss.get_data())
    print(data.asf.get_data())
    print(data.consumption.get_data())