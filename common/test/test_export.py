import pandas as pd
from os import getcwd, listdir, remove
from common.utils.export import export_logs, export_missing_nodes

NODES = [
    {
        "id": 1, 
        "central": "central", 
        "account_code": "account_code", 
        "state": "state", 
        "ip": "ip", 
        "region": "region"
    },
    {
        "id": 2, 
        "central": "central", 
        "account_code": "account_code", 
        "state": "state", 
        "ip": "ip", 
        "region": "region"
    }
]

DATA = [
    "This is example .log file",
    "Make sure to delete it after testing"
]

def test_export_logs():
    export_logs(DATA, filename="test.log")
    filepath = f"{getcwd()}/test.log"
    if "test.log" in listdir(getcwd()): 
        result_test = True
        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                if line not in DATA: 
                    result_test = False
            file.close()
        remove(filepath)
        assert result_test
    else: assert False

def test_export_missing_nodes():
    df_original = pd.DataFrame(NODES)
    export_missing_nodes(NODES, filename="test.xlsx")
    filepath = f"{getcwd()}/test.xlsx"
    if "test.xlsx" in listdir(getcwd()):
        df = pd.read_excel(filepath)
        result_test = df.equals(df_original)
        remove(filepath)
        assert result_test
    else: assert False

test_export_missing_nodes()