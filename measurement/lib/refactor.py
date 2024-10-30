def refactor_bras_name(bras_name: str) -> str:
    """Refactor the bras name to the format required."""
    try:
        bras_name = bras_name.split("_")[0].upper()
        return bras_name
    except Exception as error:
        raise error 