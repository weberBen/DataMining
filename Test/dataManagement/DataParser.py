#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import logging
import json
import sys
import zipfile
from pathlib import Path

#%%

'''
    Manipulation de la base de données : 
        db = Database(dossier) où dossier est le chemin du dossier contenant toutes les fiches de film (numérotées de 0 à (n-1) où n est le nombre de fiches et suivant le format json {<wikiId> : ***, <titre> : ***, <dateSortie> : ***, <duree> : ***, <genre> : ***, <resume> : ***})
    Pour obtenir la fiche d'index i :
        fiche = db.getMovie(i)
        if fiche not None:
            print(fiche.toString()) #affichage de la fiche
            print(fiche.id, fiche.title, fiche.summary) #affichage de certaines informations
        else :
            print("Aucune fiche trouvée")
'''



#%%
class MovieData:
    def __init__(self, id, title, release_date, length, genre, summary):
        self.id = id
        self.title = title
        self.releaseDate = release_date
        self.length = length
        self.genre = genre
        self.summary = summary
    
    def toString(self):
        return '<Film : id= {0}, nom={1}, date_sortie={2}, genre={3}, resume={4}>'.format(self.wikiId, self.titre, self.dateSortie, self.genre, self.resume)
  
class Database:
    def __init__(self, zip_filename_movie_data):
        '''
        Création d'un object base de données
        
        ARGUMENTS :
            dossier_fiches_films (string) : chemin du dossier contenant les fiches des films au format json ({<wikiId> : ***, <titre> : ***, <dateSortie> : ***, <duree> : ***, <genre> : ***, <resume> : ***})
                Les résumés sont supposés nettoyés
        '''
        logging.info("starting database")
        
        if not os.path.exists(zip_filename_movie_data) or not os.path.isfile(zip_filename_movie_data):
            logging.warning("archive de la base de données introuvabale")
            sys.exit()
        
        self._zippedFolder = zipfile.ZipFile(zip_filename_movie_data, 'r')
        self._folderDataName = Path(self._zippedFolder.filename).stem
        self._index = 0
        logging.info("database started")
    
    def _getDataFilename(self, index):
        return os.path.join(self._folderDataName, "{0}.json".format(index))
    
    def _fileExists(self, filename):
        return (filename in self._zippedFolder.namelist())
    
    def getMovie(self, index):
        '''
        Obtention d'une fiche de film
        
        ARGUMENTS :
            index (int) : index de la fiche (de 0 à (n-1) où n est le nombre de fiches)
        '''
        
        if index<0:
            return None
        
        movie_data = None
        filename = self._getDataFilename(index)
        if not self._fileExists(filename):
            return None
        
        b_json_file = self._zippedFolder.read(filename)
        json_file = b_json_file.decode('utf8')
        
        data = json.loads(json_file)
        wiki_id, title, release_date, length, genre, summary = data["wikiId"], data["titre"], data["dateSortie"], data["duree"], data["genre"], data["resume"]
        movie_data = MovieData(wiki_id, title, release_date, length, genre, summary)
        
        return movie_data
    
    #-------------------------------------------
    #
    #-------------------------------------------
    
    def iterator(self):
        return self._Iterator(self)
    
    class _Iterator():
        def __init__(self, database):
            self._database = database
            self._index = 0
        
        def hasNext(self):
            return self._database._fileExists(self._database._getDataFilename(self._index))
        
        def getNext(self):
            data = self._database.getMovie(self._index)
            if data is None:
                return None
            self._index+=1
            
            return data
            
            


#%%

        