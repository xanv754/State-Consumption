import pandas as pd

class FixFormat:
    """Class to fix the format of the data."""

    @staticmethod
    def column_word(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
        """Fixes a character corruption error in a dataframe column.

        Parameters
        ----------
        df:
            Data to be fixed.
        column_name:
            Name of the column to be fixed.
        """
        df = df.copy()
        # ß -> á
        df[column_name] = df[column_name].str.replace("ß", "a")
        # ┴ -> Á
        df[column_name] = df[column_name].str.replace("┴", "A")
        # Ú -> é
        df[column_name] = df[column_name].str.replace("Ú", "é")
        # TODO: ... -> É
        # Ý -> í
        df[column_name] = df[column_name].str.replace("Ý", "í")
        # TODO: ... -> Í
        # =, ¾ -> ó
        df[column_name] = df[column_name].str.replace("=", "ó")
        df[column_name] = df[column_name].str.replace("¾", "ó")
        # TODO: ... -> Ó
        # · -> ú
        df[column_name] = df[column_name].str.replace("·", "ú")
        # TODO: ... -> Ú
        # ± -> ñ
        df[column_name] = df[column_name].str.replace("±", "ñ")
        # &#209 -> Ñ
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
        
        Parameters
        ----------
        word : str
            Word to be fixed.
        """
        word = word.upper()
        if "-" in word:
            word = word.replace("-", " ")
        if "_" in word:
            word = word.replace("_", " ")
        if "Á" in word:
            word = word.replace("Á", "A")
        if "É" in word:
            word = word.replace("É", "E")
        if "Í" in word:
            word = word.replace("Í", "I")
        if "Ó" in word:
            word = word.replace("Ó", "O")
        if "Ú" in word:
            word = word.replace("Ú", "U")
        word = word.strip()
        return word
    
    @staticmethod
    def ip(ip: int | str | None) -> str:
        """Fixes the deleted points of an IP.
        
        Parameters
        ----------
        ip : int | str | None
            IP to be fixed.
        """
        if (ip is not None) and (type(ip) == int or type(ip) == float or ip.isdigit()):
            ip_string = str(ip)
            ip_string_reversed = "".join(reversed(ip_string))
            i = 0
            fix_ip = ""
            for character in ip_string_reversed:
                if i == 3:
                    fix_ip = fix_ip + "." + character
                    i = 0
                else:
                    fix_ip = fix_ip + character
                i += 1
            fix_ip = "".join(reversed(fix_ip))
            return fix_ip
        elif (ip is not None) and (type(ip) == str):
            ip_split = ip.split('.')
            ip_with_data = [dato for dato in ip_split if dato]
            ip  = '.'.join(ip_with_data)
            return ip
        else:
            return ip