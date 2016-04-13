import click

import ddr
import photorec
import models


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

@recover.command()
def link():
    """Match photorec files to DDR files
    """
    for src_dest in models.link_photorec_ddr():
        print(','.join(src_dest))

@recover.command()
def stats():
    """Print stats
    """
    collections = models.DDRFile.count_collections()
    photorec_dirs = models.PhotorecFile.count_dirs()
    num_ddr = models.count_files('ddrfile')
    num_photorec = models.count_files('photorecfile')
    src_dest = models.link_photorec_ddr()
    num_match = len(src_dest)
    print('ddr collections: %s' % len(collections))
    print('  photorec dirs: %s' % len(photorec_dirs))
    print('      ddr files: %s' % num_ddr)
    print(' photorec files: %s' % num_photorec)
    print('        matches: %s' % num_match)
    


if __name__ == '__main__':
    recover()
