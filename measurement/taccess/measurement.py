from os import getenv
from typing import List
from tqdm import tqdm
from dotenv import load_dotenv
from requests import post, exceptions
from urllib3.util import request
from urllib3.util.timeout import Timeout
from common.utils.date import getFirstDayOfMonth, getLastDayAvailableOfMonth
from common.utils.export import export_logs
from common.utils.validate import validate_name_bras
from common.utils.transform import bits_a_gbps
from measurement.constant import groups
from measurement.model.interface import InterfaceModel
from common.utils.file import File


load_dotenv(override=True)

TACCESS = getenv("TACCESS_URL")
EHEALTH = getenv("EHEALTH")

class MeasurementTaccess:
    interfaces: List[InterfaceModel] = []
    bras: dict
    err: bool = False
    logs = []

    def __init__(self):
        self.__get_data()
        if len(self.logs) <= 0:
            # with open("/home/angyee/medi-clients/taccess_consumo", "w") as file:
            #     file.write("interface,time,in,out,bandwidth\n")
            #     for interface_ in self.interfaces:
            #         file.write(f"{interface_.name},{interface_.time},{interface_.in_},{interface_.out},{interface_.bandwidth}\n")
            self.__generate_usage_data()
        else:
            export_logs(self.logs, filename="taccess.log")

    def __get_data(self) -> None:
        """Performs an HTTP post request to the Taccess server to obtain 
        the hourly consumption of all BRAS interfaces.

        If the query fails, it will export a .log with the errors.
        """
        try:
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
            res = post(f"{TACCESS}/trends", json=payload, timeout=20)
            if res.status_code == 200:
                data = res.json()
                for interface_ in tqdm(data):
                    total = len(interface_["times"])
                    for i in range(0, total - 1):
                        if validate_name_bras(interface_["interface"]):
                            current_interface = InterfaceModel(
                                name=interface_["interface"],
                                time=interface_["times"][i].split("T")[0].replace("-", ""),
                                in_=bits_a_gbps(interface_["in"][i]),
                                out=bits_a_gbps(interface_["out"][i]),
                                bandwidth=interface_["bandwidth"][i]
                            )
                            self.interfaces.append(current_interface)
                        else:
                            self.err = True
                            log = f"Invalid bras name: {interface_["interface"]}"
                            if not log in self.logs: self.logs.append(log)
            else:
                self.err = True
                log = f"HTTP Error {res.status_code}: {res.text}"
                if not log in self.logs: self.logs.append(log)
        except exceptions.Timeout:
            self.err = True
            log = "HTTP Error: Connect timeout"
            self.logs.append(log)
        except Exception as error:
            self.err = True
            raise error

    def __generate_usage_data(self) -> None:
        """Generates traffic consumption data from BRAS.

        Note: The maximum consumption values (In max) are used.
        """
        try:
            bras: List[str] = []
            total_in_max: List[float] = []
            bras_names = self.get_name_bras()
            for bras_name in tqdm(bras_names):
                values_max: List[float] = []
                bras_interfaces = self.filter_by_bras_name(bras_name)
                interfaces_names = self.get_name_interfaces(bras_interfaces)
                for interface_name in interfaces_names:
                    interfaces = self.filter_by_interface_name(interface_name, interfaces=bras_interfaces)
                    in_max = self.get_in_max(interfaces)
                    values_max.append(in_max)
                bras.append(bras_name)
                total_in_max.append(sum(values_max))
            self.bras = {"BRAS": bras, "IN": total_in_max}
        except Exception as error:
            raise error

    def get_in_max(self, interfaces: List[InterfaceModel]) -> float:
        """Returns the maximum value of a list of interfaces.

        Parameters
        ----------
        list_interfaces:
            List of interfaces.
        """
        try:
            in_max = 0
            current_interface: (InterfaceModel | None) = None
            for interface_ in interfaces:
                if not current_interface:
                    current_interface = interface_
                if current_interface and current_interface.time == interface_.time:
                    if interface_.in_ > in_max: in_max = interface_.in_
            return in_max
        except Exception as error:
            raise error

    def get_name_bras(self) -> List[str]:
        """Returns a list of all BRAS names unique."""
        names: List[str] = []
        for interface_ in self.interfaces:
            current_name = interface_.name.split("_")[0].upper()
            if current_name not in names: names.append(current_name)
        return names
    
    def get_name_interfaces(self, interfaces: List[InterfaceModel]) -> List[str]:
        """Returns a list of all interfaces names unique."""
        names: List[str] = []
        for interface_ in interfaces:
            if interface_.name not in names: names.append(interface_.name)
        return names
    
    def filter_by_interface_name(self, name: str, interfaces: (List[InterfaceModel] | None) = None) -> List[InterfaceModel]:
        """Returns a list of interface filters for a given interface name.

        Parameters
        ----------
        name:
            Name of the BRAS.
        interfaces: default None
            List of interfaces to be filtered. 
        """
        filtered_interfaces = []
        if not interfaces:
            for current_interface in self.interfaces:
                if current_interface.name == name:
                    filtered_interfaces.append(current_interface)
        else:
            for current_interface in interfaces:
                if current_interface.name == name:
                    filtered_interfaces.append(current_interface)
        return filtered_interfaces
    
    def filter_by_bras_name(self, name: str, interfaces: (List[InterfaceModel] | None) = None) -> List[InterfaceModel]:
        """Returns a list of interface filters given the name of a BRAS.

        Parameters
        ----------
        name:
            Name of the BRAS.
        interfaces: default None
            List of interfaces to be filtered.
        """
        filtered_interfaces = []
        if not interfaces:
            for current_interface in self.interfaces:
                current_name = current_interface.name.split("_")[0].upper()
                if current_name == name:
                    filtered_interfaces.append(current_interface)
        else:
            for current_interface in interfaces:
                current_name = current_interface.name.split("_")[0].upper()
                if current_name == name:
                    filtered_interfaces.append(current_interface)
        return filtered_interfaces
