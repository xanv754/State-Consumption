import pandas as pd
from os import getcwd, listdir, remove
from common.utils.file import File

DATA = [
    {
        "id": 1,
        "central": "central",
        "account_code": "account_code",
        "state": "state",
        "ip": "ip",
        "region": "region",
    },
    {
        "id": 2,
        "central": "central",
        "account_code": "account_code",
        "state": "state",
        "ip": "ip",
        "region": "region",
    },
]


def test_read_csv():
    filepath = f"{getcwd()}/test.csv"
    with open(filepath, "w") as file:
        file.write("id,central,account_code,state,ip,region\n")
        for value in DATA:
            line = f"{value['id']},{value['central']},{value['account_code']},{value['state']},{value['ip']},{value['region']}\n"
            file.write(line)
    file.close()
    df = File.read_csv(filepath, delimiter=",")
    result_test = df.equals(pd.DataFrame(DATA))
    remove(filepath)
    assert result_test


def test_read_excel():
    df_original = pd.DataFrame(DATA)
    filepath = f"{getcwd()}/test.xlsx"
    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
        df_original.to_excel(writer, index=False)
    df = File.read_excel(filepath)
    result_test = df.equals(df_original)
    remove(filepath)
    assert result_test


def test_write_excel():
    df_original = pd.DataFrame(DATA)
    File.write_excel(df_original, filename="test.xlsx")
    filepath = f"{getcwd()}/test.xlsx"
    if "test.xlsx" in listdir(getcwd()):
        df = pd.read_excel(filepath)
        assert df.equals(df_original)
    else:
        assert False
