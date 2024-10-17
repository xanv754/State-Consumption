from os import getenv
from typing import List
from tqdm import tqdm
from dotenv import load_dotenv
from requests import post
from common.utils.date import getFirstDayOfMonth, getLastDayAvailableOfMonth
from common.utils.export import export_logs
from common.utils.validate import validate_name_bras
from common.utils.transform import bits_a_gbps
from measurement.constant import groups
from measurement.model.interface import InterfaceModel


load_dotenv(override=True)

TACCESS = getenv("TACCESS_URL")
EHEALTH = getenv("EHEALTH")

class MeasurementTaccess:
    interfaces: List[InterfaceModel] = []
    bras: dict
    logs = []

    def __init__(self):
        self.__get_data()
        if len(self.logs) <= 0: 
            self.__get_total_in_max()
        else:
            export_logs(self.logs, filename="taccess.log")

    def __get_data(self) -> None:
        payload = {
            "ehealth": EHEALTH,
            "groups": [
                groups.ANZ,
                groups.BOL,
                groups.BTO,
                groups.CHC,
                groups.CNT,
                groups.LMS,
                groups.MAD,
                groups.MAY,
                groups.MBO,
                groups.MIL,
                groups.POD, 
                groups.SCR
            ],
            "firstday": getFirstDayOfMonth(),
            "lastday": getLastDayAvailableOfMonth()
        }
        res = post(f"{TACCESS}/trends", json=payload)
        if res.status_code == 200:
            data = res.json()
            for interface_ in tqdm(data):
                total = len(interface_["times"])
                for i in range(0, total - 1):
                    if validate_name_bras(interface_["interface"]):
                        current_interface = InterfaceModel(
                            name=interface_["interface"].split("_")[0].upper(),
                            time=interface_["times"][i].split("T")[0].replace("-", ""),
                            in_=interface_["in"][i],
                            out=interface_["out"][i],
                            bandwidth=interface_["bandwidth"][i]
                        )
                        self.interfaces.append(current_interface)
                    else:
                        log = f"Invalid bras name: {interface_["interface"]}"
                        if not log in self.logs: self.logs.append(log)
        else:
            log = f"HTTP Error {res.status_code}: {res.text}"
            if not log in self.logs: self.logs.append(log)

    def __get_in_max(self, list_interfaces: List[InterfaceModel]) -> float:
        try:
            values_max: List[float] = []
            in_max = 0
            current_interface: (InterfaceModel | None) = None
            for interface_ in list_interfaces:
                if not current_interface: 
                    current_interface = interface_
                if current_interface and current_interface.time == interface_.time:
                    if interface_.in_ > in_max: in_max = interface_.in_
                elif current_interface:
                    values_max.append(in_max)
                    in_max = 0
            return (sum(values_max) / len(values_max))
        except Exception as error:  
            raise error 

    def __get_total_in_max(self) -> None:
        try:
            bras: List[str] = []
            in_values: List[float] = []
            bras_names = self.get_name_interfaces()
            for name in tqdm(bras_names):
                list_interfaces = self.search_interfaces(name)
                in_max = self.__get_in_max(list_interfaces)
                bras.append(name)
                in_values.append(in_max)
            self.bras = {"BRAS": bras, "IN": in_values}
        except Exception as error:
            raise error
        
    def get_name_interfaces(self) -> List[str]:
        names: List[str] = []
        for current_interface in self.interfaces:
            if current_interface.name not in names: names.append(current_interface.name)
        return names
    
    def search_interfaces(self, name: str) -> List[InterfaceModel]:
        interfaces = []
        for current_interface in self.interfaces:
            if current_interface.name == name:
                interfaces.append(current_interface)
        return interfaces