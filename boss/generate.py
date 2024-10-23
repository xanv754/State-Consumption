from common import colname, add_total_sum_by_col, add_total_sum_by_row
from boss.lib.clients import ClientController
from boss.lib.report import ReportBossController
from boss.lib.data import save_data_clients, save_data_porcentage, save_data_adsl_porcentage, save_data_mdu_porcentage

def clients_by_BRAS_and_state():
    """Generate the file with the total clients by bras and state and the percentages."""
    try:
        ReportBoss = ReportBossController()
        if ReportBoss.validate:
            df_data_total = ClientController.total_bras_by_state(
                ReportBoss.report
            )
            df_data_adsl = ClientController.total_bras_by_state(
                ReportBoss.data_adsl    
            )
            df_data_mdu = ClientController.total_bras_by_state(
                ReportBoss.data_mdu
            )
            if not df_data_total.empty:
                df_data_total = add_total_sum_by_col(df_data_total, name_col=colname.TOTAL_BY_BRAS)
                df_data_total = add_total_sum_by_row(df_data_total, name_row=colname.TOTAL_BY_STATE)
                save_data_clients(df_data_total)
                df_data_adsl = add_total_sum_by_col(df_data_adsl, name_col=colname.TOTAL_BY_BRAS)
                df_data_adsl = add_total_sum_by_row(df_data_adsl, name_row=colname.TOTAL_BY_STATE)
                save_data_clients(df_data_adsl)
                df_data_mdu = add_total_sum_by_col(df_data_mdu, name_col=colname.TOTAL_BY_BRAS)
                df_data_mdu = add_total_sum_by_row(df_data_mdu, name_row=colname.TOTAL_BY_STATE)
                save_data_clients(df_data_mdu)
                df_total_porcentage = ClientController.total_porcentage(df_data_total)
                df_total_porcentage = add_total_sum_by_col(df_total_porcentage, name_col=colname.TOTAL_BY_BRAS)
                df_total_porcentage = add_total_sum_by_row(df_total_porcentage, name_row=colname.TOTAL_BY_STATE)
                save_data_porcentage(df_total_porcentage)
                df_adsl_porcentage = ClientController.total_porcentage(df_data_adsl)
                df_adsl_porcentage = add_total_sum_by_col(df_adsl_porcentage, name_col=colname.TOTAL_BY_BRAS)
                df_adsl_porcentage = add_total_sum_by_row(df_adsl_porcentage, name_row=colname.TOTAL_BY_STATE)
                save_data_adsl_porcentage(df_adsl_porcentage)
                df_mdu_porcentage = ClientController.total_porcentage(df_data_mdu)
                df_mdu_porcentage = add_total_sum_by_col(df_mdu_porcentage, name_col=colname.TOTAL_BY_BRAS)
                df_mdu_porcentage = add_total_sum_by_row(df_mdu_porcentage, name_row=colname.TOTAL_BY_STATE)
                save_data_mdu_porcentage(df_mdu_porcentage)
            else:
                raise Exception("Nodes without state exist")
    except Exception as error:
        raise error
