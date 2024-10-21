import pandas as pd
from tqdm import tqdm
from boss.constant import columns as COLUMNS


class ClientController:

    @staticmethod
    def create_usage_for_bras_by_state(df: pd.DataFrame) -> pd.DataFrame:
        try:
            # TODO: Separate ADSL and MDU
            df[COLUMNS.CLIENTS] = df[COLUMNS.CLIENTS].astype(int)
            df_bras = pd.DataFrame()
            df = df.sort_values(by=COLUMNS.NEW_STATE, ascending=True)
            new_df = pd.DataFrame(
                {COLUMNS.NEW_STATE: list(df[COLUMNS.NEW_STATE].unique())}
            )
            list_bras = list(
                df.sort_values(by=COLUMNS.NEW_BRAS, ascending=True)[
                    COLUMNS.NEW_BRAS
                ].unique()
            )
            for bras_name in tqdm(list_bras):
                clients = (
                    df[df[COLUMNS.NEW_BRAS] == bras_name]
                    .groupby(COLUMNS.NEW_STATE)[COLUMNS.CLIENTS]
                    .sum()
                )
                df_merge = new_df.merge(
                    clients, how="outer", on=[COLUMNS.NEW_STATE], indicator=False
                )
                df_bras[bras_name] = df_merge[COLUMNS.CLIENTS]
                new_df[bras_name] = df_bras[bras_name]
            return new_df
        except Exception as error:
            raise error

    @staticmethod
    def create_usage_porcentage(df: pd.DataFrame) -> pd.DataFrame:
        try:
            states = df[COLUMNS.NEW_STATE]
            states.drop([len(df) - 1], axis=0, inplace=True)
            df_porcentage = pd.DataFrame(states)
            bras = df.columns.to_list()
            bras.pop(0)
            bras.pop(-1)
            for bras_name in tqdm(bras):
                values = []
                total = df.iloc[len(df) - 1, df.columns.get_loc(bras_name)]
                for i in range(0, len(df) - 1):
                    clients = df.iloc[i, df.columns.get_loc(bras_name)]
                    porcentage = clients / total
                    values.append(porcentage)
                df_porcentage[bras_name] = values
            return df_porcentage
        except Exception as error:
            raise error

    @staticmethod
    def add_total_sum_by_bras(df: pd.DataFrame) -> pd.DataFrame:
        try:
            index_col = len(df)
            list_columns = df.columns.to_list()[1:]
            df.loc[index_col, df.columns[0]] = COLUMNS.TOTAL_BY_BRAS
            for column_name in tqdm(list_columns):
                df.loc[index_col, column_name] = df[column_name].sum()
            return df
        except Exception as error:
            raise error

    @staticmethod
    def add_total_sum_by_state(df: pd.DataFrame) -> pd.DataFrame:
        try:
            df_filter = df.drop(COLUMNS.NEW_STATE, axis=1)
            df[COLUMNS.TOTAL_BY_STATE] = df_filter.sum(axis=1)
            return df
        except Exception as error:
            raise error
