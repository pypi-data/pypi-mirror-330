import click
from datetime import datetime, timedelta

current_date = datetime.today()


def start_date() -> str:
    return (current_date - timedelta(days=1)).strftime('%Y-%m-%d')


def end_date() -> str:
    return current_date.strftime('%Y-%m-%d')


@click.group(help="Convert seismic data to SDS Format.")
def convert():
    pass


@convert.command()
@click.option('--station', '-s', default="*", help='Default * all stations.')
@click.option('--channel', '-c', default='EHZ', help='Default EHZ channel.')
@click.option('--network', '-n', default='VG', help='Default VG.')
@click.option('--location', '-l', default='00', help='Default 00.')
@click.option('--start', '-s', default=start_date(), help='Start time of seismic data.')
@click.option('--end', '-e', default=end_date(), help='End time of seismic data.')
def run(station: str,
        channel: str,
        network: str,
        location: str,
        start: str,
        end: str):
    print(f'Station: {station}, Network: {network}')
    print(f'Start date: {start}, End date: {end}')
