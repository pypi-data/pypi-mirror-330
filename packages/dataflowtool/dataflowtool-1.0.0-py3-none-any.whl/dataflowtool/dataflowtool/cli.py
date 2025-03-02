import click
from .server import run_server

@click.group()
def cli():
    """Data Flow Tool - Column-level lineage visualization for DBT Core"""
    pass

@cli.command()
def serve():
    """Start the Data Flow Tool server"""
    run_server()

if __name__ == "__main__":
    cli() 