import sys
import json
import os

import re
from string import punctuation
from time import perf_counter
from pathlib import Path

from dataManagement.Language import Language

class MovieFreq2:
    def __init__(self,id, list_freq):
        self.id = id
        self._listFreq = list_freq 
        #[(id_mot, freq)]
    
    def iterator(self):
        return self._Iterator(self._listFreq)

    class _Iterator:
        def __init__(self, list_freq):
            self._listFreq = list_freq
            self._index = 0


        def hasNext(self):
            return self._index < len(self._listFreq)

        def getNext(self):
            if self._index >= len(self._listFreq):
                return None
            
            tmp = self._listFreq[self._index]
            self._index+=1
            
            return tmp


class MovieFreq:
    def __init__(self,filename,id):
        self.filename=filename
        self.id = id
        #self._listFreq = list_freq 
    
    def iterator(self):
        return self._Iterator(self.filename,self.id)

    class _Iterator:
        def __init__(self,filename,id):
            self.filename=filename
            self.id=id
            self.file=open(self.filename,"r")
            self.pos=0


        def hasNext(self):
            self.file.seek(self.pos)#retourne jusqu'au dernier film visité
            cpt=0
            left_lines = file.readlines()
            if len(left_lines)==0:#vérifie si le fichier est vide
                return False
            for line in left_lines:#parcours les lignes du fichier
                if(cpt==1):#si il y a un autre films dans la liste
                    return True
                if(line=='\n'):
                    cpt+=1
                    continue

        def getNext(self):
            if self.hasNext==False:#vérifie si il y a bien encore un film dans la liste
                self.file.close()
                return None
            else:
                right_to_return=False
                cpt=0
                self.file.seek(self.pos,os.SEEK_SET)
                print("pos :",self.pos)
                left_lines = (self.file).readlines()
                for line in left_lines:#parcours les lignes du fichier
                    cpt+=1
                    print("Line:",line)
                    if(right_to_return==True):
                        res=self.pos+cpt
                        self.pos=res
                        return line
                    if(line=='\n'):
                        right_to_return=True
                        continue
                return None


class Frequency:
    def __init__(self, database, wordsBag, filename):
        self._database = database
        self._wordsBag = wordsBag
        self._filename = filename
    
    def _word_frequency(self, movie):
        ''' pour chaque résume de film ecrire le nombre d'occurence
        des mots
        ARGUMENTS :
            id_film (int) : 
        SORTIE : ecrit dans le fichier MoviesFrequence.txt de la forme:
        id_film
        id_mot nbr_mot
        id_mot nbr_mot
        
        id_film2
        id_mot nbr_mot
        id_mot nbr_mot
        '''
        bananasplit = self._wordsBag.getIds(movie.summary)
        #print(bananasplit)
        dico = dict()
        for word, id in bananasplit:
            dico.setdefault(id, 0)
            dico[id] += 1
        #print(dico)

        file = open(self._filename, "a")
        file.write(movie.id+"\n")
        for w in dico:
            file.write(str(w)+" "+str(dico[w])+"\n")
        file.write("\n")

    def computeFrequency(self):     
        with open(self._filename, "w") as file:
            file.write("")
        
        #file = open(self._filename, "a")
        
        it = self._database.iterator()
        cpt = 0
        while it.hasNext():
            movie = it.getNext()
            print(movie.summary)
            cpt+=1
            self._word_frequency(movie)
            
            if cpt==3:
                break
    
    def iterator(self):
        return self._Iterator(self._filename)
    
    class _Iterator:
        def __init__(self, filename):
            self._filename = filename
            
        
        def hasNext(self):
            return None
        
        def getNext(self):
            return MovieFreq()
        
    def iterator2(self):
        return self._Iterator2(self._filename)
    
    class _Iterator2:
        def __init__(self, filename):
            self._file = open(filename, 'r')
            
            self._next = self._readMovieFreq()
            if self._next is None:
                self._hasNext = False
            else :
                self._hasNext = True
            
        
        def hasNext(self):
            return self._hasNext
        
        def _readMovieFreq(self):
            line = self._file.readline()
            if line is None:
                return None
                
            id_movie = int(line)
            
            list_freq = []
            #print("-----------------")
            while True:
                line = self._file.readline()
                #print("line=", line)
                if line is None:
                    return None
                if line == "\n":
                    break
                    
                tmp = line.split(" ")
                
                id_word = int(tmp[0])
                freq = int(tmp[1])
                #print("gdggd id_word, freq", id_word, freq)
                list_freq.append((id_word, freq))
                #print(list_freq)
            return id_movie, list_freq
                
        def getNext(self):
            
            
            tmp = self._next
            
            self._next = self._readMovieFreq()
            if self._next is None:
                self._hasNext = False
            
            id_movie, list_freq = tmp
            return MovieFreq2(id_movie, list_freq)
       

if __name__ == "__main__":
    pass

