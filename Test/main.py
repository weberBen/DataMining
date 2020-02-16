#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import environment as Env
from environment import EnvVar
import os
import sys
from pathlib import Path

def getEnvPath():
    current_path = Path(sys.argv[0]).parent
    dataset_path = os.path.join(current_path,  Env.DATASET_FOLDER_NAME)
    
    while ((not os.path.exists(dataset_path)) or (not os.path.isdir(dataset_path))) and len(dataset_path)!=0:
        current_path = Path(current_path).parent
        dataset_path = os.path.join(current_path,  Env.DATASET_FOLDER_NAME)
    
    
    return dataset_path


root_path = getEnvPath()

#wordsBagInfo = Env.WordsBagInfo(os.path.join(root_path, "dictionnary.json"), True)
wordsBagInfo = None

env = EnvVar(root_path, wordsBagInfo=wordsBagInfo)
database = env.Database
wordsBag = env.WordsBag
'''
wordsBag.initialize(database, 1000)
wordsBag.update()'''

'''
itération sur tous les (fichiers des) films
--> Youssef utilise ca pour parcourir les films à la place d'utiliser les fichiers directement
'''

print("\n------------Movies title------------")
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
print("\n------------Words registered------------")

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

print("\n------------Tests words in dictionnary------------")

word1 = "shoot on sight"
word3 = "Shooter"
word4 = "geronima"


print("1:", (wordsBag.getId(word1) is not None))
print("3:", (wordsBag.getId(word3) is not None))
print("4:", (wordsBag.getId(word4) is not None))

