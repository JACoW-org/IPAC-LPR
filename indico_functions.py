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
    #Extracts from the page the value of an anchor identified by "marker"
    #returns both the index and the value
    idx=text.find(marker,idx)
    if idx>0:
        idx_start=text.find('"',idx)
        idx_end=text.find('"',idx_start+1)
        value=text[idx_start+1:idx_end]
        return [idx_end,value]
    else:
        return [-1,""]

def find_indico_named_value(marker,text,idx,value_txt="value"):
    #Extracts from the page the value of an anchor identified by "marker" where the value is 
    #dentified by the keywork "value" (or something else specified in value_txt)
    #returns both the index and the value
    idx=text.find(marker,idx)
    if idx>0:
        idx=text.find(value_txt,idx)
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

def comment_abstract(meeting_id,db_id, comment, visibility=None,indico_server="jacow.org",api_token=None):
    print("Commenting abstract ", db_id)
    headers = {'Authorization': f'Bearer {api_token}'}
    payload = { 'text': comment}
    if visibility is not None:
        if not visibility in [ "judges" ]:
            print("Visibility not understood")
            exit()
        payload['visibility'] = visibility
    #print(payload)
    data = requests.post(f'https://indico.{indico_server}/event/{meeting_id}/abstracts/{db_id}/comment', headers=headers, data=payload)

    #print(data)
    print("Response "+str(data.status_code))
    #if not (data.status_code == 200):
    #    exit()



def old_update_to_meeting(meeting_id,filename,filetype,indico_server="jacow.org",api_token=None,delete_key=None):
    if api_token is None:
        print("API token required")
        return
    headers = {'Authorization': f'Bearer {api_token}'}

    data = requests.get(f'https://indico.{indico_server}/event/{meeting_id}/', headers=headers)
    
    if not data.status_code==200:
        indico_extract_error(data.text)
        exit()           

    meeting_attachements=[]

    idx=1
    idx=data.text.find('<a class="attachment',idx)
    while idx>0:
        [idx,fileid]=find_indico_value('data-attachment-id=',data.text,idx)
        #print('fileid', fileid)
        [idx,titleid]=find_indico_value('title',data.text,idx)
        #print('titleid',titleid)
        if idx>0:
            meeting_attachements.append([fileid.strip(),titleid.strip()])

    if delete_key is None:
        print("No delete key, unable to check it the file already exists")
    else:
        for attach in meeting_attachements:
            #print(attach[0],attach[1])
            if attach[1]==filename:
                #print(attach[0],attach[1],"to be deleted",f'https://indico.{indico_server}/event/{meeting_id}/manage/attachments/{delete_key}/{attach[0]}/')                
                data2 = requests.delete(f'https://indico.{indico_server}/event/{meeting_id}/manage/attachments/{delete_key}/{attach[0]}/', headers=headers)
                if not data2.status_code==200:
                    print("Error")
                    indico_extract_error(data2.text)
                else:
                    print("deleted")
    
    print("Sending file",filename) 
    payload={ 'name':"files" ,  'filename': filename ,  'Content-Type' : filetype , "folder": '__None'  }
    files = {'files' : open(filename, 'rb')}
    data = requests.post(f'https://indico.{indico_server}/event/{meeting_id}/manage/attachments/add/files', headers=headers, data=payload , files=files)
        
    #print(data.status_code)
    if not data.status_code==200:
        indico_extract_error(data.text)
        exit()
    if data.text.find("The attachment has been uploaded")>0:
        print("Sucess")
    else:
        print("problem",data.text)
#end old_update_to_meeting

def update_to_meeting(meeting_id,filename,filetype,indico_server="jacow.org",api_token=None,delete_key=None):
    if api_token is None:
        print("API token required")
        return
    headers = {'Authorization': f'Bearer {api_token}'}

    data = requests.get(f'https://indico.{indico_server}/event/{meeting_id}/', headers=headers)
    
    if not data.status_code==200:
        indico_extract_error(data.text)
        exit()           

    meeting_attachements=[]

    #find token
    [idx,csrf_token]=find_indico_named_value("csrf-token",data.text,1,"content")
    print("csrf_token", csrf_token)


    idx=1
    idx=data.text.find('<a class="attachment',idx)
    while idx>0:
        [idx,fileid]=find_indico_value('data-attachment-id=',data.text,idx)
        #print('fileid', fileid)
        [idx,titleid]=find_indico_value('title',data.text,idx)
        #print('titleid',titleid)
        if idx>0:
            meeting_attachements.append([fileid.strip(),titleid.strip()])

    payload={ "csrf_token": csrf_token , 'name':"files" , 'title': filename , "__file_change_trigger": 'added-file',  'filename': filename ,  'Content-Type' : filetype , "folder": '__None'   }
    files = {'files' : open(filename, 'rb')}


    if delete_key is None:
        print("No delete key, unable to replace file")
    else:
        replaced=False
        for attach in meeting_attachements:
            #print(attach[0],attach[1])
            if attach[1]==filename:                
                print(attach[0],attach[1],f'https://indico.{indico_server}/event/{meeting_id}/manage/attachments/{delete_key}/{attach[0]}/')                
                if not replaced and 1==0:
                    print(payload)
                    url=f'https://indico.{indico_server}/event/{meeting_id}/manage/attachments/{delete_key}/{attach[0]}/'
                    print("Replacing file",filename,url)                     
                    data = requests.post(url, headers=headers, data=payload , files=files)
                    replaced=True
                else:
                    print("Deleting file",filename) 
                    data = requests.delete(f'https://indico.{indico_server}/event/{meeting_id}/manage/attachments/{delete_key}/{attach[0]}/', headers=headers)
                if not data.status_code==200:
                    print("Error")
                    indico_extract_error(data.text)
                    return
                else:
                    print("done")
    if not replaced:
        print("Sending file",filename) 
        data = requests.post(f'https://indico.{indico_server}/event/{meeting_id}/manage/attachments/add/files', headers=headers, data=payload , files=files)
        
    #print(data.status_code)
    if not data.status_code==200:
        indico_extract_error(data.text)
        #exit()
        return
    if data.text.find("The attachment has been uploaded")>0:
        print("Sucess (upload)",filename)
    elif data.text.find("has been updated")>0:
        print("Sucess (update)",filename)
    else:
        print("problem",data.text)
#end update_to_meeting

