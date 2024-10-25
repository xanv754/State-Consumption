import pandas as pd
from common import FileController, filename as FILE
from measurement.taccess.measurement import ConsumptionTaccess

def get_consumption_by_taccess(process: bool = False) -> pd.DataFrame:
    """Generate the file with the consumption by bras from Taccess API.
    
    Parameters
    ----------
    process: bool, default False
        Flag to save the generated data.
    """
    try:
        Measurement = ConsumptionTaccess()
        if not Measurement.err:
            df = pd.DataFrame(Measurement.bras)
            if process: FileController.write_excel(df, filename=FILE.MEASUREMENT)
            return df
    except Exception as error:
        raise error