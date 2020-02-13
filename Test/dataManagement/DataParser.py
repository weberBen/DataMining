#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import logging
import json
import os

#%%

'''
    Manipulation de la base de données : 
        db = Database(dossier) où dossier est le chemin du dossier contenant toutes les fiches de film (numérotées de 0 à (n-1) où n est le nombre de fiches et suivant le format json {<wikiId> : ***, <titre> : ***, <dateSortie> : ***, <duree> : ***, <genre> : ***, <resume> : ***})
    Pour obtenir la fiche d'index i :
        fiche = db.getMovie(i)
        if fiche not None:
            print(fiche.toString()) #affichage de la fiche
            print(fiche.wikiId, fiche.title, fiche.summary) #affichage de certaines informations
        else :
            print("Aucune fiche trouvée")
'''



#%%
class MovieData:
    def __init__(self, wiki_id, title, release_date, length, genre, summary):
        self.wikiId = wiki_id
        self.title = title
        self.releaseDate = release_date
        self.length = length
        self.genre = genre
        self.summary = summary
    
    def toString(self):
        return '<Film : wikiId= {0}, nom={1}, date_sortie={2}, genre={3}, resume={4}>'.format(self.wikiId, self.titre, self.dateSortie, self.genre, self.resume)
  
class Database:
    def __init__(self, folder_movies_data):
        '''
        Création d'un object base de données
        
        ARGUMENTS :
            dossier_fiches_films (string) : chemin du dossier contenant les fiches des films au format json ({<wikiId> : ***, <titre> : ***, <dateSortie> : ***, <duree> : ***, <genre> : ***, <resume> : ***})
                Les résumés sont supposés nettoyés
        '''
        self.folderData = folder_movies_data
        self.index = 0
    
    def __getDataFilename__(self, index):
        return os.path.join(self.folderData, "{0}.json".format(index))
    
    def getMovie(self, index):
        '''
        Obtention d'une fiche de film
        
        ARGUMENTS :
            index (int) : index de la fiche (de 0 à (n-1) où n est le nombre de fiches)
        '''
        
        if index<0:
            return None
        
        movie_data = None
        filename = self.__getDataFilename__(index)
        if not os.path.exists(filename) :
            return None
        
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            wiki_id, title, release_date, length, genre, summary = data["wikiId"], data["titre"], data["dateSortie"], data["duree"], data["genre"], data["resume"]
            movie_data = MovieData(wiki_id, title, release_date, length, genre, summary)
        
        return movie_data
    
    #-------------------------------------------
    #
    #-------------------------------------------
    
    def iterator(self):
        return self.__Iterator__(self)
    
    class __Iterator__():
        def __init__(self, database):
            self._database = database
            self._index = 0
        
        def hasNext(self):
            return os.path.exists(self._database.__getDataFilename__(self._index))
        
        def getNext(self):
            data = self._database.getMovie(self._index)
            if data is None:
                return None
            self._index+=1
            
            return data
            
            


#%%

        