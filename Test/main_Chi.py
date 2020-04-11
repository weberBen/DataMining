#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#%%
import environment as Env
import sys, os
from querySystem.matrixOp import *
import scipy.sparse as scs
import matplotlib.pyplot as plt
import numpy as np

info = Env.Info()
'''
wordsBagInfo = Env.WordsBagInfo(ignore=True) 
info = Env.Info(wordsBagInfo=wordsBagInfo)
'''

env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
database = env_obj.Database
wordsBag = env_obj.WordsBag
Freq = env_obj.Frequency

if __name__ == "__main__":
    #N = int(input("Nombre de documents : "))
    N = 10
    matrix = "matrix_"+"all"+"_but_for_real"+"_for_real_now"
    
    r = Request(database, wordsBag, Freq, env_obj.getMatrixFolder())
    #r.create(matrix, erease=True, number_movies=50, count_item=1000)
    rg = int(input("Rang de la SVD : "))
    r.load(matrix, k = rg)

    nbRes = int(input("Nombre de résultats : "))
    while True:
        raw = input("Recherche : ")
        if raw == "quit":
            break
        print("")
        movie = r.searchSVD(raw, nbRes)

        if raw == "reloadsvd":
            rg = int(input("Rang de la SVD : "))
            r.renewsvd(rg)
            print("")
        #if movie is not []:
        #    print(movie.title)
        
    '''
    N = int(input("Nombre de documents : "))
    print("Création de la matrice termes-documents sur les "+str(N)+" premiers films")
    A, V, table = createTFMatrixV4(N, Freq, mute = False)
    print(A.toarray())
    print(A.shape)
    print(V.toarray())
    print(V.shape)
    if len(table) < 50:
        print(table)
    #print(wordsBag.getIds("Bonjour"))
    while 1:
        Q = createQueryVect(wordsBag, input("Recherche : "))
        print(Q)
        imax, maxsco = getMostRelevantDoc(A, V, Q, mute = False)
        if imax is not None:
            print("Score max : "+str(maxsco)+"\nMovieID : "+str(table[imax]))
            print("Titre du film :"+database.getMovie(table[imax]).title)
        else:
            print("Rien trouvé")
    '''
#%%
