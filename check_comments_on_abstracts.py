#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 16:40:34 2025

Checks comments on abstracts

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
    print(data['abstracts'][iabstract]['comments'])
    print(len(data['abstracts'][iabstract]['comments']))
'''

date_format = "%Y-%m-%d"
last_check="2025-03-18"
date_checked = datetime.strptime(last_check, date_format)

ncomments=1

print("Checking comments")
for abstract in data['abstracts']:
    #print(abstract.keys())
    if not abstract['state'] in [ 'duplicate' ,'withdrawn' , 'rejected' ]:
        if (len(abstract['comments'])>0):
            first_comment=True
            for comment in abstract['comments']:
                date_submitted = datetime.strptime(comment['created_dt'][0:10], date_format)
                if (date_submitted>date_checked) and not (comment['user']['id']in [ 877 ] ):
                    if first_comment:
                        print("Comment ",ncomments,"id",abstract['id'],abstract['friendly_id'],abstract['submitted_for_tracks'],abstract['state'],f"{params.event_url}abstracts/{abstract['id']}/")
                        first_comment=False
                    theroles=uf.has_role_codes(userid=comment['user']['id'])
                    print("    user:",comment['user']['id'],comment['user']['full_name'],theroles)
                    print("    text:",comment['text'])
                    print("    date:",comment['created_dt'][0:20])
                    ncomments=ncomments+1
                    #print(comment.keys())
                    #print(comment['user'].keys())
                    print("   ")
    
        if (len(abstract['reviews'])>0):
            first_comment=True
            for comment in abstract['reviews']:
                date_submitted = datetime.strptime(comment['created_dt'][0:10], date_format)                
                if (date_submitted>date_checked) and not (comment['user']['id']in [ 877 ] ):
                    #print(comment.keys())
                    if first_comment:
                        print("Review ",ncomments,"id",abstract['id'],abstract['friendly_id'],abstract['submitted_for_tracks'][0]['title'][0:3],abstract['state'],f"{params.event_url}abstracts/{abstract['id']}/")
                        first_comment=False
                    theroles=uf.has_role_codes(userid=comment['user']['id'])
                    print("    user:",comment['user']['id'],comment['user']['full_name'],theroles)
                    print("    action:",comment['proposed_action'])
                    print("    text:",comment['comment'])
                    print("    date:",comment['created_dt'][0:20])
                    ncomments=ncomments+1
                    #print(comment)
                    #print(comment['user'].keys())
                    print("   ")
