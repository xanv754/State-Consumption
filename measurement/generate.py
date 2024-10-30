import pandas as pd
from common import FileController, filename as FILE
from measurement.consumption.taccess import TaccessConsumption
from measurement.consumption.external import ExternalConsumption

def get_consumption_by_taccess(process: bool = False) -> pd.DataFrame:
    """Generate the file with the consumption by bras from Taccess API.
    
    Parameters
    ----------
    process: bool, default False
        Flag to save the generated data.
    """
    try:
        Consumption = TaccessConsumption()
        if not Consumption.err:
            df = pd.DataFrame(Consumption.bras)
            if process: FileController.write_excel(df, filename=FILE.COMSUPTION_TACCESS)
            return df
    except Exception as error:
        raise error
    
def get_consumption_by_file(filename: str, sheetname: str = None, process: bool = False) -> pd.DataFrame:
    """Generate the file with the consumption by bras from a file.
    
    Parameters
    ----------
    filename: str
        Filename to be read.
    """
    try:
        if sheetname: df = FileController.read_excel(filename, sheetname=sheetname)
        else: df = FileController.read_excel(filename)
        Consumption = ExternalConsumption(df)
        if not Consumption.err:
            if process: FileController.write_excel(Consumption.data, filename=FILE.CONSUMPTION_EXTERNAL)
            return Consumption.data
    except Exception as error:
        raise error