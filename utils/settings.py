import os
from dotenv import dotenv_values


class SettingHandler:
    """Handler to obtained the constant variables of configuration."""

    __instance: "SettingHandler | None" = None
    uri: str | None = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, "__initialized"):
            self.__initialized = True
            self.__read_env()

    def __read_env(self) -> None:
        """Read the environment variables."""
        try:
            if os.path.exists(".env.development"):
                env = dotenv_values(".env.development")
                uri = env.get("URI")
                if uri: self.uri = uri
            elif os.path.exists(".env.production"):
                env = dotenv_values(".env.production")
                uri = env.get("URI")
                if uri: self.uri = uri
            elif os.path.exists(".env"):
                env = dotenv_values(".env")
                uri = env.get("URI")
                if uri: self.uri = uri
            else:
                raise FileNotFoundError("No file with environment variables found")
        except Exception as error:
            print(error, __file__)

    def write_default(self):
        pass