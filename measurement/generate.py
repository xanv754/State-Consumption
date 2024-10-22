import pandas as pd
from measurement import ConsumptionTaccess
from common import FileController, filename as FILE

def get_consumption_by_taccess():
    """Generate the file with the consumption by bras from Taccess API."""
    try:
        Measurement = ConsumptionTaccess()
        if not Measurement.err:
            df = pd.DataFrame(Measurement.bras)
            FileController.write_excel(df, filename=FILE.MEASUREMENT)
    except Exception as error:
        raise error