# -*- coding: utf-8 -*-

import sys
import json

import re
from string import punctuation
from time import perf_counter
from pathlib import Path

def word_frequency(id_film):
    ''' pour chaque résume cree un fichier qui donne le nombre d'occurence
    des mots (en faisant référence à l'identifiant du fichier précédent)

    ARGUMENTS :
        id_film (int) : id du film
    SORTIE : creer un fichier id_film_freq.txt de la forme:
    id_mot1 mot1 nbr_mot1
    id_mot2 mot2 nbr_mot2

    '''
 #start = perf_counter()
    print("Dataset/DonneesNettoyees/"+str(id_film)+'.json')
    with open( Path("Dataset/DonneesNettoyees/"+str(id_film)+'.json')) as f_json:
        json_data = json.load(f_json)
        summary = json_data['resume'].strip('\n')
        f_json.close()
        print("Résumé de "+str(id_film))
        #print(summary)

    summary = re.sub('[^\w\s-]','',summary).replace('-',' ')
    print(summary)
    bananasplit = summary.lower().split(' ')
    dico = dict()

    for w in bananasplit:
        #tid = getID(w)
        #if tid is not None:
        dico.setdefault(w, 0)
        dico[w] += 1

    #print("Taille du dico : "+str(sys.getsizeof(dico))+" bytes")

    text_file = open(str(id_film)+"_freq.txt", "w")
    for w in dico:
        text_file.write(str(w)+" "+str(dico[w])+"\n")
    #end = perf_counter()
    #print("Temps écoulé : "+str(end-start)+" s")


if __name__ == "__main__":
    for k in range (5):
        word_frequency(k)

                

    """    with open( Path("Dataset/DonneesNettoyees/"+str(id_film)+'.json')) as f_json: # j'ouvre le fichier du film et recup le résumé
      json_data = json.load(f_json)
      summary=json_data['resume']
      f_json.close()
      print(summary)
    
    with open('dictionnaire.txt') as f_dictionary:  # j'ouvre le fichier avec les mots qu'on cherche
        dictionary = f_dictionary.readlines()
        
    text_file = open(str(id_film)+"_freq.txt", "w") # creer le fichier voulu du film
    
    for line in dictionary:     # pour chaque mot du dictionnaire cherche les occurence dans le résumé
        word=line.split(' ')[1]
        cpt=0
        for w in re.split(r'[-|,|.|\s]\s*',summary) : 
            if word == w:
                cpt+=1
        print("le mot <"+word+"> est la "+str(cpt) +" fois"+"\n")
        
        text_file.write(line.split(' ')[0]+" "+word+" "+str(cpt)+"\n") # ecrit le nombre d'occurence dans le fichier 
    text_file.close()
        """