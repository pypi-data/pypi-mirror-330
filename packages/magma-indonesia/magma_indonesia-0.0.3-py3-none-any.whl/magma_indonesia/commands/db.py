import click


@click.group(help="Database command for MAGMA Indonesia.")
def db():
    pass


@db.command()
@click.option('--force', '-f', default=False, is_flag=True, help='Overwrite existing database.')
def migrate(force: bool = False) -> None:
    pass
