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
            terminal.print(f"[red3]ERROR: [default]Unit test error. Problema con la base de datos - {error}")
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


# class BossFile(FileHandler):
#     """Class to test BOSS file."""

#     def __init__(self, filepath: str | None = None) -> None:
#         if not filepath:
#             filepath = f"./clientes.xlsx"
#         self.filepath = filepath

#     def create_file(self) -> None:
#         data: Dict[str, list[str | int]] = {
#             BossNameColumns.SUFFIX_BRAS: ["bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00"],
#             BossNameColumns.PREFIX_BRAS: ["cnt", "cnt", "cnt", "cnt", "cnt", "cnt", "cnt", "cnt", "cnt", "cnt"],
#             BossNameColumns.EQUIPMENT: ["JUNIPER", "JUNIPER", "JUNIPER", "JUNIPER", "MDU_HW", "JUNIPER", "JUNIPER", "MDU_HW", "JUNIPER", "JUNIPER"],
#             BossNameColumns.CENTRAL: ["nodo 1", "nodo 2", "nodo 3", "nodo 4", "nodo 5", "nodo 6", "nodo 7", "nodo 8", "nodo 9", "nodo 10"],
#             BossNameColumns.ACCOUNT_CODE: [2316, 2316, 2229, 2229, 2229, 2229, 2229, 3307, 3608, 3608],
#             BossNameColumns.STATUS: [StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE],
#             BossNameColumns.TOTAL_CLIENTS: [1, 1, 2, 1, 10, 1, 1, 10, 1, 4]
#         }
#         df = pd.DataFrame(data)
#         df.to_excel(self.filepath, index=False) # type: ignore
        
        
class BossFile(FileHandler):
    """Class to test BOSS file."""

    def __init__(self, filepath: str | None = None) -> None:
        if not filepath:
            filepath = f"./clientes.xlsx"
        self.filepath = filepath
        
    def get_example_to_export(self) -> Dict[str, list[str | int]]:
        return {
            BossNameColumns.SUFFIX_BRAS: ["bras-00", "bras-00", "bras-00", "bras-01", "bras-01", "bras-01"],
            BossNameColumns.PREFIX_BRAS: ["cnt", "cnt", "anz", "anz", "chc", "chc"],
            BossNameColumns.EQUIPMENT: ["JUNIPER", "JUNIPER", "JUNIPER", "MDU_HW", "MDU_HW", "MDU_HW"],
            BossNameColumns.CENTRAL: ["nodo adsl 1", "nodo adsl 2", "nodo adsl 3", "nodo mdu 4", "nodo mdu 5", "nodo mdu 6"],
            BossNameColumns.ACCOUNT_CODE: [2316, 2316, 2229, 2229, 3307, 3307],
            BossNameColumns.STATUS: [StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE, StatusClients.BOSS_ACTIVE],
            BossNameColumns.TOTAL_CLIENTS: [10, 10, 20, 10, 10, 30]
        }
        
    def get_example(self) -> Dict[str, list[str | int]]:
        return {
            NameColumns.BRAS: ["CNT-BRAS-00", "CNT-BRAS-00", "ANZ-BRAS-00", "ANZ-BRAS-01", "CHC-BRAS-01", "CHC-BRAS-01"],
            BossNameColumns.EQUIPMENT: ["JUNIPER", "JUNIPER", "JUNIPER", "MDU_HW", "MDU_HW", "MDU_HW"],
            BossNameColumns.CENTRAL: ["nodo adsl 1", "nodo adsl 2", "nodo adsl 3", "nodo mdu 4", "nodo mdu 5", "nodo mdu 6"],
            BossNameColumns.ACCOUNT_CODE: [2316, 2316, 2229, 2229, 3307, 3307],
            NameColumns.STATE: ["AMAZONAS", "AMAZONAS", "APURE", "APURE", "MIRANDA", "MIRANDA"],
            NameColumns.TOTAL_CLIENTS: [10, 10, 20, 10, 10, 30]
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
            NameColumns.BRAS: ["CNT-BRAS-00_Huawei_10GB_GE_100", "CNT-BRAS-00_Huawei_10GB_GE_101", "ANZ-BRAS-00_Huawei_10GB_GE_100", "ANZ-BRAS-01_Huawei_10GB_GE_100", "CHC-BRAS-01_Huawei_10GB_GE_100", "CHC-BRAS-01_Huawei_10GB_GE_101"],
            NameColumns.CONSUMPTION: [10.0, 10.0, 20.0, 20.0, 10.0, 20.0]
        }

    def create_file(self) -> None:
        data = self.get_example()
        df = pd.DataFrame(data)
        df.to_excel(self.filepath, index=False) # type: ignore

    def get_data(self) -> pd.DataFrame:
        data = self.get_example()
        df = pd.DataFrame(data)
        return df

# class AsfFile(FileHandler):
#     """Class to test ASF file."""

#     def __init__(self, filepath: str | None = None) -> None:
#         if not filepath:
#             filepath = f"./asf.xlsx"
#         self.filepath = filepath

#     def create_file(self) -> None:
#         data: Dict[str, list[str]] = {
#             AsfNameColumns.DNI: ["1111111111", "2222222222"],
#             AsfNameColumns.BRAS: ["CNT-BRAS-00", "CNT-BRAS-00"],
#             AsfNameColumns.STATE: ["AMAZONAS", "AMAZONAS"],
#             AsfNameColumns.STATUS: [StatusClients.ASF_ACTIVE, StatusClients.ASF_ACTIVE]
#         }
#         df = pd.DataFrame(data)
#         df.to_excel(self.filepath, index=False) # type: ignore
        
        
class AsfFile(FileHandler):
    """Class to test ASF file."""

    def __init__(self, filepath: str | None = None) -> None:
        if not filepath:
            filepath = f"./asf.xlsx"
        self.filepath = filepath
        
    def get_example_to_export(self) -> Dict[str, list[str]]:
        return {
            AsfNameColumns.BRAS: ["CNT-BRAS-00", "CNT-BRAS-00", "ANZ-BRAS-00", "ANZ-BRAS-01", "CHC-BRAS-01", "CHC-BRAS-01"],
            AsfNameColumns.STATE: ["AMAZONAS", "AMAZONAS", "APURE", "APURE", "MIRANDA", "MIRANDA"],
            AsfNameColumns.STATUS: [StatusClients.ASF_ACTIVE, StatusClients.ASF_ACTIVE, StatusClients.ASF_ACTIVE, StatusClients.ASF_ACTIVE, StatusClients.ASF_ACTIVE, StatusClients.ASF_ACTIVE]
        }
        
    def get_example(self) -> Dict[str, list[str]]:
        return {
            NameColumns.BRAS: ["CNT-BRAS-00", "CNT-BRAS-00", "ANZ-BRAS-00", "ANZ-BRAS-01", "CHC-BRAS-01", "CHC-BRAS-01"],
            NameColumns.STATE: ["AMAZONAS", "AMAZONAS", "APURE", "APURE", "MIRANDA", "MIRANDA"],
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
    # boss, asf, bras = data.get_files_path()

    # df = pd.read_excel(boss) # type: ignore
    # print(df)
    # df = pd.read_excel(bras) # type: ignore
    # print(df)
    # df = pd.read_excel(asf) # type: ignore
    # print(df)

    # data.delete_files()
    
    print(data.boss.get_data())
    print(data.asf.get_data())
    print(data.consumption.get_data())