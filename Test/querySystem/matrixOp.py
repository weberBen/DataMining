#! usr/bin/env python3
# -*- coding: utf-8 -*-
# matrixOp.py
# Opérations matricielles utiles au projet
# - Création de la matrice termes-documents

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
from decimal import *
import matplotlib.pyplot as plt
        
#################################################
#--------------------CLASSES--------------------#
#################################################

class Response:
    def __init__(self):
        self.userQuery = None
        self.filteredQuery = None
        self.dataset = None
        self.results = None
        self.nbRes = None
        self.threshold = None


class Request:

    ### INITIALISATION ###

    def __init__(self, database, wordsBag, Frequency, matrix_folder):

        self._rootDirectory = matrix_folder
        self._database = database
        self._wordsBag = wordsBag
        self._Frequency = Frequency
        
        self._dataFilename = None
        self._matrix = None
        self._idf = None
        self._table = None

        self._svd = None
        self._nmf = None

    ### CREATION ###

    def _create(self, filename, number_movie, count_item):
        logging.info("creation of matrix under <<"+str(filename)+">>")
        self._matrix, self._idf, self._table = createTFMatrixV5(number_movie, self._Frequency, count_item)
            
        with open(filename, "wb" ) as file:
            pickle.dump([self._matrix, self._idf, self._table], file)
        

    def create(self, matrix_name, erease=False, number_movies=None, count_item = 100):
        filename = os.path.join(self._rootDirectory, matrix_name)
        
        if os.path.exists(filename) and os.path.isfile(filename):
            if erease :
                logging.info("overwriting file <<"+str(filename)+">>")
                self._create(filename, number_movies, count_item)
            else:
                msg = "error during creation of matrix : cannot overwrite file <<"+str(filename)+">>"
                logging.warning(msg)
                raise IOError(msg).with_traceback(sys.exc_info()[2])
        else :
            self._create(filename, number_movies, count_item)
    

    ### CHARGEMENT ###

    def _load(self, filename, k):
        logging.info("loading matrix from <<"+str(filename)+">>")
        with open(filename, "rb" ) as file:
            tmp = pickle.load(file)
        self._matrix, self._idf, self._table = tmp[0], tmp[1], tmp[2]
        
        tmp = self._normalizetfidf()
        U, S, Vt = scs.linalg.svds(tmp, k = k, which = 'LM')
        self._svd = self._normalizesvd(U, S, Vt)
        self._dataFilename = filename
    

    def load(self, matrix_name, k = 400):
        filename = os.path.join(self._rootDirectory, matrix_name)
        
        if not os.path.exists(filename) or not os.path.isfile(filename):
            msg = "file <<"+str(filename)+">> does not exists"
            logging.error(msg)
            raise IOError(msg).with_traceback(sys.exc_info()[2])
        else:
            self._load(filename, k)
    

    ### NORMALISATION DE LA MATRICE & SVD ###

    def _normalizetfidf(self):
        diagidf = scs.diags(self._idf.tocsc().T.A, [0]).tocsc()
        return diagidf@self._matrix


    def _normalizesvd(self, u, s, vt):
        srt = np.array(list(zip(s, range(s.size))))
        srt = srt[srt[:,0].argsort()[::-1]]
        sig, prm = srt[:,0], np.array(srt[:,1], dtype = np.int)
        u, vt = u[:, prm], vt[prm, :]
        return scs.csc_matrix(u), scs.diags(s, 0).tocsc(), scs.csc_matrix(vt)


    def renewsvd(self, k = 400):
        if self._matrix is None or self._idf is None:
            logging.error("matrix or idf vector not initialized")
            exit()

        tmp = self._normalizetfidf()
        U, S, Vt = scs.linalg.svds(tmp, k = k, which = 'LM')
        self._svd = self._normalizesvd(U, S, Vt)


    ### NMF ###

    def _nmf(self, k = 100, maxiter = 1000):
        m, n = self._matrix.shape
        W = np.random.rand(m, n)
        H = np.zeros((m, n))
        cpt = 0
        while cpt < maxiter:
            W = W/scs.linalg.norm(W)
            Wold = W
            for j in range(n):
                H[:,j] = scs.linalg.lsqr(W, self._matrix[:,j])
            for i in range(m):
                tmp = scs.linalg.lsqr(H.T, self._matrix[i,:].T)
                W[i,:] = tmp.T
            if np.allclose(Wold, W):
                break
            cpt += 1
        return W, H

    ### RECHERCHE ###

    def search(self, txt, max_nbRes = 1, threshold = 0):
        if self._matrix is None or self._idf is None or self._table is None:
            logging.error("elements for search has not been initialized")
            return None
        
        response = Response()
        response.nbRes = max_nbRes
        response.userQuery = txt
        response.threshold = threshold
        response.dataset = self._dataFilename
        
        Q = createQueryVect(self._wordsBag, txt, response = response)
        res = getMostRelevantDocs(self._matrix, self._idf, Q, max_nbRes, threshold)
        output = []
        for e in res:
            if e[0] is None:
                continue
            movie_id = self._table[e[0]]
            score = e[1]
            output.append((movie_id, score))
            
            logging.debug("Score : "+str(score)+"\nMovieID : "+str(movie_id))
        
        response.results = output
        
        return response


    def searchSVD(self, txt, max_nbRes = 1, threshold = 0):
        if self._svd is None or self._table is None:
            logging.error("elements for search has not been initialized")
            return None
        
        response = Response()
        response.nbRes = max_nbRes
        response.userQuery = txt
        response.threshold = threshold
        response.dataset = self._dataFilename
        
        Q = createQueryVect(self._wordsBag, txt, response = response)
        res = getMostRelevantDocsSVD(self._svd, Q, max_nbRes, threshold)
        output = []
        for e in res:
            if e[0] is None:
                continue
            movie_id = self._table[e[0]]
            score = e[1]
            output.append((movie_id, score))
            
            logging.debug("Score : "+str(score)+"\nMovieID : "+str(movie_id))
        
        response.results = output
        
        return response


##################################################################
#--------------------CREATION MATRICE/VECTEUR--------------------#
##################################################################

def createTFMatrixV5(N, Freq, count_item = 100, mute = True):
    """
    int * bool -> CSC | None
    Retourne la matrice termes-documents TF dont
    les coefficients sont les fréquences de chaque mot
    dans les documents
    """
    def varsizecheck(data, row, col, M, V):
        logging.debug("createMatrixV5 - Tailles des var intermédiaires")
        logging.debug("sizeof(data) : "+str(sys.getsizeof(data)))
        logging.debug("sizeof(row) : "+str(sys.getsizeof(row)))
        logging.debug("sizeof(col) : "+str(sys.getsizeof(col)))
        logging.debug("createTFMatrixV5 - Taille CSC : "+str(M.data.nbytes+M.row.nbytes+M.col.nbytes)+" bytes")
        logging.debug("createTFMatrixV5 - Taille Vecteur IDF : "+str(sys.getsizeof(V))+" bytes")

    data, row, col = [], [], []
    table = array.array('i')
    i = 0
    headIndex, tailIndex, subTotal = 0, 0, 0
    start = perf_counter()
    F = Freq
    it = F.iterator2()
    cpt = 1
    getcontext().prec = 16
    while (N is None or i < N) and it.hasNext():
        m = it.getNext()
        
        if cpt%count_item==0:
            logging.info("{0} éléments ont été parcourus depuis le début ({1})".format(cpt, datetime.datetime.now()))
            
        cpt += 1
        table.append(m.id)
        itt = m.iterator()
        subTotal = 0
        while itt.hasNext():
            wid,wct = itt.getNext()
            data.append(wct)
            row.append(wid)
            col.append(i)
            subTotal += wct
        while headIndex < tailIndex:
            data[headIndex] = float(data[headIndex])/subTotal
            headIndex += 1
        headIndex += 1
        i += 1

    logging.info("creation of the matrix")
    M = scs.coo_matrix((data, (row, col)), dtype = float)
    m,n = M.shape
    M = M.tocsc()
    print("la matrice est de taille :",n,m)
    V = array.array('f')
    for i in tqdm(range(m)):
        V.append(np.log((n+1)/(M.getrow(i).count_nonzero()+1)))
        
    logging.info("creation of the idf vector")
    V = scs.coo_matrix((V, (range(len(V)), [0]*len(V))), dtype = float).tocsc()
    end = perf_counter()
    if not mute:
        varsizecheck(data, row, col, M, V)
        logging.debug("createTFMatrixV5 - Temps pris : "+str(end-start)+"s")
    return M, V, table


def createQueryVect(wordsbag, sentence, mute = True, response = None):
    """
    string * bool -> CSC | None
    """
    start = perf_counter()
    tmp = wordsbag.getIds(sentence)
    indices = [k[-1] for k in tmp]
    logging.debug(tmp)
    if len(indices) == 0:
        return None
    data = [1]*len(indices)
    indptr = [0, len(indices)]
    Q = scs.csc_matrix((data, indices, indptr), dtype = int)
    end = perf_counter()
    if not mute:
        logging.debug("createQueryVect - Temps pris : "+str(end-start)+"s")
    
    if response is not None:
        response.filteredQuery = tmp
    
    return Q


####################################################
#--------------------NORMES COS--------------------#
####################################################

def cosNorm(Q, C):
    """
    CSC * CSC -> float
    """
    return Q.multiply(C).sum()/(scs.linalg.norm(Q)*scs.linalg.norm(C))


def cosNormSVD(QUk, Hkj):
    """
    CSC * CSC -> float
    """
    # Q ligne (151206,1)
    # Uk (6,151206)
    # Uk.T*q.T = (qUk).T
    resn = QUk.multiply(Hkj).sum()
    resd = (scs.linalg.norm(QUk)*scs.linalg.norm(Hkj))
    return resn/resd


########################################################
#--------------------SEARCH RESULTS--------------------#
########################################################

def getMostRelevantDocs(M, V, Q, max_nbRes = 1, threshold = 0, mute = True):
    """
    CSC * CSC * CSC -> list[int*float]
    """
    if Q is None:
        logging.info("Requête rejetée")
        return [(None, 0)]
    ql = Q.shape[0]
    m, n = M.shape
    lst_top = [(None,0.0)]*max_nbRes
    #lst_imax = [None]*nbRes
    start = perf_counter()
    if ql < m:
        Q.resize(V.shape)
    else:
        Q = Q[:m]
    i = 0
    #while i < n:
    Q = Q.multiply(V)
    for i in tqdm(range(n),desc = 'recherche en cours'):
        scoi = cosNorm(Q, M[:,i])
        lst_sco = [e[-1] for e in lst_top]
        minil = min(lst_sco)
        if scoi is not None and scoi > minil:
            try:
                lst_top[lst_sco.index(minil)] = (i,scoi)
            except ValueError:
                logging.debug("ValueError")
                logging.debug("minil = "+str(minil))
                logging.debug("lst_top = "+str(lst_top))
        #i += 1 
    end = perf_counter()
    if not mute:
        logging.debug("getMostRelevantDocs - Temps pris : "+str(end-start)+"s")
        
    lst_top = sorted(lst_top, key = lambda x:x[-1], reverse = True)
    
    output = []
    for e in lst_top:
        scoi = e[-1]
        
        if len(output)>max_nbRes:
            break
        
        if scoi > threshold :
            if e[0] is not None:
                output.append(e)
    
    return output


def getMostRelevantDocsSVD(svd, Q, max_nbRes = 1, threshold = 0, mute = True):
    """
    [CSC * CSC] * CSC -> list[int*float]
    """
    if Q is None:
        logging.info("Requête rejetée")
        return [(None, 0)]
    ql = Q.shape[0]
    uk, sk, vk = svd
    hk = sk@vk
    m, n = uk.shape[0], hk.shape[-1]
    lst_top = [(None,0.0)]*max_nbRes
    #lst_imax = [None]*nbRes
    start = perf_counter()
    if ql < m:
        Q.resize((m,1))
    else:
        Q = Q[:m]
    i = 0
    #while i < n:
    Q = uk.transpose().multiply(Q.transpose())
    for i in tqdm(range(n),desc = 'recherche en cours'):
        scoi = cosNorm(Q, hk[:,i])
        lst_sco = [e[-1] for e in lst_top]
        minil = min(lst_sco)
        if scoi is not None and scoi > minil:
            try:
                lst_top[lst_sco.index(minil)] = (i,scoi)
            except ValueError:
                logging.debug("ValueError")
                logging.debug("minil = "+str(minil))
                logging.debug("lst_top = "+str(lst_top))
        #i += 1 
    end = perf_counter()
    if not mute:
        logging.debug("getMostRelevantDocsSVD - Temps pris : "+str(end-start)+"s")
        
    lst_top = sorted(lst_top, key = lambda x:x[-1], reverse = True)
    
    output = []
    for e in lst_top:
        scoi = e[-1]
        
        if len(output)>max_nbRes:
            break
        
        if scoi > threshold :
            if e[0] is not None:
                output.append(e)
    
    return output


#################################################
#--------------------VISUALS--------------------#
#################################################

def plot_coo_matrix(m):
    if not isinstance(m, scs.coo_matrix):
        m = scs.coo_matrix(m)
    fig = plt.figure()
    ax = fig.add_subplot(111, facecolor='black')
    ax.plot(m.col, m.row, 's', color='white', ms=1)
    ax.set_xlim(0, m.shape[1])
    ax.set_ylim(0, m.shape[0])
    ax.set_aspect('equal')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.invert_yaxis()
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    return ax


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
    A, V, table = createTFMatrixV5(N, "../MoviesFrequence.txt", mute = False)
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