#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import environment as Env
import sys, os
import querySystem.matrixOp as query
from Gui.gui import App
#%%
raw = input("Start as gui application ? [y/n] : ")
if raw=="y":
    dataset = input("Dataset to load : ")
    app = App(dataset)
    app.run()
else:
    
    def getParms():
        while True:
            try :
                max_nbr_res=int(input("Maximun results to see : "))
                break
            except ValueError:
                pass
        
        while True:
            try :
                threshold=float(input("Threshold results score : "))
                break
            except ValueError:
                pass
        return max_nbr_res, threshold
    
    info = Env.Info()
    env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
    database = env_obj.Database
    wordsBag = env_obj.WordsBag
    Freq = env_obj.Frequency
    
    dataset = input("Dataset to load : ")
    r = query.Request(database, wordsBag, Freq, env_obj.getMatrixFolder())
    r.load(dataset)
    
    max_nbr_res, threshold = getParms()
    
    while True:
        print("-----------------------------------------")
        raw = input("Search : ")
        response = r.search(raw, max_nbr_res, threshold)
        res = response.results
        print("Filtered query : "+str(response.filteredQuery))
        print("Maximun results number : "+str(max_nbr_res))
        print("Threshold results score : "+str(threshold))
        
        if len(res)==0:
            print("No results")
        else:
            for movie_id, score in res:
                movie = database.getMovie(movie_id)
                print("Movie id :" + str(movie.id)+ ", Movie title : <<"+str(movie.title)+">>, Score :"+str(score))
        
        print("-----------------------------------------")
        raw = input("New search ? [y/n] : ")
        if raw=="n":
            break
        
        raw = input("Change settings ? [y/n] : ")
        if raw=="y":
            max_nbr_res, threshold = getParms()
            
    