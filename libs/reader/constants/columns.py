class BossNameColumns:
    """Column names to get the data from the process."""

    SUFFIX_BRAS: str = "Nrpname"
    PREFIX_BRAS: str = "Location"
    EQUIPMENT: str = "Provider.1"
    CENTRAL: str = "Name Coid"
    ACCOUNT_CODE: str = "Coid"
    TOTAL_CLIENTS: str = "Cantidad"


class BossNewNameColumns:
    EQUIPMENT: str = "Modelo"
    CENTRAL: str = "Central"
    ACCOUNT_CODE: str = "CC"


class AsfNameColumns:
    DNI: str = "DOCUMENTO"
    BRAS: str = "HOSTNAME"
    STATE: str = "ESTADO"
    STATUS: str = "STATUS"


boss_all_columns = [
    BossNameColumns.SUFFIX_BRAS,
    BossNameColumns.PREFIX_BRAS,
    BossNameColumns.EQUIPMENT,
    BossNameColumns.CENTRAL,
    BossNameColumns.ACCOUNT_CODE,
    BossNameColumns.TOTAL_CLIENTS,
]

asf_all_columns = [
    AsfNameColumns.DNI,
    AsfNameColumns.BRAS,
    AsfNameColumns.STATE,
    AsfNameColumns.STATUS,
]

