import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from state_consumption.database.querys.insert import InsertQuery
from state_consumption.utils.configuration import ScrapperEnvironment
from state_consumption.utils.info.logger import logger


class SsompScrapper:
    """
    Scrapper for extracting node data from the SSOMP platform.
    """

    def __init__(self, dev: bool = False, testing: bool = False) -> None:
        self._env = ScrapperEnvironment(dev=dev, testing=testing)
        self._url_login = self._env.get_url_login()
        self._url_base = self._env.get_url_base()
        self._credentials = self._env.get_credentials()
        self._session = requests.Session()
        self._data = []
        self._insert_query = InsertQuery(dev=dev, testing=testing)
        self._first_row_data = None

    def _login(self) -> bool:
        if not self._url_login or not self._credentials:
            logger.error("URL de login o credenciales no configuradas.")
            return False
        try:
            response = self._session.post(self._url_login, data=self._credentials)
            response.raise_for_status()
            logger.info("Inicio de sesión exitoso en SSOMP.")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al iniciar sesión o conectar con el servidor: {e}")
            return False

    @staticmethod
    def _clean_value(text: str) -> str | None:
        """
        Converts empty strings, whitespace, or '---' marker to None.
        """
        cleaned_text = text.strip()
        if not cleaned_text or cleaned_text in ('---', '-'):
            return None
        return cleaned_text

    def _extract_page_data(self, page_number: int) -> bool:
        """
        Extracts data from a single page.
        Returns True if data was found, False otherwise.
        Detects if the first row repeats to avoid infinite loops.
        """
        try:
            url = self._url_base.format(pagina=page_number)
            response = self._session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            main_table = soup.find("table", id="toperad")

            rows = main_table.find_all("tr")[2:] if main_table else []
            if not rows:
                logger.info(f"No se encontró tabla de datos en la página {page_number}. Se asume fin de la paginación.")
                return False

            # Detectar bucle infinito por repetición de la primera fila
            first_row = rows[0] if rows else None
            if first_row:
                first_cells = first_row.find_all("td")
                first_row_data = tuple(cell.get_text(strip=True) for cell in first_cells)
                if self._first_row_data is None:
                    self._first_row_data = first_row_data
                elif first_row_data == self._first_row_data:
                    logger.info(f"Se detectó repetición de la primera fila en la página {page_number}. Fin de la paginación.")
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
                            "Estado": state,
                            "CC": cc,
                            "Nombre del Nodo": node_name
                        })
            time.sleep(0.1)
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de conexión/HTTP al procesar la página {page_number}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error de parseo en la página {page_number}: {e}")
            return False

    def run_scrapping(self) -> pd.DataFrame | None:
        """
        Runs the complete scrapping process.
        """
        if not self._login():
            return None

        logger.info("Comenzando la extracción de páginas...")
        page_num = 1
        with tqdm(desc="Extrayendo datos de SSOMP", unit="página") as pbar:
            while self._extract_page_data(page_num):
                page_num += 1
                pbar.update(1)
        
        logger.info(f"Extracción completada. Se procesaron {page_num - 1} páginas. Consolidando datos...")
        if not self._data:
            logger.warning("No se pudo extraer ningún dato.")
            return None

        df = pd.DataFrame(self._data)
        df['CC'] = pd.to_numeric(df['CC'], errors='coerce')
        df['CC'] = df['CC'].fillna('')
        def format_cc_or_empty(val):
            if isinstance(val, float): 
                if not pd.isna(val):
                    return str(int(val))
            return str(val)
        df['CC'] = df['CC'].apply(format_cc_or_empty)
        return df

    def save_to_database(self, df: pd.DataFrame) -> None:
        """
        Saves the DataFrame to the database.
        """
        if df is None or df.empty:
            logger.warning("El DataFrame está vacío. No hay nada que guardar en la base de datos.")
            print("\n⚠️ PROCESO TERMINADO: No se pudo guardar porque no se extrajo ningún dato válido.")
            return

        # Validación adicional: Filtrar filas sin Nombre del Nodo o Estado; permitir CC='--' o vacío
        initial_count = len(df)
        df = df[df['Nombre del Nodo'].notna() & (df['Nombre del Nodo'] != '') & df['Estado'].notna() & (df['Estado'] != '')]
        filtered_count = initial_count - len(df)
        if filtered_count > 0:
            logger.info(f"Se filtraron {filtered_count} registros sin 'Nombre del Nodo' o 'Estado' válido.")

        logger.info("Guardando datos en la base de datos...")

        documents = df.to_dict('records')
        result = self._insert_query.insert_nodes(documents)

        if result:
            total_upserted = getattr(result, 'upserted_count', 0)
            total_modified = getattr(result, 'modified_count', 0)
            total_db_changes = total_upserted + total_modified

            logger.info(f"Se realizaron {total_db_changes} operaciones (Inserciones nuevas: {total_upserted}, Modificaciones: {total_modified}) exitosamente.")

            total_extraidos = len(df)
            print(f"\n✨ SCRAPING FINALIZADO CON ÉXITO: {total_extraidos} registros extraídos.")
            print("¡Proceso completado! ✅")

        else:
            logger.error("No se pudieron guardar los datos en la base de datos.")
            print("\n❌ ERROR CRÍTICO: Fallo al guardar los datos en la base de datos. Por favor, revisa los logs.")