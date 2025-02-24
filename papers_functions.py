#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 00:13:18 2025

Function to access paper and contributions data

@author: delerue
"""

import params
import os
import time
import requests
import json

### Papers and contribs 
def get_paper_info(db_id,event_id=None,use_cache=False,file_age_to_renew=24*60*60,sleep_before_online=0.5):
    return get_paper_contrib_info(db_id,event_id=event_id,use_cache=use_cache,file_age_to_renew=file_age_to_renew,sleep_before_online=sleep_before_online,filetype='paper')

def get_contrib_info(db_id,event_id=None,use_cache=False,file_age_to_renew=24*60*60,sleep_before_online=0.5):
    return get_paper_contrib_info(db_id,event_id=event_id,use_cache=use_cache,file_age_to_renew=file_age_to_renew,sleep_before_online=sleep_before_online,filetype='contrib')

def get_paper_contrib_info(db_id,event_id=None,use_cache=False,file_age_to_renew=24*60*60,sleep_before_online=0.5,filetype='paper'):
    if event_id is None:
        conf_id=params.event_id
    filename="papers/"+filetype+"_"+str(db_id)+".json"
    use_online=True
    if use_cache:
        #print(filename)
        if os.path.isfile(filename):
            file_age=time.time()-os.path.getmtime(filename)
            if file_age_to_renew>0:
                if file_age > file_age_to_renew:
                    print('file_age',file_age)
                    use_online=True
                    print("Updating paper from online")
                else:
                    use_online=False
            else:
                use_online=False
        else:
            use_online=True
    #print('use_online',use_online)
    if use_online:
        time.sleep(sleep_before_online)
        headers = {'Authorization': f'Bearer {params.api_token}'}
        if filetype=='paper':
            url=f'https://indico.jacow.org/event/{event_id}/papers/api/'+str(db_id)
        elif filetype=='contrib':
            url=f'https://indico.jacow.org/event/{event_id}/contributions/{db_id}.json'       
        data = requests.get(url, headers=headers)
        #print('accessing url ',url)
        if data.status_code == 200:
            fdata=open(filename,"w")
            json.dump(data.json(),fdata)
            fdata.close()
            return(data.json())
        else:
            fdata=open(filename,"w")
            fdata.write("{}")
            fdata.close()
            print('Status code (',filetype,' access)', data.status_code,url)
            #print('db_id',db_id)
            return None
    else:
        fdata=open(filename,"r")
        data_json=json.load(fdata)
        fdata.close()
        #print('data_json',data_json,len(data_json))
        if len(data_json) <5:
            return None
        else:
            return data_json
