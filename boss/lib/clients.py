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
            for bras_name in tqdm(list_bras, desc="Calculating clients by state..."):
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
    def total_porcentage(df1: pd.DataFrame, df2: pd.DataFrame = None) -> pd.DataFrame:
        """Returns percentages of total clients value.

        Parameters
        ----------
        df1: DataFrame
            Dataframe ADSL or MDU with the total clients by state and BRAS.
        df2: DataFrame
            Dataframe ADSL or MDU with the total clients by state and BRAS.
            
        Returns
        -------
        DataFrame
            A dataframe with the percentage of total clients value by BRAS in each state.
        """
        try:
            states = df1[colname.STATE]
            states.drop([len(df1) - 1], axis=0, inplace=True)
            df_porcentage = pd.DataFrame(states)
            bras = df1.columns.to_list()
            bras.pop(0)
            bras.pop(-1)
            for bras_name in tqdm(bras, desc="Calculating total clients..."):
                values = []
                total_adsl = df1[bras_name].iloc[len(df1) - 1]
                if bras_name in df2.columns.to_list(): total_mdu = df2[bras_name].iloc[len(df2) - 1]
                else: total_mdu = 0
                total = total_adsl + total_mdu
                for i in range(0, len(df1[bras_name]) - 1):
                    clients = df1[bras_name][i]
                    porcentage = (clients * 100) / total
                    values.append(round(porcentage, 2))
                df_porcentage[bras_name] = values
            return df_porcentage
        except Exception as error:
            raise error

    @staticmethod
    def total_by_bras(df_adsl: pd.DataFrame, df_mdu: pd.DataFrame) -> pd.DataFrame:
        """Total clients by bras.

        Parameters
        ----------
        df_adsl: DataFrame
            Dataframe ADSL with the total clients by state and BRAS.
        df_mdu: DataFrame
            Dataframe MDU with the total clients by state and BRAS.

        Returns
        -------
        DataFrame
            A dataframe with the total number of clients by BRAS.
        """
        try:
            data = {
                "AGREGADOR": [],
                "ADSL": [],
                "MDU": [],
                "TOTAL": []
            }
            brasnames = list(set(list(df_adsl[colname.BRAS].unique()) + list(df_mdu[colname.BRAS].unique())))
            brasnames.sort()
            bras_short_names = []
            for bras in brasnames:
                new_bras = bras[0:3]
                if not new_bras in bras_short_names:
                    bras_short_names.append(new_bras)
            bras_short_names.sort()
            for bras_short in tqdm(bras_short_names, desc="Generating total clients for each bras..."):
                data["AGREGADOR"].append(bras_short)
                total_adsl = 0
                total_mdu = 0   
                for bras in brasnames:
                    if bras[0:3] == bras_short:
                        total_adsl += df_adsl[df_adsl[colname.BRAS] == bras][colboss.CLIENTS].sum()
                        total_mdu += df_mdu[df_mdu[colname.BRAS] == bras][colboss.CLIENTS].sum()
                data["ADSL"].append(total_adsl)
                data["MDU"].append(total_mdu)
                data["TOTAL"].append(total_adsl + total_mdu)
            df = pd.DataFrame(data)
            return df
        except Exception as error:
            raise error