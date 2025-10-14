import pandas as pd
from abc import ABC, abstractmethod


class Reader(ABC):
    """Class to read the data from the file."""

    _filename: str

    def __init__(self, filename: str):
        self._filename = filename

    def get_filename(self) -> str:
        """Get the filename."""
        return self._filename

    @abstractmethod
    def get_data(self) -> pd.DataFrame:
        """Read the data from the file."""
        pass

    @abstractmethod
    def check_reader(self) -> bool:
        """Check if the proccess to reader the data will be successful."""
        pass
