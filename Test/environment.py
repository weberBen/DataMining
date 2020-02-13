#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 20:54:45 2020

@author: benjamin
"""
from dataManagement.DataParser import Database
from dataManagement.Dictionnary import WordsBag
import os

class EnvVar:
    def __init__(self, root_directory):
        self.rootDirectory = root_directory
        self.Database = self.__getDatabase__()
        self.WordsBag = self.__getWordsBag__()
        
    def __getDatabase__(self):
        path = os.path.join(self.rootDirectory, "CleanMovieData")
        return Database(path)
    
    def __getWordsBag__(self):
        path = os.path.join(self.rootDirectory, "dictionnary")
        return WordsBag(path)

