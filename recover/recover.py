import click

import ddr
import photorec


@click.group()
def recover():
    """Simple program that does something.
    """
    pass

@recover.command()
@click.argument('source')
@click.argument('path')
def get(source, path):
    """Get data for binaries from DDR collection repo or photorec dir.
    """
    if source == 'ddr':
        ddr.process_collection(path)
    elif source == 'photorec':
        photorec.process_dir(path)

@recover.command()
@click.argument('source')
def dumpcsv(source):
    """Dump data from source to commandline in CSV format.
    """
    if source == 'ddr':
        ddr.dump()
    elif source == 'photorec':
        photorec.dump()


if __name__ == '__main__':
    recover()
