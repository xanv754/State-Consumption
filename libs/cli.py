import rich
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from database.libs.mongo import MongoDatabase
from database.querys.nodes import NodesQueryMongo
from database.model.node import NodeModel
from libs.process import DataProcess


class DatabaseCLIHandler:
    """Handler to operate with the database to CLI."""

    def make_migration(self) -> bool:
        mongo = MongoDatabase()
        if mongo.connected:
            return mongo.migration()
        

    def rollback(self) -> bool:
        mongo = MongoDatabase()
        if mongo.connected:
            return mongo.rollback()
        
    
    def add_new_node(self) -> bool:
        state = Prompt.ask("State of new node")
        if not state: 
            rich.print("[yellow2]Warning: State of node is required")
            return False
        state = state.upper()
        central = Prompt.ask("Central of new node")
        if not central: 
            rich.print("[yellow2]Warning: Central of node is required")
            return False
        central = central.upper()
        account_code = Prompt.ask("Account code of new node")
        if not account_code: 
            rich.print("[yellow2]Warning: Account code of node is required")
            return False
        ip = Prompt.ask("IP of new node")
        if not ip: ip = None
        region = Prompt.ask("Region of new node")
        if not region: region = None
        else: region = region.upper()
        new_node = NodeModel(
            state=state, 
            central=central, 
            account_code=account_code, 
            ip=ip, 
            region=region
        )
        
        console = Console()
        console.clear()
        table = Table(title="New node")
        table.add_column("Field", justify="right", style="cyan", no_wrap=True)
        table.add_column("Value", justify="left", style="yellow")
        table.add_row("State", new_node.state)
        table.add_row("Central", new_node.central)
        table.add_row("Account code", new_node.account_code)
        table.add_row("IP", new_node.ip)
        table.add_row("Region", new_node.region)
        console.print(table)

        response = Prompt.ask("Are you sure you want to add this node to the database? (y/N)")
        if not response or response.lower() != "y": exit(0)

        return NodesQueryMongo.insert_one(node=new_node)
    

class ProcessCLIHandler:
    """Handler to process the data to CLI."""

    def main(self, boss_path: str, consumption_path: str, process_consumption: bool) -> bool:
        data = DataProcess(
            boss_path=boss_path, 
            consumption_path=consumption_path, 
            process_consumption=process_consumption
        )
        df = data.process()
        print(df)
        return True
