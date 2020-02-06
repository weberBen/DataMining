#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import ast
import logging
import os
import json
import unwiki

#%%__init__

'''
    Pour nettoyer la base de données (regroupper dans un seul fichier propre à chaque film les métadonnées et les résumés) et normaliser le texte des résumés appeler la fonction
    <nettoyerResumes> prennant en arguments : 
        fichier_table_film (string) : chemin du fichier contenant les informations des films - fichier CSV (avec comme séparateur la tabulation) associant l'indentifiant wikipédia du film et ses informations
        fichier_resume (string) : chemin du fichier contenant tous les résumes au format <identifiant wikipedia>[espace\tabulation]<texte du résumé>
        dossier_de_sortie (string) : chemin vers le dossier où seront écrites les fiches des films
    
    Pour n films dans la base de données originelle, les fiches en sorties sont numérotées de 0 à n-1 dans l'ordre de lecture.
    Une fiche a comme format 
'''




#%%
class Film:
  def __init__(self, nom, date_sortie, duree, langue, pays, genre, _id=-1):
    self.nom = nom
    self.dateSortie = date_sortie
    self.duree = duree
    self.langue = langue
    self.pays = pays
    self.genre = genre
    self.id = _id
    
  def toString(self):
      return '<Film : nom={0}, date_sortie={1}, genre={2}>'.format(self.nom,self.dateSortie, self.genre)


def lireTableDonnee(filename):
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
            wiki_id, freebase_id, nom, date_sortie, revenu, duree, langue, pays, genre = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]
            genre_dico = ast.literal_eval(genre)
            table[wiki_id] = Film(nom, date_sortie, duree, langue, pays, listeGenre(genre_dico))
            
        return table
    
#%%
def lireResume(ligne_resume):
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
    for c in ligne_resume:
        if not c.isalnum():
            break
        _id+=c
        pos+=1
    
    #suppression des caractère non alphabétique avant le début du texte
    for c in ligne_resume[pos:]:
        if c.isalpha() :
            break
        pos+=1
    
    return _id, ligne_resume[pos:]


class Resume:
    def __init__(self, ligne_resume):
        tmp = lireResume(ligne_resume)
        self.id = tmp[0]
        self.data = tmp[1]


def listeGenre(genre_dico):
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

def nettoyerResume(resume):
    '''
    Suppression des marqueurs wikipédia des résumé
    
    ARGUMENTS :
        resume (string) : résumé du film au format txt
    SORTIE :
        string nettoyé du résumé du film
    '''
    unwiki_str = unwiki.loads(resume)
    unwiki_str = unwiki_str.lstrip() #suppression des espaces avant le début du texte
    
    return unwiki_str

    
def nettoyerResumes(fichier_resumes, table_films, dossier_de_sortie):
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
    with open(fichier_resumes, 'r') as fichier:
        for ligne in fichier:
            
            res = Resume(ligne)
            film_id = res.id        
            if not film_id in table_films:
                logging.warning("Le film \""+film_id+"\" n'est pas dans la table de référencement")
                continue
            
            film_data = table_films[film_id]
            
            data = {}
            data["wikiId"] = film_id
            data["titre"] = film_data.nom
            data["dateSortie"] = film_data.dateSortie
            data["duree"] = film_data.duree
            data["genre"] = film_data.genre
            data["resume"] = nettoyerResume(res.data)
            
            
            path_ = os.path.join(dossier_de_sortie, "{0}.json".format(cpt))
            with open(path_, 'w') as outfile:
                json.dump(data, outfile)
                
            
            cpt+=1
            
#%%

def nettoyer(fichier_table_film, fichier_resume, dossier_sortie):
    '''
    Ecrit dans un fichier propre à chaque film les informations de ce dernier ainsi que son résumé. Les fiches sont numérotées dans l'ordre de lecture en débutant à 0
    
    ARGUMENTS :
        fichier_table_film (string) : chemin du fichier contenant les informations des films - fichier CSV (avec comme séparateur la tabulation) associant l'indentifiant wikipédia du film et ses informations
        fichier_resume (string) : chemin du fichier contenant tous les résumes au format <identifiant wikipedia>[espace\tabulation]<texte du résumé>
        dossier_de_sortie (string) : chemin vers le dossier où seront écrites les fiches des films
    SORTIE :
        None
    '''
    table_films = lireTableDonnee(fichier_table_film)
    nettoyerResumes(fichier_resume, table_films, dossier_sortie)

#%%

            
            