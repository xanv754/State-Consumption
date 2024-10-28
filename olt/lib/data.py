from pandas import DataFrame
from common import FileController, filename

def load_data_olt(filename: str) -> DataFrame:
    """Load the data OLT to get the dataframe.
    
    Parameters
    ----------
    file_name:
        Name of the file to be read.
    """
    if ".xlsx" in filename:
        df = FileController.read_excel(filename)
        if df.empty: raise Exception("Data OLT not found")
    elif ".csv" in filename:
        df = FileController.read_csv(filename)
        if df.empty: raise Exception("Data OLT not found")
    else:
        raise Exception("Data OLT file not valid")
    return df

def save_data_olt(data: DataFrame) -> None:
    """Save the data OLT to a file.
    
    Parameters
    ----------
    data: DataFrame
        Dataframe for saving in .xlsx format.
    """
    try:
        FileController.write_excel(data, filename=filename.OLT_TOTAL)
    except Exception as error:
        raise error