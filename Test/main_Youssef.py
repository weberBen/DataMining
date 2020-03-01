#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#%%
import environment as Env
import sys, os
#import Frequency.SummaryWordFrequency as Freq
#from nltk.stem.porter import *
from querySystem.matrixOp import *
import time


info = Env.Info()
'''
wordsBagInfo = Env.WordsBagInfo(ignore=True)
info = Env.Info(wordsBagInfo=wordsBagInfo)
'''
'''
env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
database = env_obj.Database
wordsBag = env_obj.WordsBag'''
#F=Freq.Frequency(None,None, "MoviesFrequence.txt")

"""
it = F.iterator2()
cpt = 0
while it.hasNext():
    print("&&&&&&&&&&&&&&&&& MOVIE  &&&&&&&&&&&&&&&&&")
    m = it.getNext()
    print("\tid_movie="+str(m.id))
    itt = m.iterator()
    
    print("----> itration freq movie")
    while itt.hasNext():
        print("id_word, freq=", itt.getNext())
    
    cpt+=1
    
    if cpt==3:
        break
    
"""    
#print(F._filename)
#F.computeFrequency()

'''
F2=Freq.MovieFreq("MoviesFrequence.txt","0")
it=F2.iterator()

cpt=0
while cpt<4:
    test = it.getNext()
    print(test)
    cpt+=1
'''

#%%
List_movie=["Argo","The Artist","The King's Speech","Slumdog Millionaire","Million Dollar Baby","The Lord of the Rings: The Return of the King","Titanic","Forrest Gump"]
List_search=["cover story escapees Mendez Hollywood make-up artist fake production company U.S. Central Intelligence Iranian culture contact planned military rescue alias Kevin Harkins science fantasy adventure",
             "Valentin Zimmer Kinograph Studios silent film new sound film single film canister latest hit film paid loyal Clifton tock Market Crash superb dancing ability",
             "Bertie King George King Edward new king Royal Family Logue dining room table Minister Stanley Baldwin Australian-born Lionel Logue",
             "Jamal Salim Javed Latika Maman third musketeer grand prize answer Salim orders Jamal rival crime lord",
             "Frankie Maggie Scrap cantankerous boxing trainer amateur boxing division illegal sucker punch unpunished dirty fighter medical rehabilitation facility manager Mickey Mack Los Angeles gym",
             "Frodo Aragorn Gollum Gandalf Ring Sauron Minas Tirith Pippin Gondor Mordor",
             "Cal Jack necklace boat deck mother Ruth board Wall Street Crash New York City Akademik Mstislav Keldysh Rose Dawson Calvert",
             "Forrest United States President Lieutenant Dan Jenny named Forrest Gump Bubba bus stop white feather John Lennon first day"]




env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
database = env_obj.Database
wordsBag = env_obj.WordsBag
Freq = env_obj.Frequency


debut = time.time()

matrix = "matrix_"+"all"+"_but_for_real"+"_for_real_now"
r = Request(database, wordsBag, Freq, env_obj.getMatrixFolder())
r.load(matrix)
msg="number of movies to test (max : "+str(len(List_movie))+"): "
nbr=int(input(msg))
L=[]
for k in range(nbr) :
    movie = r.search(List_search[k], 1)
    
    if(movie.title==List_movie[k]):
        L.append(1)
    else:
        L.append(0)
fin = time.time()   


print("\n\n----------------------------------------------\n\n")

print("Test 1 : search of movies, normal method\n")

for k in range (len(L)):
    if (L[k]==1):
        print("Search of the movie <"+List_movie[k]+"> = SUCCESS")
    else:
        print("Search of the movie <"+List_movie[k]+"> = FAILED")
print("\n",str(int(fin-debut)),"s ")
print("\n\n----------------------------------------------\n\n")
