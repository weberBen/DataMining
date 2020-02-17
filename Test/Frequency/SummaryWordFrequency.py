import sys
import json

import re
from string import punctuation
from time import perf_counter
from pathlib import Path

from dataManagement.Language import Language


class MovieFreq:
    def __init__(self, id, list_freq):
        self.id = id
        self._listFreq = list_freq 
    
    def iterator(self):
        return _Iterator()

    class _Iterator:
        def __init__(self, filename):
            self._filename = filename

        
        def hasNext(self):
            return None
        
        def getNext(self):
            return (id_word, freq)


class Frequency:
    def __init__(self, database, wordsBag):
        self._database = database
        self._wordsBag = wordsBag
        self._filename = "MoviesFrequence.txt"
    
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
       

if __name__ == "__main__":
    pass

