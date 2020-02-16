#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#%%
import environment as Env
import sys

info = Env.Info()
'''
wordsBagInfo = Env.WordsBagInfo(ignore=True)
info = Env.Info(wordsBagInfo=wordsBagInfo)
'''

env_obj = Env.setupEnv(sys.argv[0], info)
database = env_obj.Database
wordsBag = env_obj.WordsBag


#%%
