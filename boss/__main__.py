import click
from boss.generate import clients_by_BRAS_and_state, total_comsuption_by_state, adsl_clients_by_BRAS_and_state, mdu_clients_by_BRAS_and_state
from common.constant import filename

@click.group()
def cli():
    """MODULE BOSS

    This module is in charge of generating new reports from the boss report.

    \b
    Arguments:
      clients -f [REPORT_BOSS_FILE]                         
      adsl -f [REPORT_BOSS_FILE] -c [CONSUMPTION_BRAS_FILE] 
      mdu -f [REPORT_BOSS_FILE] -c [CONSUMPTION_BRAS_FILE]  
    """
    pass

@cli.command(help="Create the total clients report by state and bras")
@click.option("-f", "--filereport", help="Filepath of the report boss file to be read", type=click.Path(exists=True))
def clients(filereport):
    if filereport:
        clients_by_BRAS_and_state(filereport)

@cli.command(help="Create the total ADSL consumption by state")
@click.option("-f", "--filereport", help="Filepath of the report boss file to be read", type=click.Path(exists=True))
@click.option("-c", "--fileconsumption", help="Filepath of the consumption file to be read", type=click.Path(exists=True))
@click.option("-p", "--process", help="Save all files in the process execute", is_flag=True)
def adsl(filereport, fileconsumption):
    if filereport and fileconsumption:
        adsl_clients_by_BRAS_and_state(filereport)
        total_comsuption_by_state(filename.ADSL_PORCENTAGE, fileconsumption, equipment="adsl")

@cli.command(help="Create the total MDU consumption by state")
@click.option("-f", "--filereport", help="Filepath of the report boss file to be read", type=click.Path(exists=True))
@click.option("-c", "--fileconsumption", help="Filepath of the consumption file to be read", type=click.Path(exists=True))
def mdu(filereport, fileconsumption):
    if filereport and fileconsumption:
        mdu_clients_by_BRAS_and_state(filereport)
        total_comsuption_by_state(filename.MDU_PORCENTAGE, fileconsumption, equipment="mdu")

if __name__ == "__main__":
    try:
        cli()
    except Exception as error:
        click.echo(error)
