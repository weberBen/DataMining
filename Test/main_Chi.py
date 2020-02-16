#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#%%
import environment as Env
import sys
from querySystem.matrixOp import *
from dataManagement.Dictionnary import WordsBag

info = Env.Info()
'''
wordsBagInfo = Env.WordsBagInfo(ignore=True)
info = Env.Info(wordsBagInfo=wordsBagInfo)
'''

env_obj = Env.setupEnv(sys.argv[0], info)
database = env_obj.Database
wordsBag = env_obj.WordsBag

if __name__ == "__main__":
    A, V = createTFMatrixV2("./querySystem", mute = False)
    print(A.toarray())
    print(V.toarray())
    print(wordsBag.getIds("Bonjour"))
    Q = createQueryVect(wordsBag, input("Recherche : "))
    print(Q)

#%%
