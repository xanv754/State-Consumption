from boss import ClientController, ReportBossController, save_data_clients, save_data_porcentage
from common import colname, add_total_sum_by_col, add_total_sum_by_row

def clients_by_BRAS_and_state():
    """Generate the file with the total clients by bras and state and the percentages."""
    try:
        ReportBoss = ReportBossController()
        if ReportBoss.validate:
            df_clients = ClientController.total_bras_by_state(
                ReportBoss.report
            )
            if not df_clients.empty:
                df_clients = add_total_sum_by_col(df_clients, name_col=colname.TOTAL_BY_BRAS)
                df_clients = add_total_sum_by_row(df_clients, name_row=colname.TOTAL_BY_STATE)
                save_data_clients(df_clients)
                df_porcentage = ClientController.total_porcentage(df_clients)
                df_porcentage = add_total_sum_by_col(df_porcentage, name_col=colname.TOTAL_BY_BRAS)
                df_porcentage = add_total_sum_by_row(df_porcentage, name_row=colname.TOTAL_BY_STATE)
                save_data_porcentage(df_porcentage)
            else:
                raise Exception("Nodes without state exist")
    except Exception as error:
        raise error
