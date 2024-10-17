import click
import traceback
import pandas as pd
from taccess.measurement import MeasurementTaccess
from common.utils.file import File

def measurement_by_taccess():
    try:
        click.echo("Getting measurements...")
        Measurement = MeasurementTaccess()
        if Measurement.bras:
            click.echo("Measurements found!")
            df = pd.DataFrame(Measurement.bras)
            File.write_excel(df, filename="consumo_por_bras.xlsx")
    except Exception as error:
        raise error
        

if __name__ == "__main__":
    try:
        measurement_by_taccess()
    except:
        traceback.print_exc()