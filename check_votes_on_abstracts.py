#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 16:40:34 2025

Checks reviews on abstracts

@author: delerue
"""

import params

#import sys
#import json
#import requests,json
from datetime import datetime
#import matplotlib.pyplot as plt
#import numpy as np

#sys.path.append('../jacow-ipac-lpr/')
import users_functions as uf
#import jacow_nd_func as jnf
#import papers_functions as pf
import indico_functions as indf

headers = {'Authorization': f'Bearer {params.api_token}'}


data = indf.indico_get(f'{params.event_url}/manage/abstracts/abstracts.json',datatype='json',headers=headers)
#print(data.text)
#print(data.json().keys())

'''
if 1==0:
    print(len(data['abstracts']))
    iabstract=53
    print(data['abstracts'][iabstract]['id'])
    print(data['abstracts'][iabstract]['friendly_id'])
    #print(data['abstracts'][iabstract]['submitter'])
    print(data['abstracts'][iabstract].keys())
    print(data['abstracts'][iabstract]['reviews'])
    print(len(data['abstracts'][iabstract]['reviews']))
'''

all_votes_spm={}
all_votes_abstract={}


print("Checking votes")
for abstract in data['abstracts']:
    if not abstract['state'] in [ 'duplicate' ,'withdrawn' , 'rejected' ]:
        if (len(abstract['reviews'])>0):
            for review in abstract['reviews']:
                #print("review ","id",abstract['id'],abstract['friendly_id'],abstract['state'],f"{params.event_url}abstracts/{abstract['id']}/")
                #theroles=uf.has_role_codes(userid=review['user']['id'])
                #print("    user:",review['user']['id'],review['user']['full_name'])
                #print("    ratings:",review['ratings'])
                if review['ratings'][0]['value'] is None and review['ratings'][1]['value'] is None:
                    pass
                elif review['ratings'][0]['value'] is False and review['ratings'][1]['value'] is False:
                    pass
                else:
                    if review['ratings'][0]['value'] is True and review['ratings'][1]['value'] is True:
                        print("Warning: Double True vote!" )
    
                    if not review['user']['id'] in all_votes_spm.keys():
                        all_votes_spm[review['user']['id']]={}
                        all_votes_spm[review['user']['id']]['full_name']=review['user']['full_name']
                        for imc in range(1,9):
                            all_votes_spm[review['user']['id']]["MC"+str(imc)]={}
                            all_votes_spm[review['user']['id']]["MC"+str(imc)]['1st']=[]
                            all_votes_spm[review['user']['id']]["MC"+str(imc)]['2nd']=[]                            
                            
                    if not abstract['id'] in all_votes_abstract.keys():
                        all_votes_abstract[abstract['id']]={}
                        all_votes_abstract[abstract['id']]['MC']=abstract['submitted_for_tracks'][0]['title'][0:3]
                        all_votes_abstract[abstract['id']]['1st']=[]
                        all_votes_abstract[abstract['id']]['2nd']=[]
                    if review['ratings'][0]['value'] is True:
                        all_votes_spm[review['user']['id']][abstract['submitted_for_tracks'][0]['title'][0:3]]['1st'].append(abstract['id'])                    
                        all_votes_abstract[abstract['id']]['1st'].append(review['user']['id'])
                    elif review['ratings'][1]['value'] is True:
                        all_votes_spm[review['user']['id']][abstract['submitted_for_tracks'][0]['title'][0:3]]['2nd'].append(abstract['id'])                    
                        all_votes_abstract[abstract['id']]['2nd'].append(review['user']['id'])
                        


full_names=sorted([ [all_votes_spm[thekey]['full_name'] , thekey ] for thekey in all_votes_spm.keys() ])
               
#print(full_names)
for fname in full_names:
    print(fname[0])
    print("     1st choices: ",end='')
    for imc in range(1,9):
        print(f"MC{imc}: ",len(all_votes_spm[fname[1]]["MC"+str(imc)]['1st']),end=" ")
    print("\n     2nd choices: ",end='')
    for imc in range(1,9):
        print(f"MC{imc}: ",len(all_votes_spm[fname[1]]["MC"+str(imc)]['2nd']),end=" ")
    print("")

for imc in range(1,9):
    print(f"MC{imc}")
    ranked=sorted([ [ 2*len(all_votes_abstract[theid]['1st'])+len(all_votes_abstract[theid]['2nd']),  theid] for theid in all_votes_abstract.keys() if all_votes_abstract[theid]['MC'] == "MC"+str(imc) ], reverse=True)
    for therank in ranked:
        print(therank[1],therank[0],len(all_votes_abstract[therank[1]]['1st']),len(all_votes_abstract[therank[1]]['2nd']))
