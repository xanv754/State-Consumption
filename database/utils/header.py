from typing import List
from utils.console import terminal


class HeaderUpdater:
    """Columns of the header required to update the database."""

    STATE: List[str] = ["ESTADO", "STATE"]
    CENTRAL: List[str] = ["CENTRAL", "NODO", "CENTRALES", "NODOS", "NODE", "NODES", "NAME COID"]
    ACCOUNT_CODE: List[str] = ["CC", "CODIGO CONTABLE", "CODIGO_CONTABLE", "ACCOUNT CODE", "ACCOUNT_CODE"]

    def validate(self, header: list) -> bool:
        """Validate the header of the data.
        
        Parameters
        ----------
        header: list
            Header of the data.
        """
        column_state = False
        column_central = False
        column_account_code = False
        for column in header:
            if column in self.STATE: column_state = True
            if column in self.CENTRAL: column_central = True
            if column in self.ACCOUNT_CODE: column_account_code = True
        return column_state and column_central and column_account_code
    
    def get_state_column(self, header: list) -> str:
        """Get the column of the state.
        
        Parameters
        ----------
        header: list
            Header of the data.
        """
        try:
            for column in header:
                if column in self.STATE: return column
            raise ValueError("State column not found")
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}\n {error}")
            exit(1)
    
    def get_central_column(self, header: list) -> str:
        """Get the column of the central.
        
        Parameters
        ----------
        header: list
            Header of the data.
        """
        try:
            for column in header:
                if column in self.CENTRAL: return column
            raise ValueError("Central column not found")
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}\n {error}")
            exit(1)
    
    def get_account_code_column(self, header: list) -> str:
        """Get the column of the account code.
        
        Parameters
        ----------
        header: list
            Header of the data.
        """
        try:
            for column in header:
                if column in self.ACCOUNT_CODE: return column
            raise ValueError("Account code column not found")
        except Exception as error:
            terminal.print(f"[red3]Error in: {__file__}\n {error}")
            exit(1)
