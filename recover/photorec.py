# script for collection file hashes from photorec recovery dir


# BASE/recup_dir.N/
# BASE/recup_dir.15/f99133440.pdf

from datetime import datetime
import hashlib
import os

from models import db, DDRFile, PhotorecFile


def file_hash(path, algo='sha1'):
    if algo == 'sha256':
        h = hashlib.sha256()
    elif algo == 'md5':
        h = hashlib.md5()
    else:
        h = hashlib.sha1()
    block_size=1024
    f = open(path, 'rb')
    while True:
        data = f.read(block_size)
        if not data:
            break
        h.update(data)
    f.close()
    return h.hexdigest()


def extract_data(path, basedir):
    dirname = os.path.basename(os.path.normpath(basedir))
    path_abs = os.path.join(basedir, path)
    path_rel = os.path.join(dirname, path)
    sha256 = file_hash(path_abs, 'sha256')
    data = {
        'sha256': sha256,
        'path_rel': path_rel,
    }
    return data

def make_object(data):
    """make a database object
    """
    o = PhotorecFile()
    o.sha256 = data['sha256']
    o.path_rel = data['path_rel']
    return o

def save_object(o):
    """save object to database if not already existing
    """
    try:
        existing = PhotorecFile.get(PhotorecFile.sha256 == o.sha256)
    except:
        existing = False
    
    if existing:
        return False
    else:
        o.save(force_insert=True)
        return True
    
def process_dir(dir_path):
    print('%s %s' % (datetime.now(), dir_path))
    paths = os.listdir(dir_path)
    num = len(paths)
    for n,path in enumerate(paths):
        data = extract_data(path, dir_path)
        o = make_object(data)
        new = save_object(o)
        if new:
            status = '+'
        else:
            status = ' '
        now = datetime.now()
        print('%s %s/%s %s %s %s' % (
            now, n, num, status, o.path_rel, o.sha256)
        )
    print('%s DONE %s' % (datetime.now(), dir_path))
