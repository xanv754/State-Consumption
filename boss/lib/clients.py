import pandas as pd
from tqdm import tqdm
from common import colname
from boss.constant import columns as colboss

class ClientController:

    @staticmethod
    def total_bras_by_state(df: pd.DataFrame) -> pd.DataFrame:
        """Total clients by state and BRAS.

        Parameters
        ----------
        df: DataFrame
            Dataframe with all nodes and their clients by state.

        Returns
        -------
        DataFrame
            A dataframe with the total number of clients by BRAS in each state.
        """
        try:
            df_bras = pd.DataFrame()
            df[colboss.CLIENTS] = df[colboss.CLIENTS].astype(int)
            df = df.sort_values(by=colname.STATE, ascending=True)
            new_df = pd.DataFrame(
                {colname.STATE: list(df[colname.STATE].unique())}
            )
            list_bras = list(
                df.sort_values(by=colname.BRAS, ascending=True)[
                    colname.BRAS
                ].unique()
            )
            for bras_name in tqdm(list_bras):
                clients = (
                    df[df[colname.BRAS] == bras_name]
                    .groupby(colname.STATE)[colboss.CLIENTS]
                    .sum()
                )
                df_merge = new_df.merge(
                    clients, how="outer", on=[colname.STATE], indicator=False
                )
                df_bras[bras_name] = df_merge[colboss.CLIENTS]
                new_df[bras_name] = df_bras[bras_name]
            return new_df
        except Exception as error:
            raise error

    @staticmethod
    def total_porcentage(df: pd.DataFrame) -> pd.DataFrame:
        """Returns percentages of total clients value.

        Parameters
        ----------
        df: DataFrame
            Dataframe with the total clients by state and BRAS.

        Returns
        -------
        DataFrame
            A dataframe with the percentage of total clients value by BRAS in each state.
        """
        try:
            states = df[colname.STATE]
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
                    values.append(round(porcentage, 2))
                df_porcentage[bras_name] = values
            return df_porcentage
        except Exception as error:
            raise error
