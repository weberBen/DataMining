#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 20:54:45 2020

@author: benjamin
"""
from dataManagement.DataParser import Database
from dataManagement.Dictionnary import WordsBag
import os
import logging

logging.root.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

DATASET_FOLDER_NAME = "Dataset"

class WordsBagInfo:
    def __init__(self, filename, erease):
        self.filename = filename
        self.erease = erease
        
class DatabaseInfo:
    def __init__(self, filename):
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
            path = info.filename
        return Database(path)
    
    def _getWordsBag(self, info=None):
        if info is None:
            path = os.path.join(self.rootDirectory, "dictionnary.json")
            erease = False
        else:
            path = info.filename
            erease = info.erease
        
        return WordsBag(path, erease)

