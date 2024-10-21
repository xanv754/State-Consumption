from os import getenv
from dotenv import load_dotenv
from pandas import DataFrame
from common.utils.file import File

load_dotenv(override=True)

MASTERNODO = getenv("MASTERNODO_PATH")


def upload_file() -> DataFrame:
    if MASTERNODO:
        df = File.read_excel(MASTERNODO)
        if df.empty:
            raise Exception("Data not found")
        return df
    else:
        raise Exception("There is no file to update")
