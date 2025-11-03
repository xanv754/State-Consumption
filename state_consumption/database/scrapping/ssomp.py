import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from state_consumption.constants import SSOMPScrappingColumns
from state_consumption.database.querys.insert import InsertQuery
from state_consumption.utils import ScrapperEnvironment, logger, terminal


class SsompScrapper:
    """Scrapper for extracting node data from the SSOMP platform."""

    def __init__(self, prod: bool = False, dev: bool = False, testing: bool = False) -> None:
        self._env = ScrapperEnvironment(prod=prod, dev=dev, testing=testing)
        self._url_login = self._env.get_url_login()
        self._url_base = self._env.get_url_base()
        self._credentials = self._env.get_credentials()
        self._session = requests.Session()
        self._data = []
        self._insert_query = InsertQuery(dev=dev, testing=testing)
        self._first_row_data = None

    def _login(self) -> bool:
        if not self._url_login or not self._credentials:
            logger.error("URL de login o credenciales no configuradas")
            terminal.print_spinner(f"[red3]ERROR: [default]URL de login o credenciales no configuradas")
            return False
        try:
            response = self._session.post(self._url_login, data=self._credentials)
            response.raise_for_status()
            logger.info("Inicio de sesión exitoso en SSOMP")
            return True
        except requests.exceptions.RequestException as error:
            logger.error(f"Error al iniciar sesión o conectar con el servidor - {error}")
            terminal.print_spinner(f"[red3]ERROR: [default]Error al iniciar sesión o conectar con el servidor - {error}")
            return False
        except Exception as error:
            logger.error(f"Error inesperado al iniciar sesión - {error}")
            terminal.print_spinner(f"[red3]ERROR: [default]Error inesperado al iniciar sesión - {error}")
            return False

    def _clean_value(self, text: str) -> str | None:
        """Converts empty strings, whitespace, or '---' marker to None."""
        cleaned_text = text.strip()
        if not cleaned_text or cleaned_text in ('---', '-'):
            return None
        return cleaned_text

    def _extract_page_data(self, page_number: int) -> bool:
        """Extracts data from a single page. Detects if the first row repeats to avoid infinite loops.
        
        :returns bool: True if data was found, False otherwise.
        """
        try:
            url = self._url_base.format(pagina=page_number)
            response = self._session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            main_table = soup.find("table", id="toperad")
            rows = main_table.find_all("tr")[2:] if main_table else []
            if not rows:
                logger.warning(f"No se encontró tabla de datos en la página {page_number}. Se asume fin de la paginación")
                terminal.print_spinner(f"\n[orange1]WARNING: [default]No se encontró tabla de datos en la página {page_number}. Se asume fin de la paginación")
                return False
            first_row = rows[0] if rows else None
            if first_row:
                first_cells = first_row.find_all("td")
                first_row_data = tuple(cell.get_text(strip=True) for cell in first_cells)
                if self._first_row_data is None:
                    self._first_row_data = first_row_data
                elif first_row_data == self._first_row_data:
                    logger.warning(f"Se detectó repetición de la primera fila en la página {page_number}. Fin de la paginación")
                    terminal.print_spinner(f"\n[orange1]WARNING: [default]Se detectó repetición de la primera fila en la página {page_number}. Fin de la paginación")
                    return False

            for row in rows:
                cells = row.find_all("td")
                if len(cells) > 7:
                    state = self._clean_value(cells[1].get_text())
                    cc_link = cells[6].find('a')
                    cc_raw = cc_link.get_text() if cc_link else cells[6].get_text()
                    cc = self._clean_value(cc_raw)
                    node_link = cells[7].find('a')
                    node_raw = node_link.get_text() if node_link else cells[7].get_text()
                    node_name = self._clean_value(node_raw)

                    if state and node_name:
                        self._data.append({
                            SSOMPScrappingColumns.STATE: state,
                            SSOMPScrappingColumns.ACCOUNT_CODE: cc,
                            SSOMPScrappingColumns.NAME_NODE: node_name
                        })
            time.sleep(0.1)
            return True
        except requests.exceptions.RequestException as error:
            logger.error(f"Error de conexión/HTTP al procesar la página {page_number} - {error}")
            terminal.print_spinner(f"[red3]ERROR: [default]Error de conexión/HTTP al procesar la página {page_number} - {error}")
            return False
        except Exception as error:
            logger.error(f"Error de parseo en la página {page_number} - {error}")
            terminal.print_spinner(f"[red3]ERROR: [default]Error de parseo en la página {page_number} - {error}")
            return False

    def run_scrapping(self) -> pd.DataFrame | None:
        """Runs the complete scrapping process."""
        if not self._login(): return None

        logger.info("Comenzando la extracción de páginas...")
        terminal.print_spinner(f"Comenzando la extracción de páginas...")
        page_num = 1
        with tqdm(desc="Extrayendo datos de SSOMP", unit=" página") as pbar:
            while self._extract_page_data(page_num):
                page_num += 1
                pbar.update(1)
        
        logger.info(f"Extracción completada. Se procesaron {page_num - 1} páginas. Consolidando datos...")
        terminal.print_spinner(f"[green3]Extracción completada. [default]Se procesaron {page_num - 1} páginas. Consolidando datos...")
        if not self._data:
            logger.error("No se pudo extraer ningún dato")
            terminal.print_spinner(f"[red3]]ERROR: [default]No se pudo extraer ningún dato")
            return None

        df = pd.DataFrame(self._data)
        df[SSOMPScrappingColumns.ACCOUNT_CODE] = pd.to_numeric(df[SSOMPScrappingColumns.ACCOUNT_CODE], errors='coerce')
        df[SSOMPScrappingColumns.ACCOUNT_CODE] = df[SSOMPScrappingColumns.ACCOUNT_CODE].fillna('')
        def format_cc_or_empty(val) -> str:
            if isinstance(val, float): 
                if not pd.isna(val):
                    return str(int(val))
            return str(val)
        df[SSOMPScrappingColumns.ACCOUNT_CODE] = df[SSOMPScrappingColumns.ACCOUNT_CODE].apply(format_cc_or_empty)
        return df

    def save_to_database(self, df: pd.DataFrame) -> None:
        """Saves the DataFrame to the database."""
        if df is None or df.empty:
            logger.warning("El DataFrame está vacío. No hay nada que guardar en la base de datos")
            terminal.print_spinner(f"[orange3]WARNING: Proceso terminado. [default]El DataFrame está vacío. No hay nada que guardar en la base de datos")
            return

        initial_count = len(df)
        df = df[df[SSOMPScrappingColumns.NAME_NODE].notna() & (df[SSOMPScrappingColumns.NAME_NODE] != '') & df[SSOMPScrappingColumns.STATE].notna() & (df[SSOMPScrappingColumns.STATE] != '')]
        filtered_count = initial_count - len(df)
        if filtered_count > 0:
            logger.warning(f"Se filtraron {filtered_count} registros sin 'Nombre del Nodo o 'Estado' válido")
            terminal.print_spinner(f"[orange3]WARNING: [default]Se filtraron {filtered_count} registros sin 'Nombre del Nodo o 'Estado' válido")

        logger.info("Guardando datos en la base de datos...")

        documents = df.to_dict('records')
        result = self._insert_query.insert_nodes(documents)

        if result:
            total_upserted = getattr(result, 'upserted_count', 0)
            total_modified = getattr(result, 'modified_count', 0)
            total_db_changes = total_upserted + total_modified

            logger.info(f"Se realizaron {total_db_changes} operaciones (Inserciones nuevas: {total_upserted}, Modificaciones: {total_modified}) exitosamente")

            total_extraidos = len(df)
            logger.info(f"Proceso finalizado con éxito. {total_extraidos} registros extraídos")
            terminal.print_spinner(f"[green3]Proceso finalizado con éxito. [default]{total_extraidos} registros extraídos")

        else:
            logger.error("Fallo al guardar los datos en la base de datos")
            terminal.print_spinner(f"[red3]ERROR: [default]Fallo al guardar los datos en la base de datos")