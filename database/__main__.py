import traceback
import click
from lib.update import UpdateController

@click.group()
def cli():
    """MODULE DATABASE

    This module is used to update the database with nodes.

    \b
    update -f normal   Update the database with the masternode file. 
    update -f input    Update the database with input data.
    """
    pass

def update_by_file():
    try:
        nodes_updated = UpdateController.update_by_file()
        if nodes_updated > 0:
            click.echo(f"The database was updated with {nodes_updated} nodes")
        else: click.echo(f"There are no new nodes to update database")
    except Exception as error:
        raise error

def update_by_input():
    try:
        click.clear()
        click.echo("Enter the information to search node...")
        central = str(input("CENTRAL: "))
        state = str(input("STATE: "))
        account_code = str(input("ACCOUNT CODE: "))
        node = UpdateController.search_node(account_code, central, state)
        if node:
            click.clear()
            id = node.id
            click.echo("Enter the information of the node to be updated to the database")
            click.echo("CURRENT CENTRAL: ", node.central)
            central = str(input("NEW CENTRAL [current]: ")).upper()
            if not central: central = node.central
            click.echo("CURRENT STATE [current]: ", node.state)
            state = str(input("NEW STATE: ")).upper()
            if not state: state = node.state
            click.echo("CURRENT ACCOUNT CODE [current]: ", node.account_code)
            account_code = str(input("NEW ACCOUNT NODE: "))
            if not account_code: account_code = node.account_code
            click.echo("CURRENT IP [current]: ", node.ip)
            ip = str(input("NEW IP: "))
            if not ip: ip = node.ip
            click.echo("CURRENT REGION [current]: ", node.region)
            region = str(input("NEW REGION: ")).upper()

            click.clear()
            if not region: region = node.region
            click.echo("VERIFICATION OF DATA TO BE UPDATED:")
            click.echo("CENTRAL: ", central)
            click.echo("STATE: ", state)
            click.echo("ACCOUNT CODE: ", account_code)
            click.echo("IP: ", ip)
            click.echo("REGION: ", region)
            updated = click.confirm("Confirm you want to update the node?")
            if updated:
                if UpdateController.update_node(id, central, account_code, state, ip, region):
                    click.echo("Node updated!")
                else: click.echo("Oh no... Node not updated")
            else: click.echo("Update canceled")
        else: click.echo("Node not found")
    except Exception as error:
        raise error

@cli.command(help="Update the database.")
@click.option('-f', '--from', help="Specifies where the database is to be updated from.")
def update(option):
    if option == "normal":
        update_by_file()
    elif option == "input":
        update_by_input()
    
@cli.command(help="Create the new node with input data to the database")
def create():
    try:
        click.clear()
        click.echo("Enter the information of the node to be added to the database")
        central = str(input("CENTRAL: "))
        if not central: 
            click.echo("Central is required")
            click.echo("Creation cancelled")
            raise Exception(SystemExit)
        state = str(input("STATE: "))
        if not state:
            click.echo("State is required")
            click.echo("Creation cancelled")
            raise Exception(SystemExit)
        account_code = str(input("ACCOUNT CODE: "))
        if not account_code:
            click.echo("State is required")
            click.echo("Creation cancelled")
            raise Exception(SystemExit)
        ip = str(input("IP [pass]: "))
        region = str(input("REGION [pass]: "))

        click.clear()
        click.echo("VERIFICATION OF DATA TO BE CREATED:")
        click.echo("CENTRAL: ", central)
        click.echo("STATE: ", state)
        click.echo("ACCOUNT CODE: ", account_code)
        click.echo("IP: ", ip)
        click.echo("REGION: ", region)
        updated = click.confirm("Confirm you want to create the node?")
        if updated and UpdateController.create_new_node(central, account_code, state, ip, region):
            click.echo("New node saved!")
        elif updated: 
            click.echo("Oh no... new node not saved")
        else:
            click.echo("Creation cancelled")
    except SystemExit:
        pass
    except Exception as error:
        raise error

if __name__ == "__main__":
    try:
        cli()
    except SystemExit as error:
        if error == 1: pass
    except:
        traceback.print_exc()
