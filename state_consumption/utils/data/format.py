import pandas as pd
import textwrap


class FixFormat:
    """Class to fix the format of the data."""

    @staticmethod
    def column_word(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
        """Fixes a character corruption error in a dataframe column.
        
        :params df: Data to be fixed.
        :type df: DataFrame
        :params column_name: Name of the column to be fixed.
        :type column_name: str
        :returns DataFrame: Processed data.
        """
        df = df.copy()
        df[column_name] = df[column_name].str.replace("ß", "a")
        df[column_name] = df[column_name].str.replace("┴", "A")
        df[column_name] = df[column_name].str.replace("Ú", "é")
        # TODO: ... -> É
        df[column_name] = df[column_name].str.replace("Ý", "í")
        # TODO: ... -> Í
        df[column_name] = df[column_name].str.replace("=", "ó")
        df[column_name] = df[column_name].str.replace("¾", "ó")
        # TODO: ... -> Ó
        df[column_name] = df[column_name].str.replace("·", "ú")
        # TODO: ... -> Ú
        df[column_name] = df[column_name].str.replace("±", "ñ")
        df[column_name] = df[column_name].str.replace("&#209", "Ñ")
        df[column_name] = df[column_name].str.upper()
        df[column_name] = df[column_name].str.strip()
        df[column_name] = df[column_name].str.replace("Á", "A")
        df[column_name] = df[column_name].str.replace("É", "E")
        df[column_name] = df[column_name].str.replace("Í", "I")
        df[column_name] = df[column_name].str.replace("Ó", "O")
        df[column_name] = df[column_name].str.replace("Ú", "U")
        return df
    
    @staticmethod
    def word(word: str) -> str:
        """Fixes the formatting of a word to make it standardised.

        :params word: Word to be fixed.
        :type word: str
        :return str: Processed word.
        """
        word = word.upper()
        if "-" in word: word = word.replace("-", " ")
        if "_" in word: word = word.replace("_", " ")
        if "Á" in word: word = word.replace("Á", "A")
        if "É" in word: word = word.replace("É", "E")
        if "Í" in word: word = word.replace("Í", "I")
        if "Ó" in word: word = word.replace("Ó", "O")
        if "Ú" in word: word = word.replace("Ú", "U")
        word = word.strip()
        return word
    
    @staticmethod
    def ip(ip: int | str | None) -> str:
        """Fixes the deleted points of an IP.
        
        :params ip: IP to be fixed.
        :type ip: str | int | None
        :returns str: IP fixed.
        """
        if ip and type(ip) != str or not "." in ip: ip = ".".join(textwrap.wrap(str(ip)[::-1], 3))[::-1]
        elif not ip: ip = ""
        return ip