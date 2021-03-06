# script for collecting hashes of collection binaries
#  
# Finds all the FILE.json files in collection
# Collects info for each file:
# - collection id
# - file id
# - hash (SHA256?)
# - working file path (relative to collection dir)
# - annex objects file path (relative to collection dir)

import os

from peewee import *

from config import db

class DDRFile(Model):
    sha256 = CharField(primary_key=True)
    annex_path_rel = CharField()
    path_rel = CharField()
    file_id = CharField()
    collection_id = CharField()

    class Meta:
        database = db

    def dumpcsv(self):
        return ','.join([
            self.sha256,
            self.annex_path_rel,
            self.path_rel,
            self.file_id,
            self.collection_id,
        ])
    
    @staticmethod
    def count_collections():
        SQL = 'SELECT collection_id FROM ddrfile';
        return set([cid for cid in db.execute_sql(SQL)])

class PhotorecFile(Model):
    sha256 = CharField(primary_key=True)
    path_rel = CharField()

    class Meta:
        database = db
    
    def dumpcsv(self):
        return ','.join([
            self.sha256,
            self.path_rel
        ])
    
    @staticmethod
    def count_dirs():
        SQL = 'SELECT path_rel FROM photorecfile';
        return set([
            # get just the photorec dirname
            fields[0].split('/')[0]
            # fields is a list
            for fields in db.execute_sql(SQL)
        ])


COUNT_SQL = """
SELECT count(*) FROM %s;
"""
MATCH_SQL = """
SELECT p.sha256, p.path_rel, d.collection_id, d.annex_path_rel
FROM ddrfile d, photorecfile p
WHERE p.sha256 = d.sha256;
"""
def link_photorec_ddr():
    """
    """
    src_dest = []
    for sha256,src_path_rel,cid,annex_path_rel in db.execute_sql(MATCH_SQL,):
        src_dest.append([
            src_path_rel,
            os.path.join(cid, annex_path_rel)
        ])
    return src_dest

def count_files(table):
    return [
        x for x in db.execute_sql(COUNT_SQL % table)
    ][0]
