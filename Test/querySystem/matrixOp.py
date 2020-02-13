#! usr/bin/env python3
# -*- coding: utf-8 -*-
# matrixOp.py
# Opérations matricielles utiles au projet
# - Création de la matrice termes-documents
# TODO :
# createMatrix
# addDocument
# addWord
# getIDF

import sys
import numpy as np
import scipy.sparse as scs
import glob
import os
from math import log
from time import perf_counter

freqFormat = "/*_freq.txt"

def createTFMatrixV1(path = "."):
    """
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

def createTFMatrixV2(path = "."):
    """
    string -> CSR | None
    Retourne la matrice termes-documents TF dont
    les coefficients sont les fréquences de chaque mot
    dans les documents
    """
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
                # Ajout du mot et de son nombre d'occurence
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
            """for i in range(headIndex,tailIndex):
                data[i] = float(data[i])/subTotal
            headIndex = tailIndex
            """
            i = headIndex
            while i < tailIndex:
                data[i] = float(data[i])/subTotal
                i += 1
            headIndex = tailIndex
        except IOError:
            print("Erreur de lecture (IOError)")
            return None
    print("createMatrixV2 - Tailles des var intermédiaires")
    print("sizeof(data) : "+str(sys.getsizeof(data)))
    print("sizeof(indices) : "+str(sys.getsizeof(indices)))
    print("sizeof(indptr) : "+str(sys.getsizeof(indptr)))
    M = scs.csc_matrix((data, indices, indptr), dtype = float)
    print("createTFMatrixV2 - Taille CSC : "+str(sys.getsizeof(M))+" bytes")
    i = 0
    m,n = M.shape
    while i < m:
        idfi = log(n/max(0.001, M.getrow(i).count_nonzero()))
        M[i] *= idfi
        i += 1
    end = perf_counter()
    print("createTFMatrixV2 - Temps pris : "+str(end-start)+" s")
    return M

def getIDF():
    pass

def addDocument():
    pass

def addWord():
    pass

def convertToTFIDF(M):
    """
    TODO - DEPRECATED
    ndarray -> ndarray
    Convertit la matrice termes-documents TF en matrice
    TF-IDF
    """
    m, n = M.shape
    for i in range(m):
        ni = max(np.sum(M[i]>0),0.001)
        M[i] = M[i]*log(n/ni)
    return M

def usage():
    # Self-explanatory
    instr = """Usage : python3 matrixOperations.py"""
    print(instr)

def test():
    A  = np.array([1, 2, 3, 9, 1, 4])
    indptr = np.array([0, 2, 4, 4, 6])
    indices = np.array([0, 1, 1, 6, 2, 7])
    print(scs.csr_matrix((A, indices, indptr), dtype = float).toarray())

def main(args):
    # Pour avoir une matrice plus lisible, ajouter .toarray() pour convertir
    # la matrice CSR en matrice normale
    print(createTFMatrixV1().toarray())
    print("")
    A = createTFMatrixV2()
    print(A.toarray())
    print(A.nonzero())
    #test()

if __name__ == '__main__':
    args = sys.argv
    main(args)