from state_consumption.utils.configuration.env import Environment
from state_consumption.utils.info.logger import logger
from state_consumption.utils.info.console import terminal



class SSOMPEnvironment(Environment):
    """A class that inherits from `Environment` to get the credentials from environment variables."""

    def __init__(
        self, prod: bool = False, dev: bool = False, testing: bool = False
    ) -> None:
        super().__init__(prod, dev, testing)

    def get_host(self) -> str | None:
        """Gets the IP from the environment variables.

        :returns str | None: IP if found, otherwise `None`.
        """
        try:
            return self._get_env_var("HOST")
        except Exception as error:
            logger.error(f"No se ha encontrado la variable de entorno 'HOST' - {error}")
            terminal.print_spinner(f"[red3]ERROR: [default]No se ha encontrado la variable de entorno 'HOST' - {error}")
            exit(1)


class ScrapperEnvironment(Environment):
    """A class to get the scrapper credentials from environment variables."""

    def __init__(
        self, prod: bool = False, dev: bool = False, testing: bool = False
    ) -> None:
        super().__init__(prod, dev, testing)
        self._url_login: str | None = None
        self._url_base: str | None = None
        self._user: str | None = None
        self._password: str | None = None
        self._load_credentials()

    def _load_credentials(self) -> None:
        """Loads all credentials from environment variables."""
        try:
            self._url_login = self._get_env_var("SSOMP_URL_LOGIN")
            self._url_base = self._get_env_var("SSOMP_URL_BASE")
            self._user = self._get_env_var("SSOMP_USER")
            self._password = self._get_env_var("SSOMP_PASSWORD")
        except Exception as error:
            logger.error(f"No se han encontrado las variables de entorno requeridas para el scrapper - {error}")
            terminal.print_spinner(f"[red3]ERROR: [default]No se han encontrado las variables de entorno requeridas para el scrapper - {error}")
            exit(1)

    def _get_env_var(self, var_name: str) -> str:
        """Gets a specific variable from the environment."""
        var = self._env.get(var_name)
        if not var:
            raise Exception(f"Variable '{var_name}' no declarada")
        return var

    def get_credentials(self) -> dict[str, str | None]:
        """Returns user and password."""
        return {"nombre": self._user, "clave": self._password}

    def get_url_login(self) -> str | None:
        """Returns the login URL."""
        return self._url_login

    def get_url_base(self) -> str | None:
        """Returns the base data URL."""
        return self._url_base
