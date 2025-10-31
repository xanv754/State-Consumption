import click
from state_consumption.database.libs.mongo import MongoDatabase


@click.group()
def cli():
    pass


@cli.command(help="Instancia la base de datos.")
@click.option("--dev", is_flag=True, help="Instancia la base de datos en modo desarrollo.")
@click.option("--testing", is_flag=True, help="Instancia la base de datos en modo de pruebas.")
def start(dev: bool = False, testing: bool = False) -> None:
    mongo = MongoDatabase(dev=dev, testing=testing)
    mongo.initialize_collection()


@cli.command(help="Elimina la base de datos.")
@click.option("--dev", is_flag=True, help="Destruye la base de datos en modo desarrollo.")
@click.option("--testing", is_flag=True, help="Destruye la base de datos en modo de pruebas.")
def destroy(dev: bool = False, testing: bool = False) -> None:
    mongo = MongoDatabase(dev=dev, testing=testing)
    mongo.drop_collection()


@cli.command(help="Ejecuta el scrapper para obtener y guardar los nodos.")
@click.option("--dev", is_flag=True, help="Usa la base de datos de desarrollo.")
@click.option("--testing", is_flag=True, help="Usa la base de datos de pruebas.")
def scrape(dev: bool = False, testing: bool = False) -> None:
    """
    Ejecuta el scrapper de SSOMP y guarda los datos en la base de datos.
    """
    from state_consumption.database.scrapping.ssomp import SsompScrapper
    scrapper = SsompScrapper(dev=dev, testing=testing)
    df = scrapper.run_scrapping()

    if df is not None and not df.empty:
        scrapper.save_to_database(df)
    else:
        print("No se extrajeron datos o se produjo un error.")


if __name__ == "__main__":
    cli()