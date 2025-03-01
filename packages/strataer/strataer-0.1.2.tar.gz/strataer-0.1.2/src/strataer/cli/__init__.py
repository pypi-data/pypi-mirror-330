import click
from strataer.cli.runner import cli_run


@click.command()
@click.argument("config", nargs=1, type=click.Path(exists=True))
def run(config):
    """Interpolate the CMIP7 stratospheric aerosol forcing to new wavelength bands.

    Example
    -------

    >>> convert-cmip7 "config.yaml"

    """
    cli_run(config)
