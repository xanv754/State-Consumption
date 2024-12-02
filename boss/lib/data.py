from pandas import DataFrame
from common import FileController, filename

def save_data_clients(data: DataFrame) -> None:
    """Save the data of Clients x Bras/State.
    
    Parameters
    ----------
    data: DataFrame
        Dataframe for saving in .xlsx format.
    """
    try:
        FileController.write_excel(data, filename=filename.CLIENTS)
    except Exception as error:
        raise error
    
def save_data_clients_adsl(data: DataFrame) -> None:
    """Save the data of Clients x Bras/State.
    
    Parameters
    ----------
    data: DataFrame
        Dataframe for saving in .xlsx format.
    """
    try:
        FileController.write_excel(data, filename=filename.ADSL_CLIENTS)
    except Exception as error:
        raise error
    
def save_data_clients_mdu(data: DataFrame) -> None:
    """Save the data of Clients x Bras/State.
    
    Parameters
    ----------
    data: DataFrame
        Dataframe for saving in .xlsx format.
    """
    try:
        FileController.write_excel(data, filename=filename.MDU_CLIENTS)
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
            FileController.write_excel(data_adsl, filename=filename.ADSL_REPORT_BOSS)
        if not data_mdu.empty:
            FileController.write_excel(data_mdu, filename=filename.MDU_REPORT_BOSS)
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
    
def save_data_porcentage_adsl(data: DataFrame) -> None:
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
    
def save_data_porcentage_mdu(data: DataFrame) -> None:
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

def save_data_consumption(data: DataFrame) -> None:
    """Save the data consumption by state.
    
    Parameters
    ----------
    data: DataFrame
        Dataframe for saving in .xlsx format.
    """
    try:
        FileController.write_excel(data, filename=filename.CONSUMPTION)
    except Exception as error:
        raise error
    
def save_data_consumption_adsl(data: DataFrame) -> None:
    """Save the data consumption by state.
    
    Parameters
    ----------
    data: DataFrame
        Dataframe for saving in .xlsx format.
    """
    try:
        FileController.write_excel(data, filename=filename.ADSL_CONSUMPTION)
    except Exception as error:
        raise error
    
def save_data_consumption_mdu(data: DataFrame) -> None:
    """Save the data consumption by state.
    
    Parameters
    ----------
    data: DataFrame
        Dataframe for saving in .xlsx format.
    """
    try:
        FileController.write_excel(data, filename=filename.MDU_CONSUMPTION)
    except Exception as error:
        raise error
    
def save_data_clients_by_bras(data: DataFrame) -> None:
    """Save the data of Clients x Bras.

    Parameters
    ----------
    data: DataFrame
        Dataframe for saving in .xlsx format.
    """
    try:
        FileController.write_excel(data, filename=filename.CLIENTS_BY_BRAS)
    except Exception as error:
        raise error