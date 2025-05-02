import pandas as pd
from reader.constants.columns import BossNewNameColumns, NameColumns
from reader.constants.equipment import EquipmentModelConstant
from reader.boss import BossReader
from reader.asf import AsfReader
from reader.traffic import ConsumptionTrafficReader
from libs.process.calculations import Calculate


class DataHandler:
    """Class to get information from the data."""

    data_adsl: pd.DataFrame
    data_mdu: pd.DataFrame
    data_asf: pd.DataFrame
    data_consumption: pd.DataFrame

    def __init__(self, boss_path: str, consumption_path: str, asf_path: str, process_consumption: bool = False) -> None:
        boss = BossReader(boss_path)
        data = boss.get_data()
        self.data_adsl = self.__adsl_filter(data)
        self.data_mdu = self.__mdu_filter(data)
        consumption = ConsumptionTrafficReader(path=consumption_path, process=process_consumption)
        self.data_consumption = consumption.get_data()
        asf = AsfReader(asf_path)
        self.data_asf = asf.get_data()


    def __adsl_filter(self, df: pd.DataFrame) -> None:
        """Get the ADSL from the dataframe."""
        df = df[df[BossNewNameColumns.EQUIPMENT] != EquipmentModelConstant.MDU]
        columns_required = [NameColumns.BRAS, NameColumns.STATE, NameColumns.TOTAL_CLIENTS]
        df = df[columns_required]
        df = df.reset_index(drop=True)
        return df
    
    def __mdu_filter(self, df: pd.DataFrame) -> None:
        """Get the MDU from the dataframe."""
        df = df[df[BossNewNameColumns.EQUIPMENT] == EquipmentModelConstant.MDU]
        columns_required = [NameColumns.BRAS, NameColumns.STATE, NameColumns.TOTAL_CLIENTS]
        df = df[columns_required]
        df = df.reset_index(drop=True)
        return df
    
    def get_data_adsl(self) -> pd.DataFrame:
        """Get the data of ADSL."""
        return self.data_adsl
    
    def get_data_mdu(self) -> pd.DataFrame:
        """Get the data of MDU."""
        return self.data_mdu
    
    def get_data_asf(self) -> pd.DataFrame:
        """Get the data of ASF."""
        return self.data_asf
    
    def total_clients_by_bras(self) -> pd.DataFrame:
        """Total of all clients (ADSL, MDU and OLT) by bras."""
        df_total_adsl = self.total_clients_adsl()
        df_total_mdu = self.total_clients_mdu()
        df_total_asf = self.total_clients_olt()
        df_unite = pd.concat([df_total_adsl, df_total_mdu, df_total_asf], axis=0)
        df_total = df_unite.groupby(NameColumns.BRAS).sum()
        df_total.drop(columns=[NameColumns.STATE], inplace=True)
        df_total = df_total.reset_index()
        return df_total
    
    def total_clients_adsl(self) -> pd.DataFrame:
        """Totalize clients ADSL."""
        return Calculate.total_clients_adsl_mdu(self.data_adsl)
    
    def total_clients_mdu(self) -> pd.DataFrame:
        """Totalize clients MDU."""
        return Calculate.total_clients_adsl_mdu(self.data_mdu)
    
    def total_clients_olt(self) -> pd.DataFrame:
        """Totalize clients OLT."""
        return Calculate.total_clients_olt(self.data_asf)
    
    def total_clients_adsl_by_bras(self) -> pd.DataFrame:
        """Totalize clients ADSL by bras."""
        df_total_clients = self.total_clients_adsl()
        return Calculate.total_clients_by_bras(df_total_clients)
    
    def total_clients_mdu_by_bras(self) -> pd.DataFrame:
        """Totalize clients MDU by bras."""
        df_total_clients = self.total_clients_mdu()
        return Calculate.total_clients_by_bras(df_total_clients)

    def total_clients_olt_by_bras(self) -> pd.DataFrame:
        """Totalize clients OLT by bras."""
        df_total_clients = self.total_clients_olt()
        return Calculate.total_clients_by_bras(df_total_clients)
    
    def total_consumption_adsl_by_bras(self) -> pd.DataFrame: #
        """Totalize the consumption by bras only ADSL."""
        df_total_clients_adsl = self.total_clients_adsl_by_bras()
        df_total_clients = self.total_clients_by_bras()
        brasnames = self.data_adsl[NameColumns.BRAS].unique()
        return Calculate.total_consumption_equipment(df_total_clients_adsl, df_total_clients, self.data_consumption, brasnames)
    
    def total_consumption_mdu_by_bras(self) -> pd.DataFrame:
        """Totalize the consumption by bras only MDU."""
        df_total_clients_mdu = self.total_clients_mdu_by_bras()
        df_total_clients = self.total_clients_by_bras()
        brasnames = self.data_mdu[NameColumns.BRAS].unique()
        return Calculate.total_consumption_equipment(df_total_clients_mdu, df_total_clients, self.data_consumption, brasnames)

    def total_consumption_olt_by_bras(self) -> pd.DataFrame:
        """Totalize the consumption by bras only OLT."""
        df_total_clients_asf = self.total_clients_olt_by_bras()
        df_total_clients = self.total_clients_by_bras()
        brasnames = self.data_asf[NameColumns.BRAS].unique()
        return Calculate.total_consumption_equipment(df_total_clients_asf, df_total_clients, self.data_consumption, brasnames)
    
    def total_consumption_state_adsl_by_bras(self) -> pd.DataFrame:
        """Totalize the consumption of each state only ADSL and group by bras."""
        df_consumption_adsl = self.total_consumption_adsl_by_bras()
        df_clients_adsl_by_state = self.total_clients_adsl()
        df_clients_adsl_by_bras = self.total_clients_adsl_by_bras()
        return Calculate.total_consumption_equipment_by_state(df_consumption_adsl, df_clients_adsl_by_state, df_clients_adsl_by_bras)
    
    def total_consumption_state_mdu_by_bras(self) -> pd.DataFrame:
        """Totalize the consumption of each state only MDU and group by bras."""
        df_consumption_mdu = self.total_consumption_mdu_by_bras()
        df_clients_mdu_by_state = self.total_clients_mdu()
        df_clients_mdu_by_bras = self.total_clients_mdu_by_bras()
        return Calculate.total_consumption_equipment_by_state(df_consumption_mdu, df_clients_mdu_by_state, df_clients_mdu_by_bras)

    def total_consumption_state_olt_by_bras(self) -> pd.DataFrame:
        """Totalize the consumption of each state only OLT and group by bras."""
        df_consumption_asf = self.total_consumption_olt_by_bras()
        df_clients_asf_by_state = self.total_clients_olt()
        df_clients_asf_by_bras = self.total_clients_olt_by_bras()
        return Calculate.total_consumption_equipment_by_state(df_consumption_asf, df_clients_asf_by_state, df_clients_asf_by_bras)
    
    def total_consumption_adsl_by_state(self) -> pd.DataFrame:
        """Totalize the consumption group by state only ADSL."""
        df_consumption_adsl_by_state = self.total_consumption_state_adsl_by_bras()
        return Calculate.total_consumption_by_state(df_consumption_adsl_by_state)
    
    def total_consumption_mdu_by_state(self) -> pd.DataFrame:
        """Totalize the consumption group by state only MDU."""
        df_consumption_mdu_by_state = self.total_consumption_state_mdu_by_bras()
        return Calculate.total_consumption_by_state(df_consumption_mdu_by_state)

    def total_consumption_olt_by_state(self) -> pd.DataFrame:
        """Totalize the consumption group by state only OLT."""
        df_consumption_asf_by_state = self.total_consumption_state_olt_by_bras()
        return Calculate.total_consumption_by_state(df_consumption_asf_by_state)