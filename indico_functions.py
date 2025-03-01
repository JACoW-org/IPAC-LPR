#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 10:27:01 2025

Indico management functions

@author: delerue
"""

import os
import requests,json

def indico_extract_error(text):
    idx_start=text.find("error-box")
    idx_end=text.find("error-box-small")
    print(text[idx_start+10:idx_end-20])
    
def indico_get(url,headers=None,payload=None,cachable=False,datatype='text'):
    if cachable:
        filename="data/"+url.replace("https://","").replace("/","_").replace(".","_")+".cached_url"
        if os.path.isfile(filename):
            fdata=open(filename,"r")
            if datatype=='text': 
                data=fdata.read()
            elif datatype=='json': 
                data=json.load(fdata)
            fdata.close()
            return data
    data = requests.get(url,headers=headers)
    #print(payload)
    if data.status_code != 200:
        print('Status code',data.status_code,'for URL',url)
        indico_extract_error(data.text)
        return None
    if data.text.find("error-box")>0:
        indico_extract_error(data.text)
        return None
    if cachable:
        fdata=open(filename,"w")
        if datatype=='text': 
            data=fdata.write(data.text)
        elif datatype=='json': 
            json.dump(data.json(),fdata)
        fdata.close()
    if datatype=='text': 
        return data.text
    elif datatype=='json': 
        return data.json()

def find_indico_value(marker,text,idx):
    idx=text.find(marker,idx)
    if idx>0:
        idx_start=text.find('"',idx)
        idx_end=text.find('"',idx_start+1)
        value=text[idx_start+1:idx_end]
        return [idx_end,value]
    else:
        return [-1,""]

def find_indico_named_value(marker,text,idx):
    idx=text.find(marker,idx)
    if idx>0:
        idx=text.find("value",idx)
        idx_start=text.find('"',idx)
        idx_end=text.find('"',idx_start+1)
        value=text[idx_start+1:idx_end]
        return [idx_end,value]
    else:
        return [-1,""]

def accumulate(value,thedict,subvalue=None):
    if not value in thedict.keys():
        thedict[value]={}
        thedict[value]['All']=0
    thedict[value]['All']=thedict[value]['All']+1
    if subvalue is not None:
        if not subvalue in thedict[value].keys():       
            thedict[value][subvalue]=0
        thedict[value][subvalue]=thedict[value][subvalue]+1
