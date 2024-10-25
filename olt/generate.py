from olt.lib.report import ReportOLTController
from olt.lib.data import save_data_olt

def total_by_state(filename: str):
    """Generate the file with the total clients by state and the percentages."""
    try:
        ReportOLT = ReportOLTController(filename)
        if ReportOLT.validate:
            df_totals = ReportOLT.generate_totals()
            save_data_olt(df_totals)
    except Exception as error:
        raise error