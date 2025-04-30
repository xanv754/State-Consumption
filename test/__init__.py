import os
import pandas as pd
from abc import ABC, abstractmethod
from reader.constants.columns import BossNameColumns, TrafficNewNameColumns, AsfNameColumns


class FileTest(ABC):
    """Class to test file."""

    filepath: str

    @abstractmethod
    def create_excel(self) -> None:
        """Create the excel file."""
        pass

    def delete_excel(self) -> None:
        """Delete the excel file."""
        if os.path.exists(self.filepath):
            os.remove(self.filepath)


class BossFileTest(FileTest):
    """Class to test BOSS file."""

    def __init__(self, filepath: str | None = None) -> None:
        if not filepath:
            filepath = f"./clientes.xlsx"
        self.filepath = filepath

    def create_excel(self) -> None:
        data = {
            BossNameColumns.SUFFIX_BRAS: ["bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00", "bras-00"],
            BossNameColumns.PREFIX_BRAS: ["cnt", "cnt", "cnt", "cnt", "cnt", "cnt", "cnt", "cnt", "cnt", "cnt"],
            BossNameColumns.EQUIPMENT: ["JUNIPER", "JUNIPER", "JUNIPER", "JUNIPER", "MDU_HW", "JUNIPER", "JUNIPER", "MDU_HW", "JUNIPER", "JUNIPER"],
            BossNameColumns.CENTRAL: ["nodo 1", "nodo 2", "nodo 3", "nodo 4", "nodo 5", "nodo 6", "nodo 7", "nodo 8", "nodo 9", "nodo 10"],
            BossNameColumns.ACCOUNT_CODE: [2316, 2316, 2229, 2229, 2229, 2229, 2229, 3307, 3608, 3608],
            BossNameColumns.TOTAL_CLIENTS: [1, 1, 2, 1, 10, 1, 1, 10, 1, 4]
        }
        df = pd.DataFrame(data)
        df.to_excel(self.filepath, index=False)


class ConsumptionFileTest(FileTest):
    """Class to test consumption file."""
    
    def __init__(self, filepath: str | None = None) -> None:
        if not filepath:
            filepath = f"./consumo.xlsx"
        self.filepath = filepath

    def create_excel(self) -> None:
        data = {
            TrafficNewNameColumns.BRAS: ["CNT-BRAS-00_Huawei_10GB_GE_100", "CNT-BRAS-00_Huawei_10GB_GE_101"],
            TrafficNewNameColumns.CONSUMPTION: [5.43, 5.42]
        }
        df = pd.DataFrame(data)
        df.to_excel(self.filepath, index=False)


class AsfFileTest(FileTest):
    """Class to test ASF file."""

    def __init__(self, filepath: str | None = None) -> None:
        if not filepath:
            filepath = f"./asf.xlsx"
        self.filepath = filepath

    def create_excel(self) -> None:
        data = {
            AsfNameColumns.DNI: ["1111111111", "2222222222"],
            AsfNameColumns.BRAS: ["CNT-BRAS-00", "CNT-BRAS-00"],
            AsfNameColumns.STATE: ["AMAZONAS", "AMAZONAS"]
        }
        df = pd.DataFrame(data)
        df.to_excel(self.filepath, index=False)


if __name__ == "__main__":
    boss_file = BossFileTest()
    consumption_file = ConsumptionFileTest()
    asf_file = AsfFileTest()

    boss_file.create_excel()
    consumption_file.create_excel()
    asf_file.create_excel()

    df = pd.read_excel(boss_file.filepath)
    print(df)
    df = pd.read_excel(consumption_file.filepath)
    print(df)
    df = pd.read_excel(asf_file.filepath)
    print(df)

    boss_file.delete_excel()
    consumption_file.delete_excel()
    asf_file.delete_excel()