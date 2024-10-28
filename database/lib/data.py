from os import getenv
from dotenv import load_dotenv
from pandas import DataFrame
from common import FileController

load_dotenv(override=True)

MASTERNODO = getenv("MASTERNODO_PATH")

def upload_file() -> DataFrame:
    """Load the masternodo to get the dataframe."""
    if MASTERNODO:
        df = FileController.read_excel(MASTERNODO)
        if df.empty:
            raise Exception("Data not found")
        return df
    else:
        raise Exception("There is no file to update")
