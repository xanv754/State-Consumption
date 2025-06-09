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