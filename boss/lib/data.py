from os import getenv
from pandas import DataFrame
from dotenv import load_dotenv
from common.utils.file import FileController
from common.constant import filename

load_dotenv(override=True)

REPORT_BOSS = getenv("REPORTBOSS_PATH")

def load_report_boss() -> DataFrame:
    """Load the boss report to get the dataframe."""
    try:
        if ".xlsx" in REPORT_BOSS:
            df = FileController.read_excel(REPORT_BOSS)
            if df.empty:
                raise Exception("Report boss data not found")
            return df
        else:
            raise Exception("Report boss file not found")
    except Exception as error:
        raise error


def save_data_clients(data: DataFrame) -> None:
    """Save the data of Clients x Bras/State.
    
    Parameters
    ----------
    data: DataFrame
        Dataframe for saving in .xlsx format.
    """
    try:
        FileController.write_excel(data, filename=filename.CLIENTS_BY_BRAS)
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
