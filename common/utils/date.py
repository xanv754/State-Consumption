import datetime

def getFirstDayOfMonth() -> str:
    today = datetime.date.today()
    return today.strftime("%Y%m01")

def getLastDayAvailableOfMonth() -> str:
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime("%Y%m%d")