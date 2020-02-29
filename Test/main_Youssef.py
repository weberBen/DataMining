#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#%%
import environment as Env
import sys, os
import Frequency.SummaryWordFrequency as Freq
from nltk.stem.porter import *

info = Env.Info()
'''
wordsBagInfo = Env.WordsBagInfo(ignore=True)
info = Env.Info(wordsBagInfo=wordsBagInfo)
'''
'''
env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
database = env_obj.Database
wordsBag = env_obj.WordsBag'''
#F=Freq.Frequency(None,None, "MoviesFrequence.txt")

"""
it = F.iterator2()
cpt = 0
while it.hasNext():
    print("&&&&&&&&&&&&&&&&& MOVIE  &&&&&&&&&&&&&&&&&")
    m = it.getNext()
    print("\tid_movie="+str(m.id))
    itt = m.iterator()
    
    print("----> itration freq movie")
    while itt.hasNext():
        print("id_word, freq=", itt.getNext())
    
    cpt+=1
    
    if cpt==3:
        break
    
"""    
#print(F._filename)
#F.computeFrequency()

'''
F2=Freq.MovieFreq("MoviesFrequence.txt","0")
it=F2.iterator()

cpt=0
while cpt<4:
    test = it.getNext()
    print(test)
    cpt+=1
'''
stemmer = PorterStemmer()
print(stemmer.stem("Frodo Aragorn Gollum Gandalf "))
#%%
