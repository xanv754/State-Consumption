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
    def get_data(self) -> pd.DataFrame:
        """Read the data from the file."""
        pass

    @abstractmethod
    def check_reader(self) -> bool:
        """Check if the proccess to reader the data will be successful."""
        pass