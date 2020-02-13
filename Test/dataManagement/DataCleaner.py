#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import ast
import logging
import os
import json
import modules.unwiki as unwiki

#%%__init__

'''
    Pour nettoyer la base de données (regroupper dans un seul fichier propre à chaque film les métadonnées et les résumés) et normaliser le texte des résumés appeler la fonction
    <clean> prennant en arguments : 
        movies_table_filename (string) : chemin du fichier contenant les informations des films - fichier CSV (avec comme séparateur la tabulation) associant l'indentifiant wikipédia du film et ses informations
        summaries_filename (string) : chemin du fichier contenant tous les résumes au format <identifiant wikipedia>[espace\tabulation]<texte du résumé>
        output_folder (string) : chemin vers le dossier où seront écrites les fiches des films
    
    Pour n films dans la base de données originelle, les fiches en sorties sont numérotées de 0 à n-1 dans l'ordre de lecture.
    Une fiche a comme format 
'''




#%%
class Movie:
  def __init__(self, name, release_date, length, language, countries, genre, _id=-1):
    self.name = name
    self.releaseDate = release_date
    self.length = length
    self.language = language
    self.countries = countries
    self.genre = genre
    self.id = _id
    
  def toString(self):
      return '<Film : nom={0}, date_sortie={1}, genre={2}>'.format(self.name,self.releaseDate, self.genre)


def readDataTable(filename):
    ''' lecture du fichier CSV (avec comme séparateur la tabulation) contenant les informations des films 
    dont le format est spécifié dans le Readme de la base de données originelle 
    
    ARGUMENTS :
        filename (string) : chemin du fichier contenant les informations sur les films
    SORTIE :
        dictionnaire associant l'indentifiant wikipedia avec ses données (sans le résumé)
        
    '''
    table = {}
    
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        
        for row in csv_reader:
            wiki_id, freebase_id, name, release_date, revenue, length, language, countries, genre = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]
            genre_dico = ast.literal_eval(genre)
            table[wiki_id] = Movie(name, release_date, length, language, countries, genreToList(genre_dico))
            
        return table
    
#%%
def readSummary(summary_line):
    '''
    chaque résumé suit le format suivant <identifiant wikipedia>[espace\tabulation]<texte du résumé>
    
    ARGUMENTS :
        ligne_resume (string) : string représentant la ligne du fichier des résumes au format spécifie ci-dessus
    SORTIE :
        l'identifiant (string), résumé du film (string)
    '''
    _id = ""
    pos = 0
    
    #lecture de l'identifiant wikipedia
    for c in summary_line:
        if not c.isalnum():
            break
        _id+=c
        pos+=1
    
    #suppression des caractère non alphabétique avant le début du texte
    for c in summary_line[pos:]:
        if c.isalpha() :
            break
        pos+=1
    
    return _id, summary_line[pos:]


class Summary:
    def __init__(self, summary_line):
        tmp = readSummary(summary_line)
        self.id = tmp[0]
        self.data = tmp[1]


def genreToList(genre_dico):
    '''
    Les genres des films se présentent sous la forme d'un dictionnaire que l'on converti en simple liste
    
     ARGUMENTS :
        genre_dico (dictionnary) : dictionnaire dont les valeurs sont les genres du film
    SORTIE :
        liste de string représentant le genre du film
    '''
    L = []
    for key, value in genre_dico.items():
        L.append(value)
        
    return L

def cleanSummary(summary):
    '''
    Suppression des marqueurs wikipédia des résumé
    
    ARGUMENTS :
        resume (string) : résumé du film au format txt
    SORTIE :
        string nettoyé du résumé du film
    '''
    unwiki_str = unwiki.loads(summary)
    unwiki_str = unwiki_str.lstrip() #suppression des espaces avant le début du texte
    
    return unwiki_str

    
def cleanSummaries(summaries_filename, movies_table, output_folder):
    '''
    Ecrit dans un fichier propre à chaque film les informations de ce dernier ainsi que son résumé. Les fiches sont numérotées dans l'ordre de lecture en débutant à 0
    
    ARGUMENTS :
        fichier_resumes (string) : chemin du fichier contenant tous les résumes au format <identifiant wikipedia>[espace\tabulation]<texte du résumé>
        table_films (dictionnary) : dictionnaire associant l'indentifiant wikipédia du film et ses informations 
        dossier_de_sortie (string) : chemin vers le dossier où seront écrites les fiches des films
    SORTIE :
        None
    '''
    
    cpt = 0
    with open(summaries_filename, 'r') as fichier:
        for line in fichier:
            
            res = Summary(line)
            movie_id = res.id        
            if not movie_id in movies_table:
                logging.warning("Le film \""+movie_id+"\" n'est pas dans la table de référencement")
                continue
            
            film_data = movies_table[movie_id]
            
            data = {}
            data["wikiId"] = movie_id
            data["titre"] = film_data.name
            data["dateSortie"] = film_data.releaseDate
            data["duree"] = film_data.length
            data["genre"] = film_data.genre
            data["resume"] = cleanSummary(res.data)
            
            
            path_ = os.path.join(output_folder, "{0}.json".format(cpt))
            with open(path_, 'w') as outfile:
                json.dump(data, outfile)
            
            
            cpt+=1
            
            
#%%

def clean(movies_table_filename, summaries_filename, output_folder):
    '''
    Ecrit dans un fichier propre à chaque film les informations de ce dernier ainsi que son résumé. Les fiches sont numérotées dans l'ordre de lecture en débutant à 0
    
    ARGUMENTS :
        fichier_table_film (string) : chemin du fichier contenant les informations des films - fichier CSV (avec comme séparateur la tabulation) associant l'indentifiant wikipédia du film et ses informations
        fichier_resume (string) : chemin du fichier contenant tous les résumes au format <identifiant wikipedia>[espace\tabulation]<texte du résumé>
        dossier_de_sortie (string) : chemin vers le dossier où seront écrites les fiches des films
    SORTIE :
        None
    '''
    movies_table = readDataTable(movies_table_filename)
    cleanSummaries(summaries_filename, movies_table, output_folder)

#%%
