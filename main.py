import click
import pandas as pd
from typing import List
from tqdm import tqdm
from common import filename, FileController, colname, add_total_sum_by_col, add_total_sum_by_row, states as GLOBAL
from measurement import interface as INTERFACE

@click.group()
def cli():
    """CONSUMPTION OF CLIENTS BY BRAS AND STATE

    \b
    Arguments:
      total -p [PORCENTAGE_CLIENTS_FILE] -c [CONSUMPTION_BRAS_FILE]  The file extension must be .xlsx
    """
    pass

if __name__ == "__main__":
    try:
        cli()
    except SystemExit as error:
        if error == 1:
            pass
    except Exception as error:
        click.echo(error)