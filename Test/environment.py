#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from pathlib import Path
import os
import logging

logging.root.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


from dataManagement.DataParser import Database
from dataManagement.Dictionary import WordsBag

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
            path = os.path.join(self.rootDirectory, "moviesData.db")
        else:
            if info.ignore:
                return None
            path = info.filename
        return Database(path)
    
    def _getWordsBag(self, info=None):
        if info is None:
            path = os.path.join(self.rootDirectory, "dictionary.json")
            erease = False
        else:
            if info.ignore:
                return None
            path = info.filename
            erease = info.erease
        
        return WordsBag(path, erease)

#%%
def getPathFolder(actual_path, folder_to_reach):
    current_path = str(Path(actual_path).parent)
    output = os.path.join(current_path,  folder_to_reach)
    
    while ((not os.path.exists(output)) or (not os.path.isdir(output))) and len(output)!=0:
        path = Path(current_path)
        path_str = str(path)
        current_path = str(path.parent)
        
        if path_str == current_path:
            return None
        
        output = os.path.join(current_path,  folder_to_reach)
        print(output)
    
    
    
    return output

def setupEnv(scirpt_path_execution, info = Info()):
    
    if type(scirpt_path_execution)==str:
        dataset_path = getPathFolder(scirpt_path_execution, _DATASET_FOLDER_NAME)
    else:
        for path in scirpt_path_execution :
            dataset_path = getPathFolder(path, _DATASET_FOLDER_NAME)
            if dataset_path is not None:
                break
    
    if dataset_path is None:
        logging.warning("Cannot find the desired path")
        sys.exit()
    
    return EnvVar(dataset_path, info)
