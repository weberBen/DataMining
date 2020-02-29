#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from pathlib import Path

#%%
import environment as Env
import sys, os


info = Env.Info()
'''
wordsBagInfo = Env.WordsBagInfo(ignore=True)
info = Env.Info(wordsBagInfo=wordsBagInfo)
'''

env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
database = env_obj.Database
wordsBag = env_obj.WordsBag





#%%


def test():
    print("\n------------Movies title------------")
    it = database.iterator()
    cpt = 0
    while it.hasNext():
        movie = it.getNext()
        print(movie.title)
        cpt+=1
        
        if cpt==10:
            break
    
    
    '''
    itération sur tous les mots du dictionnaire
    '''
    print("\n------------Words registered------------")
    
    it = wordsBag.iterator()
    cpt = 0
    while it.hasNext():
        word = it.getNext()
        print(word)
        cpt+=1
        
        if cpt==10:
            break
    
    '''
    existence d'un mot dans le dictionnaire
    '''
    
    print("\n------------Tests words in dictionary------------")
    
    word1 = "Frodo"
    word3 = "Gandalf"
    word4 = "geronima"
    
    
    print("1:", (wordsBag.getId(word1) is not None),str(wordsBag.getId(word1)))
    print("3:", (wordsBag.getId(word3) is not None),str(wordsBag.getId(word3)))
    print("4:", (wordsBag.getId(word4) is not None))

#%%
test()
