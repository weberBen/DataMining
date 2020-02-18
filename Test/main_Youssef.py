#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#%%
import environment as Env
import sys, os
import Frequency.SummaryWordFrequency as Freq

#info = Env.Info()
'''
wordsBagInfo = Env.WordsBagInfo(ignore=True)
info = Env.Info(wordsBagInfo=wordsBagInfo)
'''

#env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
#database = env_obj.Database
#wordsBag = env_obj.WordsBag

#F=Freq.Frequency(database,wordsBag)
#print(F._filename)
#F.computeFrequency()
a=Freq.MovieFreq("MoviesFrequence.txt","0")
print(a.file)
it=a.iterator()
#print(a.file.read())
cpt=0
#print(it.hasNext)

while cpt<2:
    #print(cpt)
    test = it.getNext()
    print(test)
    cpt+=1
    



#%%
