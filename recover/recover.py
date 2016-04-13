import click

from ddr import process_collection
from photorec import process_dir


@click.group()
def recover():
    """Simple program that does something.
    """
    pass

@recover.command()
@click.argument('path')
def ddr(path):
    """Get data for binaries in DDR collection repo.
    """
    process_collection(path)

@recover.command()
@click.argument('path')
def photorec(path):
    """Get hashes and paths for files in photorec dir.
    """
    process_dir(path)


if __name__ == '__main__':
    recover()
