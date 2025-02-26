import click
from magma_database.database import migrate as db_migration


@click.group(help="Database command.")
def database():
    pass


@database.command()
@click.option('--force', '-f', default=False, is_flag=True, help='Force delete or drop database table.')
def migrate(force: bool):
    db_migration(force=force)