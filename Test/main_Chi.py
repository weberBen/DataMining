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
Freq = env_obj.Frequency

if __name__ == "__main__":
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
    
    N = int(input("Nombre de documents : "))
    print("Création de la matrice termes-documents sur les "+str(N)+" premiers films")
    r = Request(database, wordsBag, "matrix", N)
    while 1:
        movie = r.search(input("Recherche : "))
        if movie is not None:
            print(movie.title)
        

#%%
