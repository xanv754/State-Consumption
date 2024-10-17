import click
from boss.lib.clients import ClientController
from boss.lib.report import ReportBossController
from boss.lib.load import save_data_clients, save_data_porcentage

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
            df_clients = ClientController.create_usage_for_bras_by_state(ReportBoss.report)
            if not df_clients.empty: 
                df_clients = ClientController.add_total_sum_by_bras(df_clients)
                df_clients = ClientController.add_total_sum_by_state(df_clients)
                save_data_clients(df_clients)
                df_porcentage = ClientController.create_usage_porcentage(df_clients)
                df_porcentage = ClientController.add_total_sum_by_bras(df_porcentage)
                df_porcentage = ClientController.add_total_sum_by_state(df_porcentage)
                save_data_porcentage(df_porcentage)
            else: raise Exception("Nodes without state exist")
    except Exception as error:  
        raise error

if __name__ == "__main__":
    try:
        cli()
    except Exception as error:
        click.echo(error)
