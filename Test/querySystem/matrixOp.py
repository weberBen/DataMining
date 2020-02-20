#! usr/bin/env python3
# -*- coding: utf-8 -*-
# matrixOp.py
# Opérations matricielles utiles au projet
# - Création de la matrice termes-documents
# TODO :
# createMatrix
# addDocument

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
        
#%%

class Request:
    def __init__(self, database, wordsBag, Frequency, matrix_folder):
        
        self._rootDirectory = matrix_folder
        self._database = database
        self._wordsBag = wordsBag
        self._Frequency = Frequency
        
        self._matrix = None
        self._idf = None
        self._table = None
        
    def _create(self, filename, number_movie, count_item):
        logging.info("creation of matrix under <<"+str(filename)+">>")
        self._matrix, self._idf, self._table = createTFMatrixV4(number_movie, self._Frequency, count_item)
            
        with open(filename, "wb" ) as file:
            pickle.dump([self._matrix, self._idf, self._table], file)
        
    def create(self, matrix_name, erease=False, number_movies=None, count_item = 100):
        filename = os.path.join(self._rootDirectory, matrix_name)
        
        if os.path.exists(filename) and os.path.isfile(filename):
            if erease :
                logging.info("overwriting file <<"+str(filename)+">>")
                self._create(filename, number_movies, count_item)
            else:
                logging.warning("error during creation of matrix : cannot overwrite file <<"+str(filename)+">>")
                sys.exit()
        else :
            self._create(filename, number_movies, count_item)
    
    def _load(self, filename):
        logging.info("loading matrix from <<"+str(filename)+">>")
        with open(filename, "rb" ) as file:
            tmp = pickle.load(file)
        self._matrix, self._idf, self._table = tmp[0], tmp[1], tmp[2]
    
    def load(self, matrix_name):
        filename = os.path.join(self._rootDirectory, matrix_name)
        
        if not os.path.exists(filename) or not os.path.isfile(filename):
            logging.error("file <<"+str(filename)+">> does not exists")
            sys.exit()
        else:
            self._load(filename)
    
    def search(self, txt):
        
        if self._matrix is None or self._idf is None or self._table is None:
            logging.error("elements for search has not been initialized")
            return None
        
        Q = createQueryVect(self._wordsBag, txt)
        imax, maxsco = getMostRelevantDoc(self._matrix, self._idf, Q)
        if imax is not None:
            movie = self._database.getMovie(self._table[imax])
            logging.debug("Score max : "+str(maxsco)+"\nMovieID : "+str(self._table[imax]))
            logging.debug("Titre du film :"+movie.title)
            return movie
        else:
            logging.debug("Rien trouvé")
            return None
    
    



#%%

###############################################
#--------------------CLASS--------------------#
###############################################

class TDMvm:
    def __init__(self, N, Freq):
        self.mat, self.idf, self.table = createTFMatrixV4(N, Freq, mute = True)

    def toStr(self):
        logging.info("Matrice Termes-Documents (TF) :\n"+str(self.mat.toarray()))
        logging.info("Vecteur IDF :\n"+str(self.idf.toarray()))

###################################################
#--------------------FUNCTIONS--------------------#
###################################################

def addDocumentToMatrix(M, V, mat):
    pass


def createTFMatrixV4(N, Freq, count_item = 100, mute = True):
    """
    int * bool -> CSC | None
    Retourne la matrice termes-documents TF dont
    les coefficients sont les fréquences de chaque mot
    dans les documents
    """
    def varsizecheck(data, indices, indptr, M, V):
        logging.debug("createMatrixV2 - Tailles des var intermédiaires")
        logging.debug("sizeof(data) : "+str(sys.getsizeof(data)))
        logging.debug("sizeof(indices) : "+str(sys.getsizeof(indices)))
        logging.debug("sizeof(indptr) : "+str(sys.getsizeof(indptr)))
        logging.debug("createTFMatrixV2 - Taille CSC : "+str(M.data.nbytes+M.indices.nbytes+M.indptr.nbytes)+" bytes")
        logging.debug("createTFMatrixV2 - Taille Vecteur IDF : "+str(sys.getsizeof(V))+" bytes")

    #lst_dwc = glob.glob(path+freqFormat)
    data = []
    indices = []
    indptr = [0]
    table = array.array('i')
    headIndex = 0
    tailIndex = 0
    i = 0
    subTotal = 0
    start = perf_counter()
    F = Freq
    it = F.iterator2()
    cpt = 1
    
    while (N is None or i < N) and it.hasNext():
        m = it.getNext()
        
        if cpt%count_item==0:
            logging.info("{0} items has been browse since the begining ({1})".format(cpt, datetime.datetime.now()))
            
        cpt+=1
        
        table.append(m.id)
        itt = m.iterator()
        subTotal = 0
        while itt.hasNext():
            wid,wct = itt.getNext()
            data.append(wct)
            indices.append(wid)
            subTotal += wct
            tailIndex += 1
        indptr.append(tailIndex-headIndex+indptr[-1])
        while headIndex < tailIndex:
            data[headIndex] = float(data[headIndex])/subTotal
            headIndex += 1
        headIndex += 1
        i += 1
    
    logging.info("creation of the matrix")
    M = scs.csc_matrix((data, indices, indptr), dtype = float)
    m,n = M.shape
    i = 0
    V = array.array('f')
    while i < m:
        V.append(np.log(n/max(0.001, M.getrow(i).count_nonzero())))
        i += 1
    logging.info("creation of the vector")
    V = scs.csc_matrix((V, range(len(V)), [0, len(V)]), dtype = float)
    end = perf_counter()
    if not mute:
        varsizecheck(data, indices, indptr, M, V)
        logging.debug("createTFMatrixV2 - Temps pris : "+str(end-start)+"s")
    return M, V, table


def createQueryVect(wordsbag, sentence, mute = True):
    """
    string * bool -> CSC | None
    """
    start = perf_counter()
    indices = [k[-1] for k in wordsbag.getIds(sentence)]
    if len(indices) == 0:
        return None
    data = [1]*len(indices)
    indptr = [0, len(indices)]
    Q = scs.csc_matrix((data, indices, indptr), dtype = int)
    end = perf_counter()
    if not mute:
        logging.debug("createQueryVect - Temps pris : "+str(end-start)+"s")
    return Q


def cosNorm(Q, C):
    """
    CSC * CSC -> float
    """
    return Q.multiply(C).sum()/np.sqrt(Q.multiply(Q).sum()*C.multiply(C).sum())


def getMostRelevantDoc(M, V, Q, mute = True):
    """
    CSC * CSC * CSC -> int * float
    """
    if Q is None:
        logging.info("Requête rejetée")
        return None, 0
    ql = Q.shape[0]
    m, n = M.shape
    maxsco = 0.0
    imax = None
    i = 0
    start = perf_counter()
    if ql < m:
        Q.resize(V.shape)
    else:
        Q = Q[:m]
    while i < n:
        scoi = cosNorm(Q, M[:,i].multiply(V))
        if maxsco < scoi:
            maxsco = scoi
            imax = i
        i += 1
    end = perf_counter()
    if not mute:
        logging.debug("getMostRelevantDoc - Temps pris : "+str(end-start)+"s")
    return imax, maxsco


def testW():
    A  = np.array([1, 2, 3, 9, 1, 4])
    indptr = np.array([0, 2, 4, 4, 6])
    indices = np.array([0, 1, 1, 6, 2, 7])
    print(scs.csr_matrix((A, indices, indptr), dtype = float).toarray())

##############################################
#--------------------MAIN--------------------#
##############################################

def main(args = None):
    def usage():
        # Self-explanatory
        instr = """Usage : python3 matrixOperations.py"""
        print(instr)
    # Pour avoir une matrice plus lisible, ajouter .toarray() pour convertir
    # la matrice CSR en matrice normale
    #print(createTFMatrixV1().toarray())
    #print("")
    #print(os.getcwd())
    print("Création de la matrice termes-documents")
    N = int(input("Nombre de films à inclure : "))
    A, V, table = createTFMatrixV3(N, "../MoviesFrequence.txt", mute = False)
    print(A.toarray())
    print("Taille matrix complete : "+str(sys.getsizeof(A.toarray()))+" bytes")
    print(A.shape)
    print(V.toarray())
    print(V.shape)
    #print(table)
    #print(A.nonzero())
    s = input("Recherche : ")
    Q = createQueryVect(s, mute = False)
    print(Q.toarray())

if __name__ == '__main__':
    #main()
    pass

####################################################
#--------------------DEPRECATED--------------------#
####################################################

def DEPRECATEDcreateTFMatrixV1(path = "."):
    """
    DEPRECATED
    string -> CSR | None
    Retourne la matrice termes-documents TF dont
    les coefficients sont les fréquences de chaque mot
    dans les documents
    """
    print("Fonction obsolète, veuillez utiliser createMatrixV2")
    exit()
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

def DEPRECATEDcreateTFMatrixV2(path = ".", mute = True):
    """
    string * bool -> CSC | None
    Retourne la matrice termes-documents TF dont
    les coefficients sont les fréquences de chaque mot
    dans les documents
    """
    freqFormat = "/*_freq.txt"
    
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
        V.append(np.log(n/max(0.001, M.getrow(i).count_nonzero())))
        i += 1
    V = scs.csc_matrix((V, range(len(V)), [0, len(V)]), dtype = float)
    end = perf_counter()
    if not mute:
        varsizecheck(data, indices, indptr, M, V)
        print("createTFMatrixV2 - Temps pris : "+str(end-start)+"s")
    return M, V

def DEPRECATEDcreateTFMatrixV3(N, pathref = "MoviesFrequence.txt", mute = True):
    """
    DEPRECATED
    int * bool -> CSC | None
    Retourne la matrice termes-documents TF dont
    les coefficients sont les fréquences de chaque mot
    dans les documents
    """
    def varsizecheck(data, indices, indptr, M, V):
        print("createMatrixV2 - Tailles des var intermédiaires")
        print("sizeof(data) : "+str(sys.getsizeof(data)))
        print("sizeof(indices) : "+str(sys.getsizeof(indices)))
        print("sizeof(indptr) : "+str(sys.getsizeof(indptr)))
        print("createTFMatrixV2 - Taille CSC : "+str(M.data.nbytes+M.indices.nbytes+M.indptr.nbytes)+" bytes")
        print("createTFMatrixV2 - Taille Vecteur IDF : "+str(sys.getsizeof(V))+" bytes")

    #lst_dwc = glob.glob(path+freqFormat)
    data = []
    indices = []
    indptr = [0]
    table = array.array('i')
    headIndex = 0
    tailIndex = 0
    i = 0
    subTotal = 0
    start = perf_counter()
    F = SWF.Frequency(None, None, pathref)
    it = F.iterator2()
    while i < N and it.hasNext():
        m = it.getNext()
        table.append(m.id)
        itt = m.iterator()
        subTotal = 0
        while itt.hasNext():
            wid,wct = itt.getNext()
            data.append(wct)
            indices.append(wid)
            subTotal += wct
            tailIndex += 1
        indptr.append(tailIndex-headIndex+indptr[-1])
        while headIndex < tailIndex:
            data[headIndex] = float(data[headIndex])/subTotal
            headIndex += 1
        headIndex += 1
        i += 1
    M = scs.csc_matrix((data, indices, indptr), dtype = float)
    m,n = M.shape
    i = 0
    V = array.array('f')
    while i < m:
        V.append(np.log(n/max(0.001, M.getrow(i).count_nonzero())))
        i += 1
    V = scs.csc_matrix((V, range(len(V)), [0, len(V)]), dtype = float)
    end = perf_counter()
    if not mute:
        varsizecheck(data, indices, indptr, M, V)
        print("createTFMatrixV2 - Temps pris : "+str(end-start)+"s")
    return M, V, table

def DEPRECATEDconvertToTFIDF(M):
    """
    DEPRECATED
    ndarray -> ndarray
    Convertit la matrice termes-documents TF en matrice
    TF-IDF
    """
    print("Fonction obsolète, veuillez utiliser createMatrixV2")
    exit()
    m, n = M.shape
    for i in range(m):
        ni = max(np.sum(M[i]>0),0.001)
        M[i] = M[i]*np.log(n/ni)
    return M