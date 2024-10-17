def validate_name_bras(name: str) -> bool:
    name = name.upper()
    if len(name) < 11: return False
    if not name.count("-") == 2: return False
    if not name.count("_") >= 1: return False
    if not name.split("-")[1] == "BRAS": return False
    if not ((name.split("-")[0] == "ANZ") 
            or (name.split("-")[0] == "ANZ")
            or (name.split("-")[0] == "BOL")
            or (name.split("-")[0] == "BTO")
            or (name.split("-")[0] == "CHC")
            or (name.split("-")[0] == "CNT")
            or (name.split("-")[0] == "LMS")
            or (name.split("-")[0] == "MAD")
            or (name.split("-")[0] == "MAY")
            or (name.split("-")[0] == "MBO")
            or (name.split("-")[0] == "MIL")
            or (name.split("-")[0] == "POD")
            or (name.split("-")[0] == "SCR")): 
        return False
    return True