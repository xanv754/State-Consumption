import click
from state_consumption.libs import CLIHandler, ReaderCLIHandler
from state_consumption.utils import logger, terminal


@click.group()
def cli():
    pass


@cli.command(help="Inspecciona la data para validar correctos formatos.")
@click.option(
    "--boss",
    help="Ruta del archivo BOSS.",
    type=click.Path(exists=True),
    required=False,
)
@click.option(
    "--asf", help="Ruta del archivo ASF.", type=click.Path(exists=True), required=False
)
@click.option(
    "--bras",
    help="Ruta del archivo con consumos por agregador.",
    type=click.Path(exists=True),
    required=False,
)
@click.option(
    "--process", help="Totaliza los consumos de la data de agregación.", is_flag=True
)
def inspect(boss: str, asf: str, bras: str, process: bool):
    logger.info("Iniciando inspección de data...")
    terminal.print("[orange3]Iniciando inspección de data...")
    if boss:
        ReaderCLIHandler.inspect_boss(boss)
    if asf:
        ReaderCLIHandler.inspect_asf(asf)
    if bras:
        if process:
            ReaderCLIHandler.inspect_consumption(bras, process=True)
        else:
            ReaderCLIHandler.inspect_consumption(bras, process=False)


@cli.command(help="Obtiene el reporte de consumo por estado.")
@click.option(
    "--boss", help="Ruta del archivo BOSS.", type=click.Path(exists=True), required=True
)
@click.option(
    "--asf", help="Ruta del archivo ASF.", type=click.Path(exists=True), required=True
)
@click.option(
    "--bras",
    help="Ruta del archivo con consumos por agregador.",
    type=click.Path(exists=True),
    required=True,
)
@click.option(
    "--process", help="Totaliza los consumos de la data de agregación.", is_flag=True
)
@click.option(
    "--percentage", help="Obtiene reporte con valoración con porcentajes.", is_flag=True
)
@click.option(
    "--filepath", help="Especifica la ruta para exportar el reporte.", type=click.Path()
)
def vpti(
    boss: str,
    asf: str,
    bras: str,
    process: bool,
    percentage: bool,
    filepath: str | None,
):
    logger.info("Generando reporte...")
    terminal.print("[orange3]Generando reporte...")
    processHandler = CLIHandler(
        boss_path=boss, asf_path=asf, bras_path=bras, process_consumption=process
    )
    if percentage:
        if filepath:
            savedIn = processHandler.clients_consumption_by_state_with_percentage(
                filepath=filepath
            )
        else:
            savedIn = processHandler.clients_consumption_by_state_with_percentage()
        if savedIn:
            logger.info(f"Reporte generado satisfactoriamente. Exportado en {savedIn}")
            terminal.print(
                f"[green3]Reporte generado satisfactoriamente. [default]Exportado en {savedIn}"
            )
        else:
            logger.error("Reporte fallido. Ha ocurrido un error en el proceso.")
            terminal.print(
                "[red3]ERROR: [default]Reporte fallido. Ha ocurrido un error en el proceso."
            )
    else:
        if filepath:
            savedIn = processHandler.clients_consumption_by_state(filepath=filepath)
        else:
            savedIn = processHandler.clients_consumption_by_state()
        if savedIn:
            logger.info(f"Reporte generado satisfactoriamente. Exportado en {savedIn}")
            terminal.print(
                f"[green3]Reporte generado satisfactoriamente. [default]Exportado en {savedIn}"
            )
        else:
            logger.error("Reporte fallido. Ha ocurrido un error en el proceso.")
            terminal.print(
                "[red3]ERROR: [default]Reporte fallido. Ha ocurrido un error en el proceso."
            )


@cli.command(help="Totalize the bras consumption.")
@click.option(
    "--filepath",
    help="Ruta del archivo con consumos por agregador.",
    type=click.Path(exists=True),
    required=True,
)
def bras(filepath: str):
    terminal.print("[orange3]Iniciando proceso de totalización...")
    processHandler = CLIHandler(
        boss_path=None, asf_path=None, bras_path=filepath, process_consumption=True
    )
    savedIn = processHandler.consumtion_bras()
    if savedIn:
        logger.info(f"Data generada satisfactoriamente. Exportado en {savedIn}")
        terminal.print(
            f"[green3]Data generada satisfactoriamente. [default]Exportado en {savedIn}"
        )
    else:
        logger.error("Data fallida. Ha ocurrido un error en el proceso.")
        terminal.print(
            "[red3]ERROR: [default]Reporte fallido. Ha ocurrido un error en el proceso."
        )


if __name__ == "__main__":
    cli()
