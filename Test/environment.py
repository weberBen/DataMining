#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from pathlib import Path
import os
import logging


logging.root.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


from dataManagement.DataParser import Database
from dataManagement.Dictionnary import WordsBag

_DATASET_FOLDER_NAME = "Dataset"
DATASET_PATH = None


#%%
def getEnvPath(folder_to_reach):
    current_path = Path(sys.argv[0]).parent
    output = os.path.join(current_path,  folder_to_reach)
    
    while ((not os.path.exists(output)) or (not os.path.isdir(output))) and len(output)!=0:
        current_path = Path(current_path).parent
        output = os.path.join(current_path,  folder_to_reach)
    
    
    return output

#%%
    
DATASET_PATH = getEnvPath(_DATASET_FOLDER_NAME)


#%%


class WordsBagInfo:
    def __init__(self, filename, erease, ignore):
        self.ignore = ignore
        self.filename = filename
        self.erease = erease
        
class DatabaseInfo:
    def __init__(self, filename, ignore):
        self.ignore = ignore
        self.filename = filename
        
class EnvVar:
    def __init__(self, root_directory, databaseInfo=None, wordsBagInfo=None):
        self.rootDirectory = root_directory
        
        self.Database = self._getDatabase(databaseInfo)
        self.WordsBag = self._getWordsBag(wordsBagInfo)
    
    def _getDatabase(self, info=None):
        if info is None:
            path = os.path.join(self.rootDirectory, "CleanMovieData.zip")
        else:
            if info.ignore:
                return None
            path = info.filename
        return Database(path)
    
    def _getWordsBag(self, info=None):
        if info is None:
            path = os.path.join(self.rootDirectory, "dictionnary.json")
            erease = False
        else:
            if info.ignore:
                return None
            path = info.filename
            erease = info.erease
        
        return WordsBag(path, erease)

#%%
