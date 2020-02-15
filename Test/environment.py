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
import sys

logging.root.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

DATASET_FOLDER_NAME = "Dataset"

class EnvVar:
    def __init__(self, root_directory):
        self.rootDirectory = root_directory
        self.Database = self._getDatabase()
        self.WordsBag = self._getWordsBag()
    
    def _getDatabase(self):
        path = os.path.join(self.rootDirectory, "CleanMovieData.zip")
        return Database(path)
    
    def _getWordsBag(self):
        path = os.path.join(self.rootDirectory, "dictionnary")
        return WordsBag(path)

