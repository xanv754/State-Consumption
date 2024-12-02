from common import validate

def refactor_bras_name(bras_name: str) -> str:
    """Refactor the bras name to the format required."""
    try:
        if validate.name_bras(bras_name):
            bras_name = bras_name.split("_")[0].upper()
            return bras_name
        else: return "UNKNOWN"
    except Exception as error:
        raise error 