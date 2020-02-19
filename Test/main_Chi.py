#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#%%
import environment as Env
import sys, os
from querySystem.matrixOp import *

info = Env.Info()
'''
wordsBagInfo = Env.WordsBagInfo(ignore=True)
info = Env.Info(wordsBagInfo=wordsBagInfo)
'''

env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
database = env_obj.Database
wordsBag = env_obj.WordsBag

if __name__ == "__main__":
    N = int(input("Nombre de documents : "))
    print("Création de la matrice termes-documents sur les "+str(N)+" premiers films")
    A, V, table = createTFMatrixV3(N, "MoviesFrequence.txt", mute = False)
    print(A.toarray())
    print(V.toarray())
    print(table)
    print(wordsBag.getIds("Bonjour"))
    Q = createQueryVect(wordsBag, input("Recherche : "))
    print(Q)
    imax, maxsco = getMostRelevantDoc(A, V, Q, mute = False)
    print("Score max : "+str(maxsco)+"\nDocument : "+str(table[imax]))

#%%
