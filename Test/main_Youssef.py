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
List_movie=["Argo","The Artist","The King's Speech","Slumdog Millionaire","Million Dollar Baby","The Lord of the Rings: The Return of the King","Titanic","Forrest Gump","Schindler's List","Gladiator"]
List_search=["cover story escapees Mendez Hollywood fake production company CIA Iranian military rescue Kevin Harkins",
             "Valentin Zimmer Kinograph Studios silent film paid loyal Clifton tock Market Crash dancing ability",
             "Bertie Lionel King George King Edward new king Royal Family Logue dining room table Minister Stanley Baldwin Australian-born Lionel Logue",
             "Jamal Salim Javed Latika Maman third musketeer grand prize answer Salim orders Jamal rival crime lord",
             "Frankie Maggie Scrap cantankerous boxing trainer amateur boxing division illegal sucker punch unpunished dirty fighter medical rehabilitation facility manager Mickey Mack Los Angeles gym",
             "Frodo Aragorn Gollum Gandalf Ring Sauron Minas Tirith Pippin Gondor Mordor",
             "Cal Jack necklace boat deck mother Ruth board Wall Street Crash New York City Akademik Mstislav Keldysh Rose Dawson Calvert",
             "United States President Lieutenant Dan Jenny named Forrest Gump Bubba bus stop white feather John Lennon first day",
             "Schindler Jewish workers German war effort Auschwitz concentration camp overcrowded Kraków Ghetto business community Nazi Party member",
             "Maximus Commodus gladiators Colosseum Lucilla Juba Emperor Marcus Aurelius Guard arrest Gracchus"]




env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
database = env_obj.Database
wordsBag = env_obj.WordsBag
Freq = env_obj.Frequency





matrix = "matrix_"+"all"+"_but_for_real"+"_for_real_now"
r = Request(database, wordsBag, Freq, env_obj.getMatrixFolder())




msg="number of movies to test (max : "+str(len(List_movie))+"): "
nbr=int(input(msg))
for rang in range(2000,2001,100):
    L=[]
    nnnnn=0
    debut=time.time()
    r.load(matrix,k=rang)
    fin=time.time()
    print("\n",rang," ",fin-debut,"\n")

    for k in range(nbr) :
        
        response = r.searchSVD(List_search[k], 5)
        res = response.results

        for l,s in res:
            movie = database.getMovie(l)
            print(movie.title)
        
        if len(res)<1:
            print("no result")
        
        movie_id, score  = res[0]
        movie = database.getMovie(movie_id)
        

        
        if(movie.title==List_movie[k]):
            L.append(1)
            nnnnn+=1
            print("\nsucces\n")

    print("\n pour le rang "+str(rang)+" on a un succes de "+str(nnnnn)+"/"+str(nbr)+"\n")
fin = time.time()   

"""
print("\n\n----------------------------------------------\n\n")

print("Test 1 : search of movies, normal method\n")

for k in range (len(L)):
    if (L[k]==1):
        print("Search of the movie <"+List_movie[k]+"> = SUCCESS")
    else:
        print("Search of the movie <"+List_movie[k]+"> = FAILED")
print("\n",str(int(fin-debut)),"s ")
print("\n\n----------------------------------------------\n\n")
"""