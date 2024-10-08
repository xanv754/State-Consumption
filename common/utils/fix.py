import pandas as pd

def fix_column_word(df: pd.DataFrame, column_name: str):
    try:
        # ß -> á
        df[column_name] = df[column_name].str.replace('ß', 'a')
        # Ú -> é
        df[column_name] = df[column_name].str.replace('Ú', 'é')
        # Ý -> í
        df[column_name] = df[column_name].str.replace('Ý', 'í')
        # =, ¾ -> ó
        df[column_name] = df[column_name].str.replace('=', 'ó')
        df[column_name] = df[column_name].str.replace('¾', 'ó')
        # · -> ú
        df[column_name] = df[column_name].str.replace('·', 'ú')
        # ± -> ñ
        df[column_name] = df[column_name].str.replace('±', 'ñ')
        # &#209 -> Ñ
        df[column_name] = df[column_name].str.replace('&#209', 'Ñ')
        return df
    except Exception as error:
        raise error