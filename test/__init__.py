import os
import pandas as pd
from abc import ABC, abstractmethod
from constants.columns import NameColumns
from libs.reader.constants.columns import BossNameColumns, AsfNameColumns


class FileTest(ABC):
    """Class to test file."""

    filepath: str

    @abstractmethod
    def create_file(self) -> None:
        """Create the file."""
        pass

    def delete_file(self) -> None:
        """Delete the file."""
        if os.path.exists(self.filepath):
            os.remove(self.filepath)


class BossFileTest(FileTest):
    """Class to test BOSS file."""

    def __init__(self, filepath: str | None = None) -> None:
        if not filepath:
            filepath = f"./clientes.xlsx"
        self.filepath = filepath

    def create_file(self) -> None:
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

    def create_file(self) -> None:
        data = {
            NameColumns.BRAS: ["CNT-BRAS-00_Huawei_10GB_GE_100", "CNT-BRAS-00_Huawei_10GB_GE_101"],
            NameColumns.CONSUMPTION: [5.43, 5.42]
        }
        df = pd.DataFrame(data)
        df.to_excel(self.filepath, index=False)


class AsfFileTest(FileTest):
    """Class to test ASF file."""

    def __init__(self, filepath: str | None = None) -> None:
        if not filepath:
            filepath = f"./asf.xlsx"
        self.filepath = filepath

    def create_file(self) -> None:
        data = {
            AsfNameColumns.DNI: ["1111111111", "2222222222"],
            AsfNameColumns.BRAS: ["CNT-BRAS-00", "CNT-BRAS-00"],
            AsfNameColumns.STATE: ["AMAZONAS", "AMAZONAS"]
        }
        df = pd.DataFrame(data)
        df.to_excel(self.filepath, index=False)


class UpdaterDatabaseFileTest(FileTest):
    """Class to test the updater database file."""

    def __init__(self, filepath: str | None = None) -> None:
        if not filepath:
            filepath = f"./updater_database.csv"
        self.filepath = filepath

    def create_file(self) -> None:
        with open(self.filepath, "w") as file:
            file.write("dato1;nodo;dato2;ip;dato3;cc;region;estado\n")
            file.write("dato random;nodo 1;dato random;10.255.255.255;dato random;123A;Oriental;Anzoátegui\n")
            file.write("dato random;nodo 2;dato random;10.255.255.255;dato random;NULL;Andina;Táchira\n")
            file.write("dato random;nodo 3;dato random;10.255.255.255;dato random;;Los Llanos;Barinas\n")
            file.write("dato random;nodo 4;dato random;10255255255;dato random;8645;Los Llanos;Bolívar\n")
            file.write("dato random;nodo 5;dato random;10..119...1..50;dato random;8624;Los Llanos;Bolívar\n")


if __name__ == "__main__":
    boss_file = BossFileTest()
    consumption_file = ConsumptionFileTest()
    asf_file = AsfFileTest()
    updater_file = UpdaterDatabaseFileTest()

    boss_file.create_file()
    consumption_file.create_file()
    asf_file.create_file()
    updater_file.create_file()

    df = pd.read_excel(boss_file.filepath)
    print(df)
    df = pd.read_excel(consumption_file.filepath)
    print(df)
    df = pd.read_excel(asf_file.filepath)
    print(df)
    df = pd.read_csv(updater_file.filepath, delimiter=";")
    print(df)

    boss_file.delete_file()
    consumption_file.delete_file()
    asf_file.delete_file()
    updater_file.delete_file()