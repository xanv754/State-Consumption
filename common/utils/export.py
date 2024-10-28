from os import getcwd
from tqdm import tqdm
from pandas import DataFrame
from common.utils.file import FileController


def export_missing_nodes(
    nodes: list[dict], filename: str = "missing_nodes.xlsx"
) -> None:
    """Creates an .xlsx file containing the list of unprocessed nodes.

    Parameters
    ----------
    nodes:
        List of nodes to be exported.
    filename:
        Name of the file to be exported.
    """
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
            FileController.write_excel(df, filename)
    except Exception as error:
        pass
        raise error


def export_logs(data: list[any], filename: str = "logs.log") -> None:
    """Creates a .log file from a list of information.

    Parameters
    ----------
    data:
        List of data to be exported.
    filename:
        Name of the file to be exported.
    """
    try:
        tqdm.write(f"{len(data)} logs exporting...")
        pwd = getcwd()
        path = f"{pwd}/{filename}"
        with open(path, "w") as file:
            for log in data:
                file.write(log + "\n")
    except Exception as error:
        raise error
