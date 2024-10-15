import pandas as pd
from tqdm import tqdm
from common.constant.columns import ReportColumns

class TableController:

    @staticmethod
    def create_usage_for_bras_by_state(df: pd.DataFrame) -> pd.DataFrame:
        try:
            #TODO: Separate ADSL and MDU
            tqdm.write("Create merge between BRAS and State Node...")
            df[ReportColumns.CLIENTS] = df[ReportColumns.CLIENTS].astype(int)
            df_bras = pd.DataFrame()
            df = df.sort_values(by=ReportColumns.STATE, ascending=True)
            new_df = pd.DataFrame({ReportColumns.STATE: list(df[ReportColumns.STATE].unique())})
            list_bras = list(df.sort_values(by="bras", ascending=True)["bras"].unique())
            for bras_name in tqdm(list_bras):
                clients = df[df["bras"] == bras_name].groupby(ReportColumns.STATE)[ReportColumns.CLIENTS].sum()
                df_merge = new_df.merge(clients, how="outer", on=[ReportColumns.STATE], indicator=False)
                df_bras[bras_name] = df_merge[ReportColumns.CLIENTS]
                new_df[bras_name] = df_bras[bras_name]
            return new_df
        except Exception as error:
            raise error

    def create_usage_porcentage(df: pd.DataFrame) -> pd.DataFrame:
        try:
            tqdm.write("Create usage porcentage...")
            states = df["Estado"]
            states.drop([len(df) - 1], axis=0, inplace=True)
            df_porcentage = pd.DataFrame(states)
            bras = df.columns.to_list()
            bras.pop(0)
            bras.pop(-1)
            for bras_name in tqdm(bras):
                values = []
                total = df.iloc[len(df) - 1, df.columns.get_loc(bras_name)]
                for i in range(0, len(df) - 1):
                    clients = (df.iloc[i, df.columns.get_loc(bras_name)])
                    porcentage = clients / total
                    values.append(porcentage)
                df_porcentage[bras_name] = values
            return df_porcentage
        except Exception as error:
            raise error

    @staticmethod
    def add_total_sum_by_bras(df: pd.DataFrame) -> pd.DataFrame:
        try:
            tqdm.write("Add total col sum...")
            index_col = len(df)
            list_columns = df.columns.to_list()[1:]
            df.loc[index_col, df.columns[0]] = ReportColumns.TOTAL_BY_BRAS
            for column_name in tqdm(list_columns):
                df.loc[index_col, column_name] = df[column_name].sum()
            return df
        except Exception as error:
            raise error

    @staticmethod
    def add_total_sum_by_state(df: pd.DataFrame) -> pd.DataFrame:
        try:
            tqdm.write("Add total row sum...")
            df_filter = df.drop(ReportColumns.STATE, axis=1)
            df[ReportColumns.TOTAL_BY_STATE] = df_filter.sum(axis=1)
            return df
        except Exception as error:
            raise error
