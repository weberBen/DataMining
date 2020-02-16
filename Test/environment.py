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

#%%


class WordsBagInfo:
    def __init__(self, filename=None, erease=False, ignore=False):
        self.ignore = ignore
        self.filename = filename
        self.erease = erease
    
        
class DatabaseInfo:
    def __init__(self, filename=None, ignore=False):
        self.ignore = ignore
        self.filename = filename

class Info:
    def __init__(self, databaseInfo=None, wordsBagInfo=None):
        self.databaseInfo = databaseInfo
        self.wordsBagInfo = wordsBagInfo

#%%
        
class EnvVar:
    def __init__(self, root_directory, info = Info()):
        self.rootDirectory = root_directory
        
        self.Database = self._getDatabase(info.databaseInfo)
        self.WordsBag = self._getWordsBag(info.wordsBagInfo)
    
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
def getPathFolder(actual_path, folder_to_reach):
    current_path = Path(actual_path).parent
    output = os.path.join(current_path,  folder_to_reach)
    
    while ((not os.path.exists(output)) or (not os.path.isdir(output))) and len(output)!=0:
        path = Path(current_path)
        current_path = path.parent
        
        if path == current_path:
            logging.warning("Cannot find the desired path")
            sys.exit()
        
        output = os.path.join(current_path,  folder_to_reach)
    
    
    return output

def setupEnv(scirpt_path_execution, info = Info()):
    dataset_path = getPathFolder(scirpt_path_execution, _DATASET_FOLDER_NAME)
    return EnvVar(dataset_path, info)
