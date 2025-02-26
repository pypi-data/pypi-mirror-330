import click
import uvicorn


@click.group(help="Run MAGMA web server.")
def run():
    pass


@run.command()
@click.option('--host', '-h', default="127.0.0.1", help='Default 127.0.0.1')
@click.option('--port', '-p', default=8000, help='Default 8000')
def dev(host: str, port: int):
    print(f'Run MAGMA webserver development on {host}:{port}.')
    uvicorn.run("magma_indonesia:app", host=host, port=port, reload=True)
