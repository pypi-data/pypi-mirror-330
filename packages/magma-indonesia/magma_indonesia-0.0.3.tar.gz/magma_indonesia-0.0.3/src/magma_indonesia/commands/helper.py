import click
from magma_database.helper import copy_env as copy_environment


@click.group(help="Helper command.")
def helper():
    pass


@helper.command()
@click.option('--overwrite', '-o', default=False, is_flag=True, help='Overwrite existing ENV file.')
def copy_env(overwrite: bool):
    copy_environment(overwrite=overwrite)
