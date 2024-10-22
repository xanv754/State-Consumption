import pandas as pd 
from tqdm import tqdm
from common.constant import colname

def add_total_sum_by_col(df: pd.DataFrame, name_col="TOTAL COL") -> pd.DataFrame:
    try:
        index_col = len(df)
        list_columns = df.columns.to_list()[1:]
        df.loc[index_col, df.columns[0]] = name_col
        for column_name in list_columns:
            df.loc[index_col, column_name] = df[column_name].sum()
        return df
    except Exception as error:
        raise error
    
def add_total_sum_by_row(df: pd.DataFrame, name_row="TOTAL ROW") -> pd.DataFrame:
    try:
        if colname.STATE in df.columns.to_list():
            df_filter = df.drop(colname.STATE, axis=1)
        df[name_row] = df_filter.sum(axis=1)
        return df
    except Exception as error:
        raise error