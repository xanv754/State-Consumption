import pandas as pd

def fix_column_word(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Fixes a character corruption error in a dataframe column.

    Parameters
    ----------
    df: 
        Data to be fixed.
    column_name: 
        Name of the column to be fixed.
    """
    try:
        # ß -> á
        df[column_name] = df[column_name].str.replace('ß', 'a')
        # ┴ -> Á
        df[column_name] = df[column_name].str.replace('┴', 'A')
        # Ú -> é
        df[column_name] = df[column_name].str.replace('Ú', 'é')
        # TODO: ... -> É
        # Ý -> í
        df[column_name] = df[column_name].str.replace('Ý', 'í')
        # TODO: ... -> Í
        # =, ¾ -> ó
        df[column_name] = df[column_name].str.replace('=', 'ó')
        df[column_name] = df[column_name].str.replace('¾', 'ó')
        # TODO: ... -> Ó
        # · -> ú
        df[column_name] = df[column_name].str.replace('·', 'ú')
        # TODO: ... -> Ú
        # ± -> ñ
        df[column_name] = df[column_name].str.replace('±', 'ñ')
        # &#209 -> Ñ
        df[column_name] = df[column_name].str.replace('&#209', 'Ñ')
        return df
    except Exception as error:
        raise error
    
def fix_format_word(word: str) -> str:
    """Fixes the formatting of a word to make it standardised."""
    try:
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
    except Exception as error:
        raise error
    
def fix_ip(ip: int) -> str:
    """Fixes the deleted points of an IP."""
    if type(ip) == int:
        ip_string = str(ip)
        ip_string_reversed = "".join(reversed(ip_string))
        i = 0
        fix_ip = ''
        for character in ip_string_reversed:
            if i == 3: 
                fix_ip = fix_ip + '.' + character
                i = 0
            else: fix_ip = fix_ip + character
            i += 1
        fix_ip = "".join(reversed(fix_ip))
        return fix_ip
    else: return ip