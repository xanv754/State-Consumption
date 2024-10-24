from os import getenv
from pandas import DataFrame
from dotenv import load_dotenv
from common import FileController, filename

load_dotenv(override=True)

REPORT_BOSS = getenv("REPORTBOSS_PATH")

def load_report_boss(filename: str) -> DataFrame:
    """Load the boss report to get the dataframe."""
    try:
        if ".xlsx" in REPORT_BOSS:
            df = FileController.read_excel(filename)
            if df.empty:
                raise Exception("Report boss data not found")
            return df
        else:
            raise Exception("Report boss file not found")
    except Exception as error:
        raise error

def load_file(filename: str) -> DataFrame:
    """Load the file to get the dataframe.
    
    Parameters
    ----------
    filepath:
        Path of the file to be read.
    """
    if ".xlsx" in filename:
        df = FileController.read_excel(filename)
        if df.empty: raise Exception("Data not found")
    elif ".csv" in filename:
        df = FileController.read_csv(filename)
        if df.empty: raise Exception("Data not found")
    else:
        raise Exception("Data file not valid")
    return df

def save_data_clients(data: DataFrame) -> None:
    """Save the data of Clients x Bras/State.
    
    Parameters
    ----------
    data: DataFrame
        Dataframe for saving in .xlsx format.
    """
    try:
        FileController.write_excel(data, filename=filename.CLIENTS_BY_BRAS_ADSL)
    except Exception as error:
        raise error


def save_new_report_boss(data: DataFrame) -> None:
    """Save the boss report with states.
    
    Parameters
    ----------
    data: DataFrame
        Dataframe for saving in .xlsx format.
    """
    try:
        FileController.write_excel(data, filename=filename.NEW_REPORT_BOSS)
    except Exception as error:
        raise error
    

def save_report_by_equipment(data_adsl: DataFrame = DataFrame(), data_mdu: DataFrame = DataFrame()) -> None:
    """Save the reports filtered by equipment.
    
    Parameters
    ----------
    data_adsl: DataFrame
        Data of ADSL equipment.
    data_mdu: DataFrame
        Data of MDU equipment.
    """
    try:
        if not data_adsl.empty:
            FileController.write_excel(data_adsl, filename=filename.NEW_REPORT_ADSL)
        if not data_mdu.empty:
            FileController.write_excel(data_mdu, filename=filename.NEW_REPORT_MDU)
    except Exception as error:
        raise error


def save_data_porcentage(data: DataFrame) -> None:
    """Save the data of Clients x Bras/State, but with percentages values.
    
    Parameters
    ----------
    data: DataFrame
        Dataframe for saving in .xlsx format.
    """
    try:
        FileController.write_excel(data, filename=filename.PORCENTAGE)
    except Exception as error:
        raise error
    
def save_data_adsl_porcentage(data: DataFrame) -> None:
    """Save the data of ADSL clients x Bras/State, but with percentages values.
    
    Parameters
    ----------
    data: DataFrame
        Dataframe for saving in .xlsx format.
    """
    try:
        FileController.write_excel(data, filename=filename.ADSL_PORCENTAGE)
    except Exception as error:
        raise error
    
def save_data_mdu_porcentage(data: DataFrame) -> None:
    """Save the data of MDU clients x Bras/State, but with percentages values.
    
    Parameters
    ----------
    data: DataFrame
        Dataframe for saving in .xlsx format.
    """
    try:
        FileController.write_excel(data, filename=filename.MDU_PORCENTAGE)
    except Exception as error:
        raise error
