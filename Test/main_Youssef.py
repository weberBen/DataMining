#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#%%
import environment as Env
import sys, os
import Frequency.SummaryWordFrequency as Freq

info = Env.Info()
'''
wordsBagInfo = Env.WordsBagInfo(ignore=True)
info = Env.Info(wordsBagInfo=wordsBagInfo)
'''

env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
database = env_obj.Database
wordsBag = env_obj.WordsBag

Freq.parcourIterateur(database,wordsBag)






#%%
