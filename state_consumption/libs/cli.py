import os
from datetime import datetime
from state_consumption.constants import SheetNames
from state_consumption.libs import AsfReader, BossReader, ConsumptionTrafficReader, ProcessData, ReportHandler
from state_consumption.utils import ExcelExport, terminal, logger


class ReaderCLIHandler:
    @staticmethod
    def inspect_boss(filepath: str) -> None:
        """Inspect the BOSS file."""
        boss = BossReader(filepath)
        if boss.check_reader():
            terminal.print("[green3]BOSS file is valid to process")
        else:
            terminal.print("[red3]BOSS file is not valid to process")

    @staticmethod
    def inspect_asf(filepath: str) -> None:
        """Inspect the ASF file."""
        asf = AsfReader(filepath)
        if asf.check_reader():
            terminal.print("[green3]ASF data is valid to process")
        else:
            terminal.print("[red3]ASF file is not valid to process")

    @staticmethod
    def inspect_consumption(filepath: str, process: bool) -> None:
        """Inspect the consumption file."""
        consumption = ConsumptionTrafficReader(filepath, process=process)
        if consumption.check_reader():
            terminal.print("[green3]Consumption file is valid to process")
        else:
            terminal.print("[red3]Consumption file is not valid to process")


class CLIHandler:
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

    def _get_path(self) -> str:
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
        
        :params filepath: The path of the file to export the data. If None, the data will be exported in the current directory.
        :type filepath: str, optional
        :returns str: The path of the file. None if the data was not exported.
        """
        try:
            consumption = ConsumptionTrafficReader(path=self.bras_path, process=self.process_consumption)
            df_data = consumption.get_data()
            if not filepath:
                path = self._get_path()
                filepath = f"{path}/consumo_bras_totalizado_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
            excel = ExcelExport(filepath)
            excel.export(data=df_data, sheet_name=SheetNames.CONSUMPTION)
            return filepath
        except Exception as error:
            logger.error(f"Ha ocurrido un error al procesar la data de consumo - {error}")
            terminal.print(f"[red3]ERROR: [default]Ha ocurrido un error al procesar la data de consumo - {error}")
            return None
        
    def clients_consumption_by_state(self, filepath: str | None = None) -> str | None:
        """Get the clients and consumption by state.
        
        :params filepath: The path of the file to export the data. If None, the data will be exported in the current directory.
        :type filepath: str, optional
        :returns str: The path of the file. None if the data was not exported.
        """
        try:
            if self.boss_path is None or self.asf_path is None:
                logger.error("Se ha intentado procesar el consumo por estado, pero no se ha encontrado data en el archivo BOSS o ASF")
                terminal.print("[red3]ERROR: [default]Se ha intentado procesar el consumo por estado, pero no se ha encontrado data en el archivo BOSS o ASF")
                return None
            process = ProcessData(self.boss_path, self.bras_path, self.asf_path, self.process_consumption)
            data = ReportHandler(process)
            df_data = data.clients_consumption_by_state()
            df_consumption = process.get_data_consumption()
            if not filepath:
                path = self._get_path()
                filepath = f"{path}/consumo_por_estado_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
            excel = ExcelExport(filepath)
            excel.export(data=df_data, sheet_name=SheetNames.VPTI)
            excel.add(new_data=df_consumption, sheet_name=SheetNames.CONSUMPTION)
            return filepath
        except Exception as error:
            logger.error(f"Ha ocurrido un error al generar el consumo por estado - {error}")
            terminal.print(f"[red3]ERROR: [default]Ha ocurrido un error al generar el consumo por estado - {error}")
            return None
        
    def clients_consumption_by_state_with_percentage(self, filepath: str | None = None) -> str | None:
        """Get the clients and consumption by state with percentage of consumption.
        
        :params filepath: The path of the file to export the data. If None, the data will be exported in the current directory.
        :type filepath: str, optional
        :returns str: The path of the file. None if the data was not exported.
        """
        try:
            if self.boss_path is None or self.asf_path is None: 
                logger.error("Se ha intentado procesar el consumo por estado, pero no se ha encontrado data en el archivo BOSS o ASF")
                terminal.print("[red3]ERROR: [default]Se ha intentado procesar el consumo por estado, pero no se ha encontrado data en el archivo BOSS o ASF")
                return None
            process = ProcessData(self.boss_path, self.bras_path, self.asf_path, self.process_consumption)
            data = ReportHandler(process)
            df_data = data.clients_consumption_by_state_with_percentage()
            df_consumption = process.get_data_consumption()
            if not filepath:
                path = self._get_path()
                filepath = f"{path}/consumo_por_estado_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
            excel = ExcelExport(filepath)
            excel.export(data=df_data, sheet_name=SheetNames.VPTI)
            excel.add(new_data=df_consumption, sheet_name=SheetNames.CONSUMPTION)
            return filepath
        except Exception as error:
            logger.error(f"Ha ocurrido un error al generar el consumo por estado con porcentaje - {error}")
            terminal.print(f"[red3]ERROR: [default]Ha ocurrido un error al generar el consumo por estado con porcentaje - {error}")
            return None
