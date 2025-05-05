import click
import rich
from libs.cli import DatabaseCLIHandler, ExportCLIHandler


@click.group()
def cli():
    pass


@cli.command(help="Operation with the database.")
@click.option("--migration", help="Make migration of the database.", is_flag=True)
@click.option("--rollback", help="Rollback of the database.", is_flag=True)
@click.option("--add", help="Add a new node to the database.", is_flag=True)
def database(migration: bool, rollback: bool, add: bool):
    if migration:
        rich.print("[orange3]Starting migration...")
        databaseHandler = DatabaseCLIHandler()
        status = databaseHandler.make_migration()
        if status: rich.print("[green3]Migration completed successfully")
        else: rich.print("[red3]Migration failed")
    elif rollback:
        rich.print("[orange3]Starting rollback...")
        databaseHandler = DatabaseCLIHandler()
        status = databaseHandler.rollback()
        if status: rich.print("[orange3]Rollback completed successfully")
        else: rich.print("[red3]Rollback failed")
    elif add:
        rich.print("[orange3]Starting add new node...")
        databaseHandler = DatabaseCLIHandler()
        status = databaseHandler.add_new_node()
        if status: rich.print("[green3]New node added successfully")
        else: rich.print("[red3]New node not added")


@cli.command(help="Update the database.")
@click.option("--filepath", help="Path of the file to extract the data.", type=click.Path(exists=True), required=True)
@click.option("--delimiter", help="Delimiter of the file.", type=click.Choice([";", ","]), default=";")
def update(filepath: str, delimiter: str):
    rich.print("[orange3]Starting update database...")
    databaseHandler = DatabaseCLIHandler()
    status = databaseHandler.update_database(filepath, delimiter=delimiter)
    if status: rich.print("[green3]Database updated successfully")
    else: rich.print("[red3]Database not updated")


@cli.command(help="Process the data to VPTI.")
@click.option("--boss", help="Path of the BOSS file.", type=click.Path(exists=True), required=True)
@click.option("--asf", help="Path of the ASF file.", type=click.Path(exists=True), required=True)
@click.option("--bras", help="Path of the bras consumption file.", type=click.Path(exists=True), required=True)
@click.option("--process", help="Process the data.", is_flag=True)
@click.option("--percentage", help="Process the data with percentage of consumption.", is_flag=True)
@click.option("--filepath", help="Path of save the data.", type=click.Path())
def vpti(boss: str, asf:str, bras: str, process: bool, percentage: bool, filepath: str | None):
    rich.print("[orange3]Starting process...")
    processHandler = ExportCLIHandler(boss_path=boss, asf_path=asf, bras_path=bras, process_consumption=process)
    if percentage:
        if filepath:
            savedIn = processHandler.clients_consumption_by_state_with_percentage(filepath=filepath)
        else:
            savedIn = processHandler.clients_consumption_by_state_with_percentage()
        if savedIn: rich.print("[green3]Process completed successfully. File saved in", savedIn)
        else: rich.print("[red3]Process failed")
    else:
        if filepath:
            savedIn = processHandler.clients_consumption_by_state(filepath=filepath)
        else:
            savedIn = processHandler.clients_consumption_by_state()
        if savedIn: rich.print("[green3]Process completed successfully. File saved in", savedIn)
        else: rich.print("[red3]Process failed")


@cli.command(help="Process the data only ADSL.")
@click.option("--boss", help="Path of the BOSS file.", type=click.Path(exists=True), required=True)
@click.option("--asf", help="Path of the ASF file.", type=click.Path(exists=True), required=True)
@click.option("--bras", help="Path of the bras consumption file.", type=click.Path(exists=True), required=True)
@click.option("--process", help="Process the data.", is_flag=True)
@click.option("--percentage", help="Process the data with percentage of consumption.", is_flag=True)
@click.option("--filepath", help="Path of save the data.", type=click.Path())
def adsl(boss: str, asf:str, bras: str, process: bool, percentage: bool, filepath: str | None):
    rich.print("[orange3]Starting process...")
    processHandler = ExportCLIHandler(boss_path=boss, asf_path=asf, bras_path=bras, process_consumption=process)
    if percentage:
        if filepath:
            savedIn = processHandler.clients_consumption_adsl_by_state_with_percentage(filepath=filepath)
        else:
            savedIn = processHandler.clients_consumption_adsl_by_state_with_percentage()
        if savedIn: rich.print("[green3]Process completed successfully. File saved in", savedIn)
        else: rich.print("[red3]Process failed")
    else:
        if filepath:
            savedIn = processHandler.clients_consumption_adsl_by_state(filepath=filepath)
        else:
            savedIn = processHandler.clients_consumption_adsl_by_state()
        if savedIn: rich.print("[green3]Process completed successfully. File saved in", savedIn)
        else: rich.print("[red3]Process failed")

@cli.command(help="Process the data only MDU.")
@click.option("--boss", help="Path of the BOSS file.", type=click.Path(exists=True), required=True)
@click.option("--asf", help="Path of the ASF file.", type=click.Path(exists=True), required=True)
@click.option("--bras", help="Path of the bras consumption file.", type=click.Path(exists=True), required=True)
@click.option("--process", help="Process the data.", is_flag=True)
@click.option("--percentage", help="Process the data with percentage of consumption.", is_flag=True)
@click.option("--filepath", help="Path of save the data.", type=click.Path())
def mdu(boss: str, asf:str, bras: str, process: bool, percentage: bool, filepath: str | None):
    rich.print("[orange3]Starting process...")
    processHandler = ExportCLIHandler(boss_path=boss, asf_path=asf, bras_path=bras, process_consumption=process)
    if percentage:
        if filepath:
            savedIn = processHandler.clients_consumption_mdu_by_state_with_percentage(filepath=filepath)
        else:
            savedIn = processHandler.clients_consumption_mdu_by_state_with_percentage()
        if savedIn: rich.print("[green3]Process completed successfully. File saved in", savedIn)
        else: rich.print("[red3]Process failed")
    else:
        if filepath:
            savedIn = processHandler.clients_consumption_mdu_by_state(filepath=filepath)
        else:
            savedIn = processHandler.clients_consumption_mdu_by_state()
        if savedIn: rich.print("[green3]Process completed successfully. File saved in", savedIn)
        else: rich.print("[red3]Process failed")

@cli.command(help="Process the data only OLT.")
@click.option("--boss", help="Path of the BOSS file.", type=click.Path(exists=True), required=True)
@click.option("--asf", help="Path of the ASF file.", type=click.Path(exists=True), required=True)
@click.option("--bras", help="Path of the bras consumption file.", type=click.Path(exists=True), required=True)
@click.option("--process", help="Process the data.", is_flag=True)
@click.option("--percentage", help="Process the data with percentage of consumption.", is_flag=True)
@click.option("--filepath", help="Path of save the data.", type=click.Path())
def olt(boss: str, asf:str, bras: str, process: bool, percentage: bool, filepath: str | None):
    rich.print("[orange3]Starting process...")
    processHandler = ExportCLIHandler(boss_path=boss, asf_path=asf, bras_path=bras, process_consumption=process)
    if percentage:
        if filepath:
            savedIn = processHandler.clients_consumption_olt_by_state_with_percentage(filepath=filepath)
        else:
            savedIn = processHandler.clients_consumption_olt_by_state_with_percentage()
        if savedIn: rich.print("[green3]Process completed successfully. File saved in", savedIn)
        else: rich.print("[red3]Process failed")
    else:
        if filepath:
            savedIn = processHandler.clients_consumption_olt_by_state(filepath=filepath)
        else:
            savedIn = processHandler.clients_consumption_olt_by_state()
        if savedIn: rich.print("[green3]Process completed successfully. File saved in", savedIn)
        else: rich.print("[red3]Process failed")

@cli.command(help="Totalize the bras consumption.")
@click.option("--filepath", help="Path of the bras consumption file.", type=click.Path(exists=True), required=True)
def bras(filepath: str):
    rich.print("[orange3]Starting process...")
    processHandler = ExportCLIHandler(boss_path=None, asf_path=None, bras_path=filepath, process_consumption=True)
    savedIn = processHandler.consumtion_bras()
    if savedIn: rich.print("[green3]Process completed successfully. File saved in", savedIn)
    else: rich.print("[red3]Process failed")


if __name__ == "__main__":
    cli()