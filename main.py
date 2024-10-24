import click
import pandas as pd
from typing import List
from tqdm import tqdm
from common import filename, FileController, colname, add_total_sum_by_col, add_total_sum_by_row, states as GLOBAL
from measurement import interface as INTERFACE

def total_adsl_mdu(fileporcentage: str, fileconsumption: str) -> None:
    try:
        PORCENTAGE = fileporcentage
        MEASUREMENT = fileconsumption
        df_porcentage = FileController.read_excel(PORCENTAGE)
        df_measurement = FileController.read_excel(MEASUREMENT)
        df_porcentage = df_porcentage.drop(df_porcentage.index[-1])
        df = pd.DataFrame({colname.STATE: GLOBAL.states})
        if not df_porcentage.empty and not df_measurement.empty:
            for _index, row in tqdm(df_measurement.iterrows(), total=df_measurement.shape[0]):
                current_bras = str(row[colname.BRAS]).lower()
                if current_bras in df_porcentage.columns.to_list():
                    total = row[INTERFACE.IN]
                    porcentage = df_porcentage[current_bras]
                    new_values: List[float] = []
                    for value in porcentage:
                        new_porcentage = value * total
                        new_values.append(round(new_porcentage, 2))
                    df[current_bras] = new_values
        df = add_total_sum_by_col(df, colname.TOTAL_BY_BRAS)
        df = add_total_sum_by_row(df, colname.TOTAL_BY_STATE)
        total_porcentage = df[colname.TOTAL_BY_STATE]
        total = total_porcentage[len(total_porcentage) - 1]
        total_porcentage = total_porcentage[:-1]
        new_values: List[float] = []
        for value in total_porcentage:
            new_values.append(round((value / total * 100), 2))
        new_values.append(sum(new_values))
        df[colname.TOTAL_BY_USAGE] = new_values
        FileController.write_excel(df, filename=filename.ADSL_CONSUMPTION)
    except Exception as error:
        raise error

def total_olt(fileolt: str) -> None:
    try:
        pass
    except Exception as error:
        raise error

@click.group()
def cli():
    """CONSUMPTION OF CLIENTS BY BRAS AND STATE

    \b
    Arguments:
      total -p [PORCENTAGE_CLIENTS_FILE] -c [CONSUMPTION_BRAS_FILE]  The file extension must be .xlsx
    """
    pass

# ADSL + MDU
@cli.command(help="Create the consumption by bras file to data ADSL and MDU.")
@click.option("-p", "--fileporcentage", help="Specific file with the porcentage of clients by bras/state.")
@click.option("-c", "--fileconsumption", help="Specific file with the consumption of clients by bras/state.")
def adsl_mdu(fileporcentage, fileconsumption):
    if fileporcentage and fileconsumption:
        total_adsl_mdu(fileporcentage, fileconsumption)

# OLT
@cli.command(help="Create the consumption by bras file to data OLT.")
@click.option("-o", "--fileolt", help="Specific file with the data olt")
def olt(fileolt):
    if fileolt:
        total_olt(fileolt)

if __name__ == "__main__":
    try:
        cli()
    except SystemExit as error:
        if error == 1:
            pass
    except Exception as error:
        click.echo(error)