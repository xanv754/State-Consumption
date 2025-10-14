class NameColumns:
    """Column names to get the data from the process."""

    BRAS: str = "Bras"
    STATE: str = "Estado"
    TOTAL_CLIENTS: str = "Total Clientes"
    CONSUMPTION: str = "Consumo (GB)"
    PERCENTAGE_CONSUMPTION: str = "Porcentaje Consumo (%)"


class ConsumptionStateColumns:
    """Column names to get the data from the process."""

    TOTAL_CLIENTS_ADSL: str = "Total Clientes ADSL"
    TOTAL_CLIENTS_MDU: str = "Total Clientes MDU"
    TOTAL_CLIENTS_OLT: str = "Total Clientes OLT"
    CONSUMPTION_ADSL: str = "Consumo ADSL (GB)"
    CONSUMPTION_MDU: str = "Consumo MDU (GB)"
    CONSUMPTION_OLT: str = "Consumo OLT (GB)"
    PERCENTAGE_CONSUMPTION_ADSL: str = "Porcentaje Consumo ADSL (%)"
    PERCENTAGE_CONSUMPTION_MDU: str = "Porcentaje Consumo MDU (%)"
    PERCENTAGE_CONSUMPTION_OLT: str = "Porcentaje Consumo OLT (%)"


class BossNameColumns:
    """Column names to get the data from the process."""

    SUFFIX_BRAS: str = "Nrpname"
    PREFIX_BRAS: str = "Location"
    EQUIPMENT: str = "Provider.1"
    CENTRAL: str = "Name Coid"
    ACCOUNT_CODE: str = "Coid"
    STATUS: str = "Status"
    TOTAL_CLIENTS: str = "Cantidad"


class BossNewNameColumns:
    EQUIPMENT: str = "Modelo"
    CENTRAL: str = "Central"
    ACCOUNT_CODE: str = "CC"


class AsfNameColumns:
    BRAS: str = "HOSTNAME"
    STATE: str = "ESTADO"
    STATUS: str = "STATUS"


boss_all_columns = [
    BossNameColumns.SUFFIX_BRAS,
    BossNameColumns.PREFIX_BRAS,
    BossNameColumns.EQUIPMENT,
    BossNameColumns.CENTRAL,
    BossNameColumns.ACCOUNT_CODE,
    BossNameColumns.STATUS,
    BossNameColumns.TOTAL_CLIENTS,
]

asf_all_columns = [AsfNameColumns.BRAS, AsfNameColumns.STATE, AsfNameColumns.STATUS]
