import pandas as pd
from abc import ABC, abstractmethod

class Reader(ABC):
    """Reader to read the data from the file."""
    __filename: str
    
    def __init__(self, filename: str):
        self.__filename = filename


    def get_filename(self) -> str:
        """Get the filename."""
        return self.__filename

    @abstractmethod
    def get_data(self, filename: str) -> pd.DataFrame:
        """Read the data from the file."""
        pass