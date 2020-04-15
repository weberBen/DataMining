#! usr/bin/env python3
# -*- coding: utf-8 -*-
# kmoy.py
# Clustering

### IMPORTS ###

from matrixOp import *

import sys
import os
import numpy as np
import scipy.sparse as scs

import array 
import glob
from pathlib import Path
from time import perf_counter
import logging
import pickle
import uuid
import datetime
from tqdm import tqdm, tnrange

###############################################
#--------------------CLASS--------------------#
###############################################

def Clusterer():
    def __init__(self, matrix):
        self._matrix = matrix
        self._clusters = None # représente les vecteurs des clusters selon leurs indices
        self._centroids = None

    def _cookiecutter(self, k = 2, n = 10):
        """
        Initialise self._clusters avec une partition aléatoire des documents

        Retourne aussi la partition calculée
        """
        # Mélange aléatoirement le np.arange(n)
        tmp = np.random.shuffle(np.arange(n))
        # JSP
        if k > 0 and k == 1:
            return tmp
        # Au lieu de piocher aléatoirement pour avoir k paquets, on peut simplement
        # couper à k-1 endroits le np.arange(n) mélangé juste avant
        cutidx = np.sort(np.random.choice(n, k-1, replace = False))
        """
        # Décalage sinon on ne récupère pas la tête : INUTILE EN FAIT
        if 0 not in cutidx and k != 2:
            cutidx = cutidx - cutidx[0]
        """

        # TODO : À TESTER, NORMALEMENT OK
        sets = []
        for i in range(k):
            if i == 0:
                sets.append(tmp[:cutidx[i]])
            if i == k-1:
                sets.append(tmp[cutidx[i-1]:])
            else:
                sets.append(tmp[cutidx[i-1]:cutidx[i]])
        self._clusters = np.array(sets)
        return self._clusters

        # exemples :
        # k = 2
        # k-1 = 1
        # cutidx = 5, longueur 1
        # seul indice de cutidx : 0
        # indices de sets : 0, 1
        # i = 0 : sets[0] = tmp[:5]
        # i = 1 : sets[1] = tmp[5:]
        # OK NORMALEMENT

        # k = 4
        # k-1 = 3
        # cutidx = 6,9,15, longueur 3
        # indices de cutidx : 0,1,2
        # indices de sets : 0,1,2,3
        # i = 0 : sets[0] = tmp[:6]
        # i = 1 : sets[1] = tmp[6:9]
        # i = 2 : sets[2] = tmp[9:15]
        # i = 3 : sets[3] = tmp[15:]


    def _tightness(self, cluster, centroid):
        """
        Cohérence d'un cluster
        Ch. 9, p. 102
        """
        tgs = 0.
        for i in cluster:
            tgs += np.linalg.norm(np.abs(self._matrix[:,i]-centroid))
        return tgs

    def _gencoherence(self, clusters, centroids):
        """
        Qualité du clustering
        Ch. 9, p. 102
        """
        if clusters.size != centroids.size:
            return None
        gtgs = 0.
        for cluster, centroid in zip(clusters, centroids):
            gtgs += self._tightness(cluster, centroid)
        return gtgs

    def _computcentroids(self, partition = self._clusters):
        """
        Calcul des centroïdes selon la partition

        Retourne une liste de vecteurs
        """
        centroids = []
        for ens in partition:
            centroids.append(np.mean(self._matrix[:,ens], axis = 1, dtype = np.float32))
        return np.array(centroids)

    def _updateclusters(self, centroids):
        """
        MàJ des clusters selon la proximité avec les centroides
        Pas de MàJ de self._clusters

        Retourne une nouvelle partition
        Méthode naïve bof : parcours linéaire un peu lent, en O(n*k), approx O(n2)
        
        Soluce 15/04 : Utiliser numpy et minimiser la distance pour chacun grâce à une matrice
        """
        _, n = self.matrix.shape
        i = 0

        clusters = []*centroids.size
        while i < n:
            tmp = centroids-self.matrix[:,i]
            clusters[np.unravel_index(tmp.argmin(), tmp.shape)].append(i)
            i += 1
        self.clusters = np.array(clusters)
        return self.clusters


    def kmeans(self, k = 2, tol = 1e-1):
        """
        Calcul des k clusters avec l'algorithme des k-moyennes
        """
        _, n = self.matrix.shape

        clusters = self._cookiecutter(k, n)
        while 1:
            centroids = self._computcentroids(clusters)
            clusters = self._updateclusters(centroids)
            # TODO : confusion new et old
            if np.abs(self._gencoherence(clusters, centroids), self._gencoherence(self._clusters, centroids)) < tol:
                break
            self._clusters = clusters
        self._clusters = clusters
        return clusters


    ### RIP PETIT ANGE PARTI TROP TOT ###

    def brouillon(self, k = 2, tol = 1e-1):
        """
        Beurk
        """
        m, n = self.matrix.shape
        
        clusters = []*k
        idx = [i for i in range(n)]

        tmp = n
        for j in range(k):
            jsize = np.random.randint(tmp//2)
            for x in range(jsize):
                x = np.random.randint(len(idx))
                clusters[j].append(idx.pop(x))
            tmp -= tmp
        
        nclusters = []*k
        while 1:
            pass
            
            if np.abs(qold-qact) < tol:
                break
        return nclusters
