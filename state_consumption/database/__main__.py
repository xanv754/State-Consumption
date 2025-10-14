import click
from state_consumption.database.libs.mongo import MongoDatabase


@click.group()
def cli():
    pass


@cli.command(help="Instancia la base de datos.")
@click.option(
    "--dev", is_flag=True, help="Instancia la base de datos en modo desarrollo."
)
@click.option(
    "--testing", is_flag=True, help="Instancia la base de datos en modo de pruebas."
)
def start(dev: bool = False, testing: bool = False) -> None:
    mongo = MongoDatabase(dev=dev, testing=testing)
    mongo.initialize_collection()


@cli.command(help="Elimina la base de datos.")
@click.option(
    "--dev", is_flag=True, help="Destruye la base de datos en modo desarrollo."
)
@click.option(
    "--testing", is_flag=True, help="Destruye la base de datos en modo de pruebas."
)
def destroy(dev: bool = False, testing: bool = False) -> None:
    mongo = MongoDatabase(dev=dev, testing=testing)
    mongo.drop_collection()


if __name__ == "__main__":
    cli()
