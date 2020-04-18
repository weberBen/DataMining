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
    print(cl._matrix)

    cl._cookiecutter(2, n)
    print(cl._clusters)

    cl._centroids = cl._computcentroids(cl._clusters)
    print(cl._centroids)

    print(cl._tightness(cl._clusters[0], cl._centroids[0]))

    print(cl._gencoherence(cl._clusters, cl._centroids))

    print(cl._updateclusters(cl._centroids))

    cl = Clusterer(A)
    print(cl.kmeans(2))