import pandas as pd

def fix_column_word(df: pd.DataFrame, column_name: str):
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