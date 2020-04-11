### DEPRECATED ###

###############################################
#--------------------TESTS--------------------#
###############################################

def testW():
    A  = np.array([1, 2, 3, 9, 1, 4])
    indptr = np.array([0, 2, 4, 4, 6])
    indices = np.array([0, 1, 1, 6, 2, 7])
    print(scs.csr_matrix((A, indices, indptr), dtype = float).toarray())
    
####################################################
#--------------------DEPRECATED--------------------#
####################################################

def _DEPRECATEDcreateTFMatrixV1(path = "."):
    """
    DEPRECATED
    string -> CSR | None
    Retourne la matrice termes-documents TF dont
    les coefficients sont les fréquences de chaque mot
    dans les documents
    """
    print("Fonction obsolète, veuillez utiliser createMatrixV5")
    exit()
    
    freqFormat = "_freq.txt"
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

def _DEPRECATEDcreateTFMatrixV2(path = ".", mute = True):
    """
    string * bool -> CSC | None
    Retourne la matrice termes-documents TF dont
    les coefficients sont les fréquences de chaque mot
    dans les documents
    """
    print("Fonction obsolète, veuillez utiliser createMatrixV5")
    exit()

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

def _DEPRECATEDcreateTFMatrixV3(N, pathref = "MoviesFrequence.txt", mute = True):
    """
    DEPRECATED
    int * bool -> CSC | None
    Retourne la matrice termes-documents TF dont
    les coefficients sont les fréquences de chaque mot
    dans les documents
    """
    print("Fonction obsolète, veuillez utiliser createMatrixV5")
    exit()

    def varsizecheck(data, indices, indptr, M, V):
        print("createMatrixV3 - Tailles des var intermédiaires")
        print("sizeof(data) : "+str(sys.getsizeof(data)))
        print("sizeof(indices) : "+str(sys.getsizeof(indices)))
        print("sizeof(indptr) : "+str(sys.getsizeof(indptr)))
        print("createTFMatrixV3 - Taille CSC : "+str(M.data.nbytes+M.indices.nbytes+M.indptr.nbytes)+" bytes")
        print("createTFMatrixV3 - Taille Vecteur IDF : "+str(sys.getsizeof(V))+" bytes")

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

def _DEPRECATEDconvertToTFIDF(M):
    """
    DEPRECATED
    ndarray -> ndarray
    Convertit la matrice termes-documents TF en matrice
    TF-IDF
    """
    print("Fonction obsolète, veuillez utiliser createMatrixV5")
    exit()

    m, n = M.shape
    for i in range(m):
        ni = max(np.sum(M[i]>0),0.001)
        M[i] = M[i]*np.log(n/ni)
    return M

def _DEPRECATEDcreateTFMatrixV4(N, Freq, count_item = 100, mute = True):
    """
    DEPRECATED
    int * bool -> CSC | None
    Retourne la matrice termes-documents TF dont
    les coefficients sont les fréquences de chaque mot
    dans les documents
    """
    print("Fonction obsolète, veuillez utiliser createMatrixV5")
    exit()

    def varsizecheck(data, indices, indptr, M, V):
        logging.debug("createMatrixV4 - Tailles des var intermédiaires")
        logging.debug("sizeof(data) : "+str(sys.getsizeof(data)))
        logging.debug("sizeof(indices) : "+str(sys.getsizeof(indices)))
        logging.debug("sizeof(indptr) : "+str(sys.getsizeof(indptr)))
        logging.debug("createTFMatrixV4 - Taille CSC : "+str(M.data.nbytes+M.indices.nbytes+M.indptr.nbytes)+" bytes")
        logging.debug("createTFMatrixV4 - Taille Vecteur IDF : "+str(sys.getsizeof(V))+" bytes")

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
            logging.info("{0} éléments ont été parcourus depuis le début ({1})".format(cpt, datetime.datetime.now()))
            
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
    logging.info("la matrice est de taille : {},{}".format(n,m))
    V = array.array('f')
    for i in tqdm(range(m)):
        V.append(np.log((n+1)/(M.getrow(i).count_nonzero()+1)))
        
    logging.info("creation of the vector")
    V = scs.csc_matrix((V, range(len(V)), [0, len(V)]), dtype = float)
    end = perf_counter()
    if not mute:
        varsizecheck(data, indices, indptr, M, V)
        logging.debug("createTFMatrixV4 - Temps pris : "+str(end-start)+"s")
    return M, V, table