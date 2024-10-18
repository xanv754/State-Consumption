import datetime

def getFirstDayOfMonth() -> str:
    """Returns the date of the first day of the month in yyyymmdd format."""
    today = datetime.date.today()
    return today.strftime("%Y%m01")

def getLastDayAvailableOfMonth() -> str:
    """Returns the latest available date in yyyymmdd format."""
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime("%Y%m%d")