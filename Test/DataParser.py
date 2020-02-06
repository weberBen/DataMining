#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import ast

class Film:
  def __init__(self, nom, date_sortie, duree, langue, pays, genre, eplm_fichier=-1):
    self.nom = nom
    self.dateSortie = date_sortie
    self.duree = duree
    self.langue = langue
    self.pays = pays
    self.genre = genre
    self.eplmFichier = eplm_fichier
    
  def toString(self):
      return '<Film : nom={0}, date_sortie={1}, genre={2}>'.format(self.nom,self.dateSortie, self.genre)
    
def lireResume(ligne_resume):
    _id = ""
    pos = 0
    
    for c in ligne_resume:
        if not c.isalnum():
            break
        _id+=c
        pos+=1
    
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
    L = []
    for key, value in genre_dico.items():
        L.append(value)
        
    return L

def lireTableDonnee(filename):
    table = {}
    
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        
        for row in csv_reader:
            wiki_id, freebase_id, nom, date_sortie, revenu, duree, langue, pays, genre = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]
            genre_dico = ast.literal_eval(genre)
            table[wiki_id] = Film(nom, date_sortie, duree, langue, pays, listeGenre(genre_dico))
            
        
        return table
    

def trouverEmplacementFilm(filename, table_film):
    curseur = 0 
    with open(filename, 'r') as file:
        for ligne in file:
            
            film_id = Resume(ligne).id
            if not film_id in table_film:
                print("Le film \""+film_id+"\" n'est pas dans la table de référencement")
                curseur+= len(ligne)
                continue
            table_film[film_id].eplmFichier = curseur
            
            curseur+= len(ligne)


def getResume(table_film, fichier_resume, film_id):
    empl = table_film[film_id].eplmFichier
    fichier_resume.seek(empl)
    return Resume(fichier_resume.readline()).data

film_table = lireTableDonnee('/users/Etu6/3678096/movie.metadata.tsv')
trouverEmplacementFilm('/users/Etu6/3678096/plot_summaries.txt', film_table)
fichier_resume = open('/users/Etu6/3678096/plot_summaries.txt', 'r')
print(getResume(film_table, fichier_resume, '18188932'))