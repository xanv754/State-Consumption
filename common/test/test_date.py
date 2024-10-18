from common.utils.date import getFirstDayOfMonth, getLastDayAvailableOfMonth

CURRENT_YESTERDAY = "20241016"
CURRENT_FIRST_DAY = "20241001"

def test_getFirstDayOfMonth():
    assert getFirstDayOfMonth() == CURRENT_FIRST_DAY

def test_getLastDayAvailableOfMonth():
    assert getLastDayAvailableOfMonth() == CURRENT_YESTERDAY
