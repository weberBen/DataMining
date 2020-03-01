#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from pathlib import Path
import os
import logging

logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


from dataManagement.DataParser import Database
from dataManagement.Dictionary import WordsBag
import Frequency.SummaryWordFrequency as SWF

_DATASET_FOLDER_NAME = "Dataset"
_ASSETS_FOLDER_NAME = "Assets"


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
        
class FreqInfo:
    def __init__(self, database=None, wordsBag=None, filename=None, ignore=False):
        self.database = database
        self.wordsBag = wordsBag
        self.ignore = ignore
        self.filename = filename

class Info:
    def __init__(self, databaseInfo=None, wordsBagInfo=None, frequencyInfo=None):
        self.databaseInfo = databaseInfo
        self.wordsBagInfo = wordsBagInfo
        self.frequencyInfo = frequencyInfo

#%%
        
class EnvVar:
    def __init__(self, root_directory, assets_directory, info = Info(), ignore_all = False):
        self.datasetDirectory = root_directory
        self.assetsDirectory = assets_directory
        
        if not ignore_all:
            self.Database = self._getDatabase(info.databaseInfo)
            self.WordsBag = self._getWordsBag(info.wordsBagInfo)
            self.Frequency = self._getFreq(info.frequencyInfo)
        
    
    def getDatasetFolder(self):
        return self.datasetDirectory
    
    def getAssetsDirectory(self):
        return self.assetsDirectory
    
    def getMatrixFolder(self):
        return os.path.join(self.datasetDirectory, "matrix")
    
    def _getDatabase(self, info=None):
        if info is None:
            path = os.path.join(self.datasetDirectory, "moviesData.db")
        else:
            if info.ignore:
                return None
            path = info.filename
        return Database(path)
    
    def _getWordsBag(self, info=None):
        if info is None:
            path = os.path.join(self.datasetDirectory, "dictionary.json")
            erease = False
        else:
            if info.ignore:
                return None
            path = info.filename
            erease = info.erease
            
        return WordsBag(path, erease)
    
    def _getFreq(self, info=None):
        if info is None:
            database = self.Database
            wordsBag = self.WordsBag
            filename = os.path.join(self.datasetDirectory, "MoviesFrequence.txt")
        else :
            if info.ignore:
                return None
            database = info.database
            wordsBag = info.wordsBag
            filename = info.filename
            
        
        return SWF.Frequency(database, wordsBag, filename)

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
    
    
    
    return output

def getPath(scirpt_path_execution, directory_name):
    if type(scirpt_path_execution)==str:
        path = getPathFolder(scirpt_path_execution, directory_name)
    else:
        for _path in scirpt_path_execution :
            path = getPathFolder(_path, directory_name)
            if path is not None:
                break
    return path

def setupEnv(scirpt_path_execution, info = Info()):
    
    dataset_path = getPath(scirpt_path_execution, _DATASET_FOLDER_NAME)
    if dataset_path is None:
        logging.error("Cannot find the dataset path")
        sys.exit()
    
    assets_path = getPath(scirpt_path_execution, _ASSETS_FOLDER_NAME)
    if assets_path is None:
        logging.error("Cannot find the assets path")
        sys.exit()
    
    return EnvVar(dataset_path, assets_path, info)

#%%

