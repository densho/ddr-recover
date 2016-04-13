# script for collecting hashes of collection binaries
#  
# Finds all the FILE.json files in collection
# Collects info for each file:
# - collection id
# - file id
# - hash (SHA256?)
# - working file path (relative to collection dir)
# - annex objects file path (relative to collection dir)

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

class PhotorecFile(Model):
    sha256 = CharField(primary_key=True)
    path_rel = CharField()

    class Meta:
        database = db
