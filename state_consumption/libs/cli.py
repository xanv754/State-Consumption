import os
import rich
from datetime import datetime
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from constants.sheetnames import SheetNames
from database.libs.mongo import MongoDatabase
from database.querys.nodes import NodesQueryMongo
from database.model.node import NodeModel
from database.updater import UpdaterDatabase
from libs.process.data import DataHandler
from libs.process.process import ProcessHandler
from libs.reader.traffic import ConsumptionTrafficReader
from libs.reader.boss import BossReader
from libs.reader.asf import AsfReader
from utils.data.excel import ExcelExport
from utils.data.format import FixFormat


class ReaderCLIHandler:

    @staticmethod
    def inspect_boss(filepath: str) -> None:
        """Inspect the BOSS file."""
        boss = BossReader(filepath)
        if boss.check_reader():
            rich.print("[green3]BOSS data is valid to process")
        else:
            rich.print("[red3]BOSS file is not valid to process")

    @staticmethod
    def inspect_asf(filepath: str) -> None:
        """Inspect the ASF file."""
        asf = AsfReader(filepath)
        if asf.check_reader():
            rich.print("[green3]ASF file is valid to process")
        else:
            rich.print("[red3]ASF file is not valid to process")

    @staticmethod
    def inspect_consumption(filepath: str, process: bool) -> None:
        """Inspect the consumption file."""
        consumption = ConsumptionTrafficReader(filepath, process=process)
        if consumption.check_reader():
            rich.print("[green3]Consumption file is valid to process")
        else:
            rich.print("[red3]Consumption file is not valid to process")

class DatabaseCLIHandler:
    """Handler to operate with the database to CLI."""

    def make_migration(self) -> bool:
        mongo = MongoDatabase()
        if mongo.connected:
            return mongo.migration()
        
    def rollback(self) -> bool:
        mongo = MongoDatabase()
        if mongo.connected:
            return mongo.rollback()
        
    def add_new_node(self) -> bool:
        state = Prompt.ask("State of new node")
        if not state: 
            rich.print("[yellow2]Warning: State of node is required")
            return False
        state = FixFormat.word(state)
        central = Prompt.ask("Central of new node")
        if not central: 
            rich.print("[yellow2]Warning: Central of node is required")
            return False
        central = FixFormat.word(central)
        account_code = Prompt.ask("Account code of new node")
        if not account_code: 
            rich.print("[yellow2]Warning: Account code of node is required")
            return False
        ip = Prompt.ask("IP of new node")
        if not ip: ip = None
        else: ip = FixFormat.ip(ip)
        region = Prompt.ask("Region of new node")
        if not region: region = None
        else: region = FixFormat.word(region)
        new_node = NodeModel(
            state=state, 
            central=central, 
            account_code=account_code, 
            ip=ip, 
            region=region
        )
        
        console = Console()
        console.clear()
        table = Table(title="New node")
        table.add_column("Field", justify="right", style="cyan", no_wrap=True)
        table.add_column("Value", justify="left", style="yellow")
        table.add_row("State", new_node.state)
        table.add_row("Central", new_node.central)
        table.add_row("Account code", new_node.account_code)
        table.add_row("IP", new_node.ip)
        table.add_row("Region", new_node.region)
        console.print(table)

        response = Prompt.ask("Are you sure you want to add this node to the database? (y/N)")
        if not response or response.lower() != "y": exit(0)

        return NodesQueryMongo.insert_one(node=new_node)
    
    def update_database(self, filepath: str, delimiter: str) -> bool:
        """Update the database extracted the data from the CSV or XLSX file.
        
        Parameters
        ----------
        filepath : str
            The path of the file to update the database.
        """
        updaterHandler = UpdaterDatabase(filepath, delimiter=delimiter)
        status = updaterHandler.update()
        return status
    

class ExportCLIHandler:
    """Handler to process and export the data to CLI."""

    boss_path: str | None
    asf_path: str | None
    bras_path: str
    process_consumption: bool

    def __init__(self, boss_path: str | None, asf_path: str | None, bras_path: str, process_consumption: bool) -> None:
        self.boss_path = boss_path
        self.asf_path = asf_path
        self.bras_path = bras_path
        self.process_consumption = process_consumption

    def __get_path(self) -> str:
        """Get the filepath to export the data."""
        home = os.path.expanduser('~')
        if os.path.exists(f"{home}/Descargas"):
            return f"{home}/Descargas"
        elif os.path.exists(f"{home}/Downloads"):
            return f"{home}/Downloads"
        else:
            return f"./"
        
    def consumtion_bras(self, filepath: str | None = None) -> str | None:
        """Get the clients and consumption by bras.
        
        Parameters
        ----------
        filepath : str, optional
            The path of the file to export the data. If None, the data will be exported in the current directory.
        
        Returns
        -------
        str
            The path of the file. None if the data was not exported.
        """
        try:
            consumption = ConsumptionTrafficReader(path=self.bras_path, process=self.process_consumption)
            df_data = consumption.get_data()
            if not filepath:
                path = self.__get_path()
                filepath = f"{path}/consumo_bras_totalizado_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
            excel = ExcelExport(filepath)
            excel.export(data=df_data, sheet_name=SheetNames.CONSUMPTION)
            return filepath
        except Exception as error:
            print(error, __file__)
            return None

    def clients_consumption_adsl_by_state(self, filepath: str | None = None) -> str | None:
        """Get the clients and consumption ADSL by state.
        
        Parameters
        ----------
        filepath : str, optional
            The path of the file to export the data. If None, the data will be exported in the current directory.

        Returns
        -------
        str
            The path of the file. None if the data was not exported.
        """
        try:
            if self.boss_path is None or self.asf_path is None: 
                rich.print("[red3]Missing BOSS or ASF file")
                return None
            process = ProcessHandler(self.boss_path, self.bras_path, self.asf_path, self.process_consumption)
            data = DataHandler(process)
            df_data = data.clients_consumption_adsl_by_state()
            df_consumption = process.get_data_consumption()
            if not filepath:
                path = self.__get_path()
                filepath = f"{path}/consumo_adsl_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
            excel = ExcelExport(filepath)
            excel.export(data=df_data, sheet_name=SheetNames.ADSL)
            excel.add(new_data=df_consumption, sheet_name=SheetNames.CONSUMPTION)
            return filepath
        except Exception as error:
            print(error, __file__)
            return None
        
    def clients_consumption_adsl_by_state_with_percentage(self, filepath: str | None = None) -> str | None:
        """Get the clients and consumption ADSL by state percentage of consumption.
        
        Parameters
        ----------
        filepath : str, optional
            The path of the file to export the data. If None, the data will be exported in the current directory.

        Returns
        -------
        str
            The path of the file. None if the data was not exported.
        """
        try:
            if self.boss_path is None or self.asf_path is None: 
                rich.print("[red3]Missing BOSS or ASF file")
                return None
            process = ProcessHandler(self.boss_path, self.bras_path, self.asf_path, self.process_consumption)
            data = DataHandler(process)
            df_data = data.clients_consumption_adsl_by_state_with_percentage()
            df_consumption = process.get_data_consumption()
            if not filepath:
                path = self.__get_path()
                filepath = f"{path}/consumo_adsl_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
            excel = ExcelExport(filepath)
            excel.export(data=df_data, sheet_name=SheetNames.ADSL)
            excel.add(new_data=df_consumption, sheet_name=SheetNames.CONSUMPTION)
            return filepath
        except Exception as error:
            print(error, __file__)
            return None
        
    def clients_consumption_mdu_by_state(self, filepath: str | None = None) -> str | None:
        """Get the clients and consumption MDU by state.
        
        Parameters
        ----------
        filepath : str, optional
            The path of the file to export the data. If None, the data will be exported in the current directory.

        Returns
        -------
        str
            The path of the file. None if the data was not exported.
        """
        try:
            if self.boss_path is None or self.asf_path is None: 
                rich.print("[red3]Missing BOSS or ASF file")
                return None
            process = ProcessHandler(self.boss_path, self.bras_path, self.asf_path, self.process_consumption)
            data = DataHandler(process)
            df_data = data.clients_consumption_mdu_by_state()
            df_consumption = process.get_data_consumption()
            if not filepath:
                path = self.__get_path()
                filepath = f"{path}/consumo_mdu_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
            excel = ExcelExport(filepath)
            excel.export(data=df_data, sheet_name=SheetNames.MDU)
            excel.add(new_data=df_consumption, sheet_name=SheetNames.CONSUMPTION)
            return filepath
        except Exception as error:
            print(error, __file__)
            return None
        
    def clients_consumption_mdu_by_state_with_percentage(self, filepath: str | None = None) -> str | None:
        """Get the clients and consumption MDU by state percentage of consumption.
        
        Parameters
        ----------
        filepath : str, optional
            The path of the file to export the data. If None, the data will be exported in the current directory.

        Returns
        -------
        str
            The path of the file. None if the data was not exported.
        """
        try:
            if self.boss_path is None or self.asf_path is None: 
                rich.print("[red3]Missing BOSS or ASF file")
                return None
            process = ProcessHandler(self.boss_path, self.bras_path, self.asf_path, self.process_consumption)
            data = DataHandler(process)
            df_data = data.clients_consumption_mdu_by_state_with_percentage()
            df_consumption = process.get_data_consumption()
            if not filepath:
                path = self.__get_path()
                filepath = f"{path}/consumo_mdu_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
            excel = ExcelExport(filepath)
            excel.export(data=df_data, sheet_name=SheetNames.MDU)
            excel.add(new_data=df_consumption, sheet_name=SheetNames.CONSUMPTION)
            return filepath
        except Exception as error:
            print(error, __file__)
            return None
        
    def clients_consumption_olt_by_state(self, filepath: str | None = None) -> str | None:
        """Get the clients and consumption OLT by state.
        
        Parameters
        ----------
        filepath : str, optional
            The path of the file to export the data. If None, the data will be exported in the current directory.

        Returns
        -------
        str
            The path of the file. None if the data was not exported.
        """
        try:
            if self.boss_path is None or self.asf_path is None: 
                rich.print("[red3]Missing BOSS or ASF file")
                return None
            process = ProcessHandler(self.boss_path, self.bras_path, self.asf_path, self.process_consumption)
            data = DataHandler(process)
            df_data = data.clients_consumption_olt_by_state()
            df_consumption = process.get_data_consumption()
            if not filepath:
                path = self.__get_path()
                filepath = f"{path}/consumo_olt_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
            excel = ExcelExport(filepath)
            excel.export(data=df_data, sheet_name=SheetNames.OLT)
            excel.add(new_data=df_consumption, sheet_name=SheetNames.CONSUMPTION)
            return filepath
        except Exception as error:
            print(error, __file__)
            return None
        
    def clients_consumption_olt_by_state_with_percentage(self, filepath: str | None = None) -> str | None:
        """Get the clients and consumption OLT by state with percentage of consumption.
        
        Parameters
        ----------
        filepath : str, optional
            The path of the file to export the data. If None, the data will be exported in the current directory.

        Returns
        -------
        str
            The path of the file. None if the data was not exported.
        """
        try:
            if self.boss_path is None or self.asf_path is None: 
                rich.print("[red3]Missing BOSS or ASF file")
                return None
            process = ProcessHandler(self.boss_path, self.bras_path, self.asf_path, self.process_consumption)
            data = DataHandler(process)
            df_data = data.clients_consumption_olt_by_state_with_percentage()
            df_consumption = process.get_data_consumption()
            if not filepath:
                path = self.__get_path()
                filepath = f"{path}/consumo_olt_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
            excel = ExcelExport(filepath)
            excel.export(data=df_data, sheet_name=SheetNames.OLT)
            excel.add(new_data=df_consumption, sheet_name=SheetNames.CONSUMPTION)
            return filepath
        except Exception as error:
            print(error, __file__)
            return None
        
    def clients_consumption_by_state(self, filepath: str | None = None) -> str | None:
        """Get the clients and consumption by state.
        
        Parameters
        ----------
        filepath : str, optional
            The path of the file to export the data. If None, the data will be exported in the current directory.

        Returns
        -------
        str
            The path of the file. None if the data was not exported.
        """
        try:
            if self.boss_path is None or self.asf_path is None: 
                rich.print("[red3]Missing BOSS or ASF file")
                return None
            process = ProcessHandler(self.boss_path, self.bras_path, self.asf_path, self.process_consumption)
            data = DataHandler(process)
            df_data = data.clients_consumption_by_state()
            df_consumption = process.get_data_consumption()
            if not filepath:
                path = self.__get_path()
                filepath = f"{path}/consumo_por_estado_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
            excel = ExcelExport(filepath)
            excel.export(data=df_data, sheet_name=SheetNames.VPTI)
            excel.add(new_data=df_consumption, sheet_name=SheetNames.CONSUMPTION)
            return filepath
        except Exception as error:
            print(error, __file__)
            return None
        
    def clients_consumption_by_state_with_percentage(self, filepath: str | None = None) -> str | None:
        """Get the clients and consumption by state with percentage of consumption.
        
        Parameters
        ----------
        filepath : str, optional
            The path of the file to export the data. If None, the data will be exported in the current directory.

        Returns
        -------
        str
            The path of the file. None if the data was not exported.
        """
        try:
            if self.boss_path is None or self.asf_path is None: 
                rich.print("[red3]Missing BOSS or ASF file")
                return None
            process = ProcessHandler(self.boss_path, self.bras_path, self.asf_path, self.process_consumption)
            data = DataHandler(process)
            df_data = data.clients_consumption_by_state_with_percentage()
            df_consumption = process.get_data_consumption()
            if not filepath:
                path = self.__get_path()
                filepath = f"{path}/consumo_por_estado_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
            excel = ExcelExport(filepath)
            excel.export(data=df_data, sheet_name=SheetNames.VPTI)
            excel.add(new_data=df_consumption, sheet_name=SheetNames.CONSUMPTION)
            return filepath
        except Exception as error:
            print(error, __file__)
            return None
