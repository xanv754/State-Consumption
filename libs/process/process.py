import pandas as pd
from constants.columns import NameColumns
from libs.reader.constants.columns import BossNewNameColumns
from libs.reader.constants.equipment import EquipmentModel
from libs.reader.boss import BossReader
from libs.reader.asf import AsfReader
from libs.reader.traffic import ConsumptionTrafficReader
from libs.process.calculations import Calculate


class ProcessHandler:
    """Class to process and get information from the data."""

    __calculate: Calculate = Calculate()
    data_adsl: pd.DataFrame
    data_mdu: pd.DataFrame
    data_olt: pd.DataFrame
    data_consumption: pd.DataFrame

    def __init__(self, boss_path: str, consumption_path: str, asf_path: str, process_consumption: bool) -> None:
        boss = BossReader(boss_path)
        data = boss.get_data()
        self.data_adsl = self.__adsl_filter(data)
        self.data_mdu = self.__mdu_filter(data)
        consumption = ConsumptionTrafficReader(path=consumption_path, process=process_consumption)
        self.data_consumption = consumption.get_data()
        asf = AsfReader(asf_path)
        self.data_olt = asf.get_data()


    def __adsl_filter(self, df: pd.DataFrame) -> None:
        """Get the ADSL from the dataframe."""
        df = df[df[BossNewNameColumns.EQUIPMENT] != EquipmentModel.MDU]
        columns_required = [NameColumns.BRAS, NameColumns.STATE, NameColumns.TOTAL_CLIENTS]
        df = df[columns_required]
        df = df.reset_index(drop=True)
        return df
    
    def __mdu_filter(self, df: pd.DataFrame) -> None:
        """Get the MDU from the dataframe."""
        df = df[df[BossNewNameColumns.EQUIPMENT] == EquipmentModel.MDU]
        columns_required = [NameColumns.BRAS, NameColumns.STATE, NameColumns.TOTAL_CLIENTS]
        df = df[columns_required]
        df = df.reset_index(drop=True)
        return df
    
    def export_missing_bras(self) -> None:
        """Export the missing bras to a .xlsx file."""
        self.__calculate.export_missing_bras()
    
    def get_data_adsl(self) -> pd.DataFrame:
        """Get the data of ADSL."""
        return self.data_adsl
    
    def get_data_mdu(self) -> pd.DataFrame:
        """Get the data of MDU."""
        return self.data_mdu
    
    def get_data_asf(self) -> pd.DataFrame:
        """Get the data of ASF."""
        return self.data_olt
    
    def get_data_consumption(self) -> pd.DataFrame:
        """Get the data of consumption."""
        return self.data_consumption
    
    def total_clients_by_bras(self) -> pd.DataFrame:
        """Total of all clients (ADSL, MDU and OLT) by bras."""
        df_total_adsl = self.total_clients_adsl()
        df_total_mdu = self.total_clients_mdu()
        df_total_olt = self.total_clients_olt()
        df_unite = pd.concat([df_total_adsl, df_total_mdu, df_total_olt], axis=0)
        df_total = df_unite.groupby(NameColumns.BRAS).sum()
        df_total.drop(columns=[NameColumns.STATE], inplace=True)
        df_total = df_total.reset_index()
        return df_total
    
    def total_clients_adsl(self) -> pd.DataFrame:
        """Totalize clients ADSL."""
        return self.__calculate.total_clients_adsl_mdu(self.data_adsl)
    
    def total_clients_mdu(self) -> pd.DataFrame:
        """Totalize clients MDU."""
        return self.__calculate.total_clients_adsl_mdu(self.data_mdu)
    
    def total_clients_olt(self) -> pd.DataFrame:
        """Totalize clients OLT."""
        return self.__calculate.total_clients_olt(self.data_olt)
    
    def total_clients_adsl_by_state(self) -> pd.DataFrame:
        """Totalize clients ADSL by state."""
        # TODO: Unit test
        df_total_clients = self.total_clients_adsl()
        return self.__calculate.total_clients_by_state(df_total_clients)
    
    def total_clients_adsl_by_bras(self) -> pd.DataFrame:
        """Totalize clients ADSL by bras."""
        df_total_clients = self.total_clients_adsl()
        return self.__calculate.total_clients_by_bras(df_total_clients)
    
    def total_clients_mdu_by_bras(self) -> pd.DataFrame:
        """Totalize clients MDU by bras."""
        df_total_clients = self.total_clients_mdu()
        return self.__calculate.total_clients_by_bras(df_total_clients)
    
    def total_clients_mdu_by_state(self) -> pd.DataFrame:
        """Totalize clients MDU by state."""
        # TODO: Unit test
        df_total_clients = self.total_clients_mdu()
        return self.__calculate.total_clients_by_state(df_total_clients)

    def total_clients_olt_by_bras(self) -> pd.DataFrame:
        """Totalize clients OLT by bras."""
        df_total_clients = self.total_clients_olt()
        return self.__calculate.total_clients_by_bras(df_total_clients)
    
    def total_clients_olt_by_state(self) -> pd.DataFrame:
        """Totalize clients OLT by state."""
        # TODO: Unit test
        df_total_clients = self.total_clients_olt()
        return self.__calculate.total_clients_by_state(df_total_clients)
    
    def total_consumption_adsl_by_bras(self) -> pd.DataFrame: #
        """Totalize the consumption by bras only ADSL."""
        df_total_clients_adsl_by_bras = self.total_clients_adsl_by_bras()
        df_total_clients_by_bras = self.total_clients_by_bras()
        brasnames = self.data_adsl[NameColumns.BRAS].unique()
        return self.__calculate.total_consumption_equipment_by_bras(df_total_clients_adsl_by_bras, df_total_clients_by_bras, self.data_consumption, brasnames)
    
    def total_consumption_mdu_by_bras(self) -> pd.DataFrame:
        """Totalize the consumption by bras only MDU."""
        df_total_clients_mdu_by_bras = self.total_clients_mdu_by_bras()
        df_total_clients = self.total_clients_by_bras()
        brasnames = self.data_mdu[NameColumns.BRAS].unique()
        return self.__calculate.total_consumption_equipment_by_bras(df_total_clients_mdu_by_bras, df_total_clients, self.data_consumption, brasnames)

    def total_consumption_olt_by_bras(self) -> pd.DataFrame:
        """Totalize the consumption by bras only OLT."""
        df_total_clients_olt_by_bras = self.total_clients_olt_by_bras()
        df_total_clients = self.total_clients_by_bras()
        brasnames = self.data_olt[NameColumns.BRAS].unique()
        return self.__calculate.total_consumption_equipment_by_bras(df_total_clients_olt_by_bras, df_total_clients, self.data_consumption, brasnames)
    
    def total_consumption_state_adsl_by_bras(self) -> pd.DataFrame:
        """Totalize the consumption of each state only ADSL and group by bras."""
        df_consumption_adsl_by_bras = self.total_consumption_adsl_by_bras()
        df_clients_adsl_by_state = self.total_clients_adsl()
        df_clients_adsl_by_bras = self.total_clients_adsl_by_bras()
        return self.__calculate.total_consumption_state_equipment_by_bras(df_consumption_adsl_by_bras, df_clients_adsl_by_state, df_clients_adsl_by_bras)
    
    def total_consumption_state_mdu_by_bras(self) -> pd.DataFrame:
        """Totalize the consumption of each state only MDU and group by bras."""
        df_consumption_mdu_by_bras = self.total_consumption_mdu_by_bras()
        df_clients_mdu_by_state = self.total_clients_mdu()
        df_clients_mdu_by_bras = self.total_clients_mdu_by_bras()
        return self.__calculate.total_consumption_state_equipment_by_bras(df_consumption_mdu_by_bras, df_clients_mdu_by_state, df_clients_mdu_by_bras)

    def total_consumption_state_olt_by_bras(self) -> pd.DataFrame:
        """Totalize the consumption of each state only OLT and group by bras."""
        df_consumption_olt_by_bras = self.total_consumption_olt_by_bras()
        df_clients_olt_by_state = self.total_clients_olt()
        df_clients_olt_by_bras = self.total_clients_olt_by_bras()
        return self.__calculate.total_consumption_state_equipment_by_bras(df_consumption_olt_by_bras, df_clients_olt_by_state, df_clients_olt_by_bras)
    
    def total_consumption_adsl_by_state(self) -> pd.DataFrame:
        """Totalize the consumption group by state only ADSL."""
        df_consumption_state_adsl_by_bras = self.total_consumption_state_adsl_by_bras()
        return self.__calculate.total_consumption_equipment_by_state(df_consumption_state_adsl_by_bras)
    
    def total_consumption_mdu_by_state(self) -> pd.DataFrame:
        """Totalize the consumption group by state only MDU."""
        df_consumption_state_mdu_by_bras = self.total_consumption_state_mdu_by_bras()
        return self.__calculate.total_consumption_equipment_by_state(df_consumption_state_mdu_by_bras)

    def total_consumption_olt_by_state(self) -> pd.DataFrame:
        """Totalize the consumption group by state only OLT."""
        df_consumption_state_olt_by_bras = self.total_consumption_state_olt_by_bras()
        return self.__calculate.total_consumption_equipment_by_state(df_consumption_state_olt_by_bras)
    
    def percentage_consumption_adsl_by_state(self) -> pd.DataFrame:
        """Totalize the percentage consumption group by state only ADSL."""
        df_consumption_adsl_by_state = self.total_consumption_adsl_by_state()
        total_consumption_bras = self.data_consumption[NameColumns.CONSUMPTION].sum()
        return self.__calculate.percentage_consumption_by_state(df_consumption_adsl_by_state, total_consumption_bras)
    
    def percentage_consumption_mdu_by_state(self) -> pd.DataFrame:
        """Totalize the percentage consumption group by state only MDU."""
        df_consumption_mdu_by_state = self.total_consumption_mdu_by_state()
        total_consumption_bras = self.data_consumption[NameColumns.CONSUMPTION].sum()
        return self.__calculate.percentage_consumption_by_state(df_consumption_mdu_by_state, total_consumption_bras)

    def percentage_consumption_olt_by_state(self) -> pd.DataFrame:
        """Totalize the percentage consumption group by state only OLT."""
        df_consumption_olt_by_state = self.total_consumption_olt_by_state()
        total_consumption_bras = self.data_consumption[NameColumns.CONSUMPTION].sum()
        return self.__calculate.percentage_consumption_by_state(df_consumption_olt_by_state, total_consumption_bras)