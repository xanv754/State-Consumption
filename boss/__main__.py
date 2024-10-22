import click
from boss.lib.clients import ClientController
from boss.lib.report import ReportBossController
from boss.lib.data import save_data_clients, save_data_porcentage
from common.utils.totalling import add_total_sum_by_col, add_total_sum_by_row
from common.constant import colname

@click.group()
def cli():
    """MODULE BOSS

    This module is in charge of generating new reports from the boss report.
    """
    pass

@cli.command(help="Create the total clients report by state and bras")
def clients():
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

if __name__ == "__main__":
    try:
        cli()
    except Exception as error:
        click.echo(error)
