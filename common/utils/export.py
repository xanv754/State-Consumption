from os import getcwd
from tqdm import tqdm
from pandas import DataFrame
from common.utils.file import File

def export_missing_nodes(nodes: list[dict], filename: str="missing_nodes.xlsx") -> None:
    try:
        tqdm.write(f"{len(nodes)} nodes were lost. Exporting...")
        missing_nodes = dict()
        keys = nodes[0].keys()
        for key_name in keys:
            missing_nodes[key_name] = []
            for node in nodes:
                missing_nodes[key_name].append(node[key_name])
        if missing_nodes:
            df = DataFrame(missing_nodes)
            File.write_excel(df, filename)
    except Exception as error:
        pass
        raise error
    
def export_logs(data: list[any], filename: str="logs.log") -> None:
    try:
        tqdm.write(f"{len(data)} logs exporting...")
        pwd = getcwd()
        path = f"{pwd}/{filename}"
        with open(path, "w") as file:
            for log in data:
                file.write(log + "\n")
    except Exception as error:
        raise error