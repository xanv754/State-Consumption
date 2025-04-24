import click
import rich
from libs.cli import DatabaseCLIHandler, ProcessCLIHandler


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


@cli.command(help="Process the data.")
@click.option("--boss", help="Path of the BOSS file.", type=click.Path(exists=True), required=True)
@click.option("--bras", help="Path of the bras consumption file.", type=click.Path(exists=True), required=True)
@click.option("--process", help="Process the data.", is_flag=True)
def process(boss: str, bras: str, process: bool):
    rich.print("[orange3]Starting process...")
    processHandler = ProcessCLIHandler()
    status = processHandler.main(boss, bras, process)
    if status: rich.print("[green3]Process completed successfully")
    else: rich.print("[red3]Process failed")


if __name__ == "__main__":
    cli()