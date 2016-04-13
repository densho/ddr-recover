import json
import os

from models import db, DDRFile, PhotorecFile


def find_meta_files( basedir, recursive=False, model='file', files_first=False, force_read=True, testing=False ):
    """Lists absolute paths to .json files in basedir; saves copy if requested.
    
    Skips/excludes .git directories.
    TODO depth (go down N levels from basedir)
    
    @param basedir: Absolute path
    @returns: list of paths
    """
    def model_exclude(m, p):
        # TODO pass in list of regexes to exclude instead of hard-coding
        exclude = 0
        if m:
            if (m == 'collection') and not ('collection.json' in p):
                exclude = 1
            elif (m == 'entity') and not ('entity.json' in p):
                exclude = 1
            elif (m == 'file') and not (('master' in p.lower()) or ('mezz' in p.lower())):
                exclude = 1
        return exclude
    CACHE_FILENAME = '.metadata_files'
    CACHE_PATH = os.path.join(basedir, CACHE_FILENAME)
    paths = []
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, 'r') as f:
            paths = [line.strip() for line in f.readlines() if '#' not in line]
    else:
        excludes = ['.git', '*~']
        for root, dirs, files in os.walk(basedir):
            # don't go down into .git directory
            if '.git' in dirs:
                dirs.remove('.git')
            for f in files:
                if f.endswith('.json'):
                    path = os.path.join(root, f)
                    exclude = [1 for x in excludes if x in path]
                    modexclude = model_exclude(model, path)
                    if not (exclude or modexclude):
                        paths.append(path)
    return paths

#        "path_rel": "ddr-testing-141-2-master-c467381d46.pdf"
#        "sha1": "c467381d4610639d77ccf54c82f531ea8508a788"
#        "sha256": "d632157e3c3d6c2d8a425060a2c9d63524458493414db3e497bc8266d903ecfd"
#        "md5": "c11c2c3cbd06b91cd3c4fab6faf0bfba"
#        "size": 30324543

def extract_data(path, basedir):
    FIELDS = [
        'path_rel',
        'sha256',
        'size',
    ]
    with open(path, 'r') as f:
        text = f.read()
    record = {}
    for field in json.loads(text):
        for key,val in field.iteritems():
            if key in FIELDS:
                record[key] = val
    # calculate
    filename = record.pop('path_rel')
    file_id = os.path.splitext(filename)[0]
    collection_id = '-'.join(file_id.split('-')[:3])
    meta_path_rel = os.path.relpath(path, basedir)
    files_dir_abs = os.path.dirname(path)
    files_dir_rel = os.path.dirname(meta_path_rel)
    path_abs = os.path.join(files_dir_abs, filename)
    path_rel = os.path.join(files_dir_rel, filename)
    annex_path_abs = os.path.realpath(path_abs)
    annex_path_rel = os.path.relpath(annex_path_abs, basedir)
    data = {
        'sha256': record['sha256'],
        'file_id': file_id,
        'collection_id': collection_id,
        'path_rel': path_rel,
        'annex_path_rel': annex_path_rel,
    }
    return data

def make_object(data):
    ddrfile = DDRFile()
    ddrfile.sha256 = data['sha256']
    ddrfile.annex_path_rel = data['annex_path_rel']
    ddrfile.path_rel = data['path_rel']
    ddrfile.file_id = data['file_id']
    ddrfile.collection_id = data['collection_id']
    return ddrfile

def save_object(ddrfile):
    existing = DDRFile.get(DDRFile.sha256 == ddrfile.sha256)
    if not existing:
        ddrfile.save(force_insert=True)


BASEDIR = '/tmp/ddr-testing-141'
paths = find_meta_files(BASEDIR)
for path in paths:
    print(path)
    data = extract_data(path, BASEDIR)
    ddrfile = make_object(data)
    save_object(ddrfile)
