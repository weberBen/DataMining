#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#%%
import environment as Env
import sys, os

from querySystem.matrixOp import *
from querySystem.kmoy import *

import scipy.sparse as scs
import numpy as np
from random import randint

#info = Env.Info()
'''
wordsBagInfo = Env.WordsBagInfo(ignore=True) 
info = Env.Info(wordsBagInfo=wordsBagInfo)
'''
'''
env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
database = env_obj.Database
wordsBag = env_obj.WordsBag
Freq = env_obj.Frequency
'''

if __name__ == "__main__":
    m, n = 10, 5
    A = np.zeros((m, n))

    nrand = randint(10, 30)
    for i in range(nrand):
        pos = randint(0, m-1), randint(0, n-1)
        A[pos] = randint(1,10)

    cl = Clusterer(A)
    print("Matrice :\n", cl._matrix)

    cl._cookiecutter(2, n)
    print("Init clusters :\n", cl._clusters)

    cl._centroids = cl._computcentroids(cl._clusters)
    print("Init centroids :\n", cl._centroids)

    print("Score cluster 0 :\n", cl._tightness(cl._clusters[0], cl._centroids[0]))

    print("Score général :\n", cl._gencoherence(cl._clusters, cl._centroids))

    print("Nouv. clusters :\n", cl._updateclusters(cl._centroids))

    cl = Clusterer(A)
    print("Full k-moyennes :\n", cl.kmeans(2))