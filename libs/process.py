import pandas as pd
from reader.constants.columns import BossNewNameColumns, TrafficNewNameColumns
from reader.constants.equipment import EquipmentModelConstant
from reader.boss import BossReader
from reader.asf import AsfReader
from reader.traffic import ConsumptionTrafficReader


class DataProcess:
    """Class to process the data."""

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
        columns_required = [BossNewNameColumns.BRAS, BossNewNameColumns.STATE, BossNewNameColumns.TOTAL_CLIENTS]
        df = df[columns_required]
        df = df.reset_index(drop=True)
        return df
    
    def __mdu_filter(self, df: pd.DataFrame) -> None:
        """Get the MDU from the dataframe."""
        df = df[df[BossNewNameColumns.EQUIPMENT] == EquipmentModelConstant.MDU]
        columns_required = [BossNewNameColumns.BRAS, BossNewNameColumns.STATE, BossNewNameColumns.TOTAL_CLIENTS]
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
        
    def total_clients_adsl_by_state(self) -> pd.DataFrame:
        """Totalize clients columns in the data of ADSL by bras and state."""
        df = self.data_adsl.copy()
        df = df.groupby([BossNewNameColumns.BRAS, BossNewNameColumns.STATE]).sum()
        df[BossNewNameColumns.TOTAL_CLIENTS] = df[BossNewNameColumns.TOTAL_CLIENTS].round(2)
        df =  df.reset_index()
        return df
    
    def total_clients_adsl_by_bras(self) -> pd.DataFrame:
        """Totalize clients columns in the data of ADSL by bras and state."""
        df = self.total_clients_adsl_by_state().copy()
        df.drop(columns=[BossNewNameColumns.STATE], inplace=True)
        df = df.groupby(BossNewNameColumns.BRAS).sum()
        df[BossNewNameColumns.TOTAL_CLIENTS] = df[BossNewNameColumns.TOTAL_CLIENTS].round(2)
        df =  df.reset_index()
        return df
    
    def total_clients_mdu_by_state(self) -> pd.DataFrame:
        """Totalize clients columns in the data of MDU by bras and state."""
        df = self.data_mdu
        df = df.groupby([BossNewNameColumns.BRAS, BossNewNameColumns.STATE]).sum()
        df[BossNewNameColumns.TOTAL_CLIENTS] = df[BossNewNameColumns.TOTAL_CLIENTS].round(2)
        df =  df.reset_index()
        return df
    
    def total_clients_by_bras(self) -> pd.DataFrame:
        """Total clients by bras."""
        df_total_adsl = self.total_clients_adsl_by_state()
        df_total_mdu = self.total_clients_mdu_by_state()
        df_unite = pd.concat([df_total_adsl, df_total_mdu], axis=0)
        df_total = df_unite.groupby(BossNewNameColumns.BRAS).sum()
        df_total.drop(columns=[BossNewNameColumns.STATE], inplace=True)
        df_total = df_total.reset_index()
        return df_total
    
    def total_consumption_adsl_by_bras(self) -> pd.DataFrame:
        """Get the consumption ADSL by bras."""
        try:
            new_data = {
                BossNewNameColumns.BRAS: [],
                TrafficNewNameColumns.CONSUMPTION: []
            }
            df_adsl_by_bras = self.total_clients_adsl_by_bras()
            df_total_bras = self.total_clients_by_bras()

            bras = self.data_adsl[TrafficNewNameColumns.BRAS].unique()
            for name in bras:
                total_clients_adsl = df_adsl_by_bras[df_adsl_by_bras[BossNewNameColumns.BRAS] == name][BossNewNameColumns.TOTAL_CLIENTS].iloc[0]
                total_clients_bras = df_total_bras[df_total_bras[BossNewNameColumns.BRAS] == name][BossNewNameColumns.TOTAL_CLIENTS].iloc[0]
                total_consumption_bras = self.data_consumption[self.data_consumption[TrafficNewNameColumns.BRAS] == name][TrafficNewNameColumns.CONSUMPTION].iloc[0].round(2)
                print(total_clients_adsl, total_consumption_bras, total_clients_bras)
                total_consumption_adsl_bras = (total_clients_adsl * total_consumption_bras) / total_clients_bras
                new_data[BossNewNameColumns.BRAS].append(name)
                new_data[TrafficNewNameColumns.CONSUMPTION].append(total_consumption_adsl_bras.round(2))
            
            df = pd.DataFrame(new_data)
            return df
        except Exception as error:
            print(error, __file__)
            exit(1)

    def total_consumption_adsl_by_state(self) -> pd.DataFrame:
        """Get the consumption ADSL by state."""
        try:
            new_data = {
                BossNewNameColumns.BRAS: [],
                BossNewNameColumns.STATE: [],
                TrafficNewNameColumns.CONSUMPTION: []
            }
            df_consumption_adsl = self.total_consumption_adsl_by_bras()
            df_clients_adsl_by_state = self.total_clients_adsl_by_state()
            df_clients_adsl_by_bras = self.total_clients_adsl_by_bras()

            for index, row in df_clients_adsl_by_state.iterrows():
                bras = row[BossNewNameColumns.BRAS]
                state = row[BossNewNameColumns.STATE]
                total_clients = row[BossNewNameColumns.TOTAL_CLIENTS]
                total_clients_bras = df_clients_adsl_by_bras[df_clients_adsl_by_bras[BossNewNameColumns.BRAS] == bras][BossNewNameColumns.TOTAL_CLIENTS].iloc[0]
                total_consumption = df_consumption_adsl[df_consumption_adsl[TrafficNewNameColumns.BRAS] == bras][TrafficNewNameColumns.CONSUMPTION].iloc[0]
                total_consumption_by_state = (total_clients * total_consumption) / total_clients_bras
                new_data[BossNewNameColumns.BRAS].append(bras)
                new_data[BossNewNameColumns.STATE].append(state)
                new_data[TrafficNewNameColumns.CONSUMPTION].append(total_consumption_by_state.round(2))
            
            df = pd.DataFrame(new_data)
            return df
        except Exception as error:
            print(error, __file__)
            exit(1)

    def process(self) -> pd.DataFrame:
        """Process the data."""
        consumption_adsl = self.total_consumption_adsl_by_state()
        return consumption_adsl
            

if __name__ == "__main__":
    boss_path = "./clientes.xlsx"
    consumption_path = "./consumo.xlsx"
    processHandler = DataProcess(boss_path, consumption_path, process_consumption=True)
    print(processHandler.process())