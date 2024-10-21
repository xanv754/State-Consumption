from common.utils.file import File
from dotenv import load_dotenv
from os import getenv

load_dotenv(override=True)

FILE_WITH_CONTENT_EXCEL = getenv("FILE_CONTENT_EXCEL")
FILE_WITH_CONTENT_CSV = getenv("FILE_CONTENT_CSV")
FILE_WITH_CONTENT_TXT = getenv("FILE_CONTENT_TXT")


def test_read_excel():
    df = File.read_excel(FILE_WITH_CONTENT_EXCEL)
    assert df.empty == False


def test_read_csv():
    df = File.read_csv(FILE_WITH_CONTENT_CSV)
    assert df.empty == False


def test_read_txt():
    df = File.read_txt(FILE_WITH_CONTENT_TXT)
    assert df.empty == False
