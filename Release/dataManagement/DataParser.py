#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import logging
import json
import sys
import zipfile
from pathlib import Path
import sqlite3
import ast
import pickle
import codecs

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
        return '<Film : id= {0}, nom={1}, date_sortie={2}, genre={3}, resume={4}>'.format(self.id, self.title, self.releaseDate, self.genre, self.summary)

#%%

class MovieHandler:
    def __init__(self, filename):
        self._tableName = "Movie"
        
        self._dbFilename = filename
        self._conn = sqlite3.connect(filename)
        
        if not self._tableExists(self._conn, self._tableName):
            self._createDb(self._conn)
    
    def openNew(self):
        return MovieHandler(self._dbFilename)
    
    def _tableExists(self, conn, table_name):
        cursor = conn.cursor()
        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{0}'".format(table_name))

        #if the count is 1, then table exists
        if cursor.fetchone()[0]==1 : 
        	    return True
        
        return False
        
    def deleteAll(self):
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM "+self._tableName)
        self._conn.commit()
    
    def _createDb(self, conn):
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE "+self._tableName+" (id integer, title text, releaseDate text, lenght text, genre text, summary blob)")
        conn.commit()
    
        
    def _addWithoutCommit(self, movieData):
        if movieData is None :
            logging.warning("Trying to add NoneType to sqlite")
            return None
        cursor = self._conn.cursor()
        try :
            query = "INSERT INTO "+self._tableName+' VALUES ({0}, "{1}", "{2}", "{3}", "{4}", "{5}")'.format(movieData.id, self._encode(movieData.title), self._encode(movieData.releaseDate), self._encode(movieData.length), self._encode(movieData.genre), self._encode(movieData.summary))
        except sqlite3.OperationalError as e:
            logging.warning(query)
            raise sqlite3.OperationalError(e)
        
        cursor.execute(query)
        
    def add(self, movieData):
        
        if not type(movieData)==list:
            movieData = [movieData]
        
        for movie in movieData:
            self._addWithoutCommit(movie)
        
        self._conn.commit()
    
    def _encode(self, obj):
        txt =  codecs.encode(pickle.dumps(obj), "base64").decode()
        txt = txt.__repr__()
        
        return txt
    
    def _decode(self, txt):
        txt = ast.literal_eval(txt)
        txt = pickle.loads(codecs.decode(txt.encode(), "base64"))
        
        return txt
        
    def _rowToMovie(self, row):
        id, title, release_date, length, genre, summary = row[0], self._decode(row[1]), self._decode(row[2]), self._decode(row[3]), self._decode(row[4]), self._decode(row[5]) 
        output = MovieData(id, title, release_date, length, genre, summary)
        
        return output
    
    def getMovie(self, movie_id):
        cursor = self._conn.cursor()
        cursor.execute(("SELECT * FROM "+self._tableName+" where id={0}").format(movie_id))
        rows = cursor.fetchall()
        
        output = None
        count = 0
        for row in rows:
            
            output = self._rowToMovie(row)
            
            count+=1
        
        if count==0:
            return None
        
        if count!=1:
            logging.debug("multiple declations of the same id in sqlite")
        
        return output
    
    def close(self):
        self._conn.close()
    
    def iterator(self):
        return self._Iterator(self)
    
    class _Iterator:
        def __init__(self, movieHandler):
            self._movieHandler = movieHandler
            self._cursor = movieHandler._conn.cursor()
            self._cursor.execute("SELECT * FROM "+movieHandler._tableName)
            
            self._next = self._getNext()
            if self._next is None:
                self._hasNext = False
            else:
                self._hasNext = True
        
        def hasNext(self):
            return self._hasNext
        
        def _getNext(self):
            return self._cursor.fetchone()
            
        def getNext(self):
            tmp = self._next
            self._next = self._getNext()
            
            if self._next is None:
                self._hasNext = False
            
            return self._movieHandler._rowToMovie(tmp)
    
        
#%%

class Database:
    def __init__(self, movies_data_filename, movie_handler=None):
        '''
        Création d'un object base de données
        
        ARGUMENTS :
            dossier_fiches_films (string) : chemin du dossier contenant les fiches des films au format json ({<wikiId> : ***, <titre> : ***, <dateSortie> : ***, <duree> : ***, <genre> : ***, <resume> : ***})
                Les résumés sont supposés nettoyés
        '''
        
        if movies_data_filename is None and movie_handler is None:
            msg = "archive de la base de données introuvabale"
            logging.warning(msg)
            raise EnvironmentError(msg).with_traceback(sys.exc_info()[2])
        
        if movie_handler is not None:
            self._movieHandler = movie_handler
        else:
            logging.info("starting database")
            self._movieHandler = MovieHandler(movies_data_filename)
            logging.info("database started")
    
    def openNew(self):
        return Database(movies_data_filename=None, movie_handler=self._movieHandler.openNew())
    
    def getMovie(self, index):
        '''
        Obtention d'une fiche de film
        
        ARGUMENTS :
            index (int) : index de la fiche (de 0 à (n-1) où n est le nombre de fiches)
        '''
        
        if type(index)!=int:
            logging.warning("Type of movie id must be integer")
            return None
        
        return self._movieHandler.getMovie(index)
    
    #-------------------------------------------
    #
    #-------------------------------------------
    
    def iterator(self):
        return self._movieHandler.iterator()
            
            


#%%

