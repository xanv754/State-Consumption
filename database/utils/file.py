import pandas as pd

class File:
    @staticmethod
    def read_txt(path: str, delimiter: str = " ") -> pd.DataFrame:
        try:
            return pd.read_csv(path, delimiter=delimiter, encoding="latin-1", low_memory=False)
        except Exception as error:
            return pd.DataFrame()
        
    @staticmethod
    def read_csv(path: str, delimiter: str = ",") -> pd.DataFrame:
        try:
            return pd.read_csv(path, delimiter=delimiter, encoding="latin-1", low_memory=False)
        except Exception as error:
            return pd.DataFrame()
    
    @staticmethod
    def read_excel(path: str) -> pd.DataFrame:
        try:
            return pd.read_excel(path, index_col=None)
        except Exception as error:
            return pd.DataFrame()
    