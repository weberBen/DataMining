#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import logging
import json
#%%

'''
    Manipulation de la base de données : 
        db = Database(dossier) où dossier est le chemin du dossier contenant toutes les fiches de film (numérotées de 0 à (n-1) où n est le nombre de fiches et suivant le format json {<wikiId> : ***, <titre> : ***, <dateSortie> : ***, <duree> : ***, <genre> : ***, <resume> : ***})
    Pour obtenir la fiche d'index i :
        fiche = db.getFiche(i)
        if fiche not None:
            print(fiche.toString()) #affichage de la fiche
            print(fiche.wikiId, fiche.titre, fiche.resume) #affichage de certaines informations
        else :
            print("Aucune fiche trouvée")
'''



#%%
class FicheFilm:
    def __init__(self, wiki_id, titre, date_sortie, duree, genre, resume):
        self.wikiId = wiki_id
        self.titre = titre
        self.dateSortie = date_sortie
        self.duree = duree
        self.genre = genre
        self.resume = resume
    
    def toString(self):
        return '<Film : wikiId= {0}, nom={1}, date_sortie={2}, genre={3}, resume={4}>'.format(self.wikiId, self.titre, self.dateSortie, self.genre, self.resume)
  
class Database:
    def __init__(self, dossier_fiches_films):
        '''
        Création d'un object base de données
        
        ARGUMENTS :
            dossier_fiches_films (string) : chemin du dossier contenant les fiches des films au format json ({<wikiId> : ***, <titre> : ***, <dateSortie> : ***, <duree> : ***, <genre> : ***, <resume> : ***})
                Les résumés sont supposés nettoyés
        '''
        self.dossierFiches = dossier_fiches_films
        self.ficheCourante = 0
    
    def getFiche(self, index):
        '''
        Obtention d'une fiche de film
        
        ARGUMENTS :
            index (int) : index de la fiche (de 0 à (n-1) où n est le nombre de fiches)
        '''
        
        if index<0:
            return None
        
        fiche = None
        fichier = os.path.join(self.dossierFiches, "{0}.json".format(index))
        with open(fichier, 'r') as json_file:
            data = json.load(json_file)
            wiki_id, titre, date_sortie, duree, genre, resume = data["wikiId"], data["titre"], data["dateSortie"], data["duree"], data["genre"], data["resume"]
            fiche = FicheFilm(wiki_id, titre, date_sortie, duree, genre, resume)
        
        return fiche


#%%

        