#! usr/bin/env python3
# -*- coding: utf-8 -*-
# matrixOp.py
# Opérations matricielles utiles au projet
# - Création de la matrice termes-documents
# TODO :
# createMatrix
# addDocument

import sys
import numpy as np
import scipy.sparse as scs
import array 
import glob
import os
from math import log
from time import perf_counter

freqFormat = "/*_freq.txt"


class TDM_VM:
    def __init__(self, path):
        self.mat, self.idf = createTFMatrixV2(path)

    def toStr(self):
        print("Matrice Termes-Documents (TF) :\n",self.mat.toarray())
        print("Vecteur IDF :\n",self.idf.toarray())

def addDocumentToMatrix(M, V, mat):
    pass

def createTFMatrixV2(path = ".", mute = True):
    """
    string * bool -> CSC | None
    Retourne la matrice termes-documents TF dont
    les coefficients sont les fréquences de chaque mot
    dans les documents
    """
    def varsizecheck(data, indices, indptr, M, V):
        print("createMatrixV2 - Tailles des var intermédiaires")
        print("sizeof(data) : "+str(sys.getsizeof(data)))
        print("sizeof(indices) : "+str(sys.getsizeof(indices)))
        print("sizeof(indptr) : "+str(sys.getsizeof(indptr)))
        print("createTFMatrixV2 - Taille CSC : "+str(sys.getsizeof(M))+" bytes")
        print("createTFMatrixV2 - Taille Vecteur IDF : "+str(sys.getsizeof(V))+" bytes")

    lst_dwc = glob.glob(path+freqFormat)
    data = []
    indices = []
    indptr = [0]
    #totalWordCount = 0
    table = {}
    isLineEmpty = False
    headIndex = 0
    tailIndex = 0
    start = perf_counter()
    for filename in lst_dwc:
        isLineEmpty = False
        subTotal = 0
        try:
            file = open(filename, "r")
            for line in file.readlines():
                content = line.strip('\n').split(' ')
                if len(content) == 0:
                    isLineEmpty = True
                    continue
                wid, wct = int(content[0]), int(content[-1])
                table.setdefault(wid, len(table))

                data.append(wct)
                indices.append(table[wid])

                subTotal += wct
                tailIndex += 1
            file.close()
            if isLineEmpty:
                continue
            #totalWordCount += subTotal
            indptr.append(tailIndex-headIndex+indptr[-1])
            """
            for i in range(headIndex,tailIndex):
                data[i] = float(data[i])/subTotal
            headIndex = tailIndex
            """
            #i = headIndex
            while headIndex < tailIndex:
                data[headIndex] = float(data[headIndex])/subTotal
                headIndex += 1
            headIndex += 1
        except IOError:
            print("Erreur de lecture (IOError)")
            return None
    M = scs.csc_matrix((data, indices, indptr), dtype = float)
    m,n = M.shape
    i = 0
    V = array.array('f')
    while i < m:
        V.append(log(n/max(0.001, M.getrow(i).count_nonzero())))
        i += 1
    V = scs.csc_matrix((V, range(len(V)), [0, len(V)]), dtype = float)
    end = perf_counter()
    if not mute:
        varsizecheck(data, indices, indptr, M, V)
        print("createTFMatrixV2 - Temps pris : "+str(end-start)+"s")
    return M, V

def createQueryVect(string, mute = True):
    """
    string * bool -> CSC | None
    """
    start = perf_counter()
    indices = [k[-1] for k in wordsBag.getIds(string)]
    data = [1]*len(indices)
    indptr = [0, len(indices)]
    Q = scs.csc_matrix((data, indices, indptr), dtype = int)
    end = perf_counter()
    if not mute:
        print("createQueryVect - Temps pris : "+str(end-start)+"s")
    return Q

def cosNorm(Q, C):
    """
    CSC * CSC -> float
    """
    return Q.multiply(C).sum()/(np.sqrt(Q.multiply(Q).sum())*np.sqrt(C.multiply(C).sum()))

def getSimilarityCos(M, V, Q):
    """
    CSC * CSC * CSC -> list[float]
    """

def test():
    A  = np.array([1, 2, 3, 9, 1, 4])
    indptr = np.array([0, 2, 4, 4, 6])
    indices = np.array([0, 1, 1, 6, 2, 7])
    print(scs.csr_matrix((A, indices, indptr), dtype = float).toarray())

def main(args):
    def usage():
        # Self-explanatory
        instr = """Usage : python3 matrixOperations.py"""
        print(instr)
    # Pour avoir une matrice plus lisible, ajouter .toarray() pour convertir
    # la matrice CSR en matrice normale
    #print(createTFMatrixV1().toarray())
    print("")
    A, V = createTFMatrixV2(mute = False)
    print(A.toarray())
    print(V.toarray())
    print(A.nonzero())
    #test()

if __name__ == '__main__':
    args = sys.argv
    main(args)

####################################################
#--------------------DEPRECATED--------------------#
####################################################

def createTFMatrixV1(path = "."):
    """
    DEPRECATED
    string -> CSR | None
    Retourne la matrice termes-documents TF dont
    les coefficients sont les fréquences de chaque mot
    dans les documents
    """
    lst_dwc = glob.glob(path+freqFormat)
    data = []
    indices = []
    indptr = [0]
    totalWordCount = 0
    isLineEmpty = False
    start = perf_counter()
    for filename in lst_dwc:
        isLineEmpty = False
        try:
            file = open(filename, "r")
            for line in file.readlines():
                content = line.strip('\n').split(' ')
                if len(content) == 0:
                    isLineEmpty = True
                    continue
                wid, wct = int(content[0]), int(content[-1])
                indices = indices + [wid]*wct
                totalWordCount += wct 
            file.close()
            if isLineEmpty:
                continue
            indptr.append(totalWordCount)
        except IOError:
            print("Erreur de lecture (IOError)")
            return None
    data = [1]*indptr[-1]
    end = perf_counter()
    print("createMatrixV1 - Tailles des var intermédiaires")
    print("sizeof(data) : "+str(sys.getsizeof(data)))
    print("sizeof(indices) : "+str(sys.getsizeof(indices)))
    print("sizeof(indptr) : "+str(sys.getsizeof(indptr)))
    #print(totalWordCount)
    print("createTFMatrixV1 - Temps pris : "+str(end-start)+" s")
    M = scs.csr_matrix((data, indices, indptr), dtype = float)
    print("createTFMatrixV1 - Taille CSR : "+str(sys.getsizeof(M))+" bytes")
    return M

def convertToTFIDF(M):
    """
    DEPRECATED
    ndarray -> ndarray
    Convertit la matrice termes-documents TF en matrice
    TF-IDF
    """
    m, n = M.shape
    for i in range(m):
        ni = max(np.sum(M[i]>0),0.001)
        M[i] = M[i]*log(n/ni)
    return M