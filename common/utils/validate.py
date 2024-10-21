from common.constant import bras


def validate_name_bras(name: str) -> bool:
    """Validates the name of a BRAS node."""
    name = name.upper()
    if len(name) < 11:
        return False
    if not name.count("-") >= 2:
        return False
    if not name.count("_") >= 1:
        return False
    if not name.split("-")[1] == bras.NAME:
        return False
    if not (
        (name.split("-")[0] == bras.ANZ)
        or (name.split("-")[0] == bras.BOL)
        or (name.split("-")[0] == bras.BTO)
        or (name.split("-")[0] == bras.CHC)
        or (name.split("-")[0] == bras.CNT)
        or (name.split("-")[0] == bras.LMS)
        or (name.split("-")[0] == bras.MAD)
        or (name.split("-")[0] == bras.MAY)
        or (name.split("-")[0] == bras.MBO)
        or (name.split("-")[0] == bras.BTO)
        or (name.split("-")[0] == bras.MIL)
        or (name.split("-")[0] == bras.POD)
        or (name.split("-")[0] == bras.SCR)
    ):
        return False
    return True
