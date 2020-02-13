#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from environment import EnvVar
import os


dataset_folder_path = '/home/benjamin/Documents/UPMC/L3/Projet_Math/DataMining/Dataset'
Env = EnvVar(dataset_folder_path)
database = Env.Database
wordsBag = Env.WordsBag


'''
itération sur tous les (fichiers des) films
--> Youssef utilise ca pour parcourir les films à la place d'utiliser les fichiers directement
'''

it = database.iterator()
cpt = 0
while it.hasNext():
    movie = it.getNext()
    print(movie.title)
    cpt+=1
    
    if cpt==10:
        break


'''
itération sur tous les mots du dictionnaire
'''

it = wordsBag.iterator()

cpt = 0
while it.hasNext():
    word = it.getNext()
    print(word)
    cpt+=1
    
    if cpt==10:
        break

'''
existence d'un mot dans le dictionnaire
'''

word1 = "shoot on sight"
word3 = "Shooter"
word4 = "geronima"


print("1:", (wordsBag.getId(word1) is not None))
print("2:", (wordsBag.getId(word2) is not None))
print("3:", (wordsBag.getId(word3) is not None))
print("4:", (wordsBag.getId(word4) is not None))

