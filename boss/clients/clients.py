import pandas as pd
from tqdm import tqdm
from common.constant.columns import ColumnsReport

class TableController:

    @staticmethod
    def create_usage_for_bras_by_state(df: pd.DataFrame) -> pd.DataFrame:
        try:
            #TODO: Separate ADSL and MDU
            tqdm.write("Create merge between BRAS and State Node...")
            df[ColumnsReport.CLIENTS] = df[ColumnsReport.CLIENTS].astype(int)
            df_bras = pd.DataFrame()
            df = df.sort_values(by=ColumnsReport.STATE, ascending=True)
            new_df = pd.DataFrame({ColumnsReport.STATE: list(df[ColumnsReport.STATE].unique())})
            list_bras = list(df.sort_values(by="bras", ascending=True)["bras"].unique())
            for bras_name in tqdm(list_bras):
                clients = df[df["bras"] == bras_name].groupby(ColumnsReport.STATE)[ColumnsReport.CLIENTS].sum()
                df_merge = new_df.merge(clients, how="outer", on=[ColumnsReport.STATE], indicator=False)
                df_bras[bras_name] = df_merge[ColumnsReport.CLIENTS]
                new_df[bras_name] = df_bras[bras_name]
            return new_df
        except Exception as error:
            raise error

    @staticmethod
    def add_total_sum_by_bras(df: pd.DataFrame) -> pd.DataFrame:
        try:
            tqdm.write("Add total col sum...")
            index_col = len(df)
            list_columns = df.columns.to_list()[1:]
            df.loc[index_col, df.columns[0]] = ColumnsReport.TOTAL_BY_BRAS
            for column_name in tqdm(list_columns): 
                df.loc[index_col, column_name] = df[column_name].sum()
            return df
        except Exception as error:
            raise error
        
    @staticmethod
    def add_total_sum_by_state(df: pd.DataFrame) -> pd.DataFrame:
        try:
            tqdm.write("Add total row sum...")
            df_filter = df.drop(ColumnsReport.STATE, axis=1)
            df[ColumnsReport.TOTAL_BY_STATE] = df_filter.sum(axis=1)
            return df
        except Exception as error:
            raise error