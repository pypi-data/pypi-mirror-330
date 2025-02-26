import click
from magma_indonesia.commands import run
from magma_indonesia.commands import db
from magma_indonesia.commands import convert
from magma_indonesia.commands import helper


@click.group(help="CLI tool run MAGMA Indonesia.")
def cli():
    pass


cli.add_command(convert.convert)
cli.add_command(helper.helper)
cli.add_command(run.run)
cli.add_command(db.db)

if __name__ == '__main__':
    cli()
