from os import path
from typing import Dict
from dotenv import load_dotenv, dotenv_values
from state_consumption.utils.info.log import logger
from state_consumption.utils.info.console import terminal


load_dotenv(override=True)


class Environment:
    """A parent class that handles the declaration of environment variables."""

    _env: Dict[str, str | None] | None
    _base_path: str = path.abspath(path.join(path.dirname(__file__), "..", "..", ".."))

    def __init__(
        self, prod: bool = False, dev: bool = False, test: bool = False
    ) -> None:
        self._env = self._get_env(prod, dev, test)

    def _get_env(
        self, prod: bool = False, dev: bool = False, test: bool = False
    ) -> Dict[str, str | None]:
        """Load variables from the specified environment.

        :returns Dict[str, str | None]: Dictionary containing the environment variables.
        """
        try:
            if prod:
                if not path.exists(path.join(self._base_path, ".env.production")) or path.exists(path.join(self._base_path, ".env")):
                    raise FileNotFoundError(
                        f"El archivo 'env.production' o '.env' es requerido"
                    )
                return dotenv_values(path.join(self._base_path, ".env.production"))
            elif dev:
                if not path.exists(path.join(self._base_path, ".env.development")):
                    raise FileNotFoundError(
                        f"El archivo 'env.development' es requerido"
                    )
                return dotenv_values(path.join(self._base_path, ".env.development"))
            elif test:
                if not path.exists(path.join(self._base_path, ".env.testing")):
                    raise FileNotFoundError(
                        f"El archivo 'env.testing' es requerido"
                    )
                return dotenv_values(path.join(self._base_path, ".env.testing"))
            else:
                raise Exception("No se ha encontrado ningún archivo")
        except FileNotFoundError as error:
            logger.error(f"Archivo con variables de entorno no encontrado en {self._base_path} - {error}")
            terminal.print_spinner(f"[red3]ERROR: [default]Archivo con variables de entorno no encontrado en {self._base_path} - {error}")
            exit(1)
        except Exception as error:
            logger.error(f"Error en las variables de entorno del sistema - {error}")
            terminal.print_spinner(f"[red3]ERROR: [default]Problemas con las variables de entorno del sistema - {error}")
            exit(1)