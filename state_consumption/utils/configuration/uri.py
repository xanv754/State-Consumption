from state_consumption.utils.configuration.env import Environment
from state_consumption.utils.info.logger import logger
from state_consumption.utils.info.console import terminal


class URIEnvironment(Environment):
    """A class that inherits from `Environment` to get the database URI from environment variables."""

    def __init__(
        self, prod: bool = False, dev: bool = False, testing: bool = False
    ) -> None:
        super().__init__(prod, dev, testing)

    def get_uri_db(self) -> str | None:
        """Gets the database URI from the environment variables.

        :returns str | None: The database URI if found, otherwise `None`.
        """
        try:
            if self._env:
                env = self._env.get("URI")
                if not env:
                    raise Exception("Variable 'URI' no declarada")
                return env
            return None
        except Exception as error:
            logger.error(f"No se ha encontrado las variables de entorno requeridas - {error}")
            terminal.print_spinner(f"[red3]ERROR: [default]No se ha encontrado las variables de entorno requeridas - {error}")
            exit(1)