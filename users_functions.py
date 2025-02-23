#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:17:29 2025

User functions

@author: delerue
"""

import os
import joblib
from hashlib import md5
import requests

import params

import time


event_id = params.event_id

api_token = params.api_token
event_url=params.event_url


#List of all known users
users_file=params.users_file
#affiliations_file=params.affiliations_file


global skip_keys
skip_keys=[ 'affiliation_meta' , '_type' ,  '_fossil' , 'avatar_url' ]
global rewrite_keys
rewrite_keys={ 'id': 'db_id' , 'fullName' : 'full_name' }
#rewrite_keys={  }
global users
global affiliations
global emailHashesDict

def load_users():
    global emailHashesDict
    global users
    global affiliations
    if os.path.isfile(users_file):
        users=joblib.load(users_file)
    else:
        print("Warning: unable to load users from ",users_file)
        users={}
    #if os.path.isfile(affiliations_file):
    #    affiliations=joblib.load(affiliations_file)
    #else:
    #    affiliations={}
    emailHashesDict={}

def save_users():
    global users
    global affiliations

    joblib.dump(users,users_file)
    #joblib.dump(affiliations,affiliations_file)

def get_user(db_id):
    #print('In get_user(db_id)')
    global users
    if len(users)>0 and str(db_id) in users.keys():
        #print("users.keys()", users[db_id].keys())
        if 'moved_to' in users[db_id].keys():
            #print("User entry has moved",db_id,users[db_id]['moved_to'])
            return get_user(users[db_id]['moved_to'])
        return users[str(db_id)]
    elif db_id in emailHashesDict.keys():
        print("Using email hash")
        return users[emailHashesDict[str(db_id)]]
    else:
        return None


def get_user_id(emailHash):
    global emailHashesDict
    if len(emailHashesDict)>0 and emailHash in list(emailHashesDict.keys()):
        #print('user id found from email hash',emailHashesDict[emailHash])
        #exit()
        return emailHashesDict[emailHash]
    return emailHash
    
def search_user_by_id(userid):
    headers = { 'Authorization': f'Bearer {api_token}'}
    payload = {"values": [ "User:"+str(userid) ] }
    data = requests.post(f'https://indico.jacow.org/event/37/manage/api/principals', headers=headers, json=payload)
    if data.status_code==200:
        #print("search_user_by_id",data.json())
        keys=list(data.json().keys())
        return data.json()[keys[0]]
    else:
        return None
#search_user_by_id

def search_and_add_users_by_id(userid_list):
    headers = { 'Authorization': f'Bearer {api_token}'}
    users_list=[ "User:"+str(userid) for userid in userid_list ]
    payload = {"values": users_list }
    data = requests.post(f'https://indico.jacow.org/event/37/manage/api/principals', headers=headers, json=payload)
    if data.status_code==200:
        #print("search_and_add_users_by_id",data.json())
        keys=list(data.json().keys())        
        #print("keys",keys)
        for key in keys:
            add_user_info(data.json()[key]['user_id'],data.json()[key])
#search_user_by_id

def search_user_id(user):
    if 'email' in user.keys():
        data=search_user(email=user['email'])
    elif 'last_name' in user.keys():
        data=search_user(last_name=user['last_name'],verbosemode=False)
        if data is None:
            if 'first_name' in user.keys():
                data=search_user(last_name=user['last_name'],first_name=user['first_name'],verbosemode=False)
        if data is None:
            if 'emailHash' in user.keys():
                data=search_user(last_name=user['last_name'],emailHash=user['emailHash'],verbosemode=False)
        if data is None:
            if 'emailHash' in user.keys() and 'first_name' in user.keys():
                data=search_user(last_name=user['last_name'],first_name=user['first_name'],emailHash=user['emailHash'])
    if data is not None:
        print("Id found")
        print(data)
        time.sleep(1)
        add_user_info(user['user_id'], data)        
        save_users()
        return data['id']
    
    print('No userid found', user['last_name'], user['first_name'], user['emailHash'])
    return None
#search_user_id

global iSearch
iSearch=0
def search_user(email=None,last_name=None,first_name=None,emailHash=None,verbosemode=True,addToUsers=True,allow_search_again=True):
    global iSearch
    iSearch=iSearch+1
    if iSearch>params.maxUserSearch:
        print("Too many user searches done!!!")
        exit()
        return None
    else:
        headers = {'Authorization': f'Bearer {api_token}'}
        if email is not None:
            data = requests.get(f'https://indico.jacow.org/user/search/?email={email}&favorites_first=true&external=true', headers=headers)
        elif last_name is not None:
            if first_name is not None:
                data = requests.get(f'https://indico.jacow.org/user/search/?last_name={last_name}&external=true&first_name={first_name}', headers=headers)
            else:
                data = requests.get(f'https://indico.jacow.org/user/search/?last_name={last_name}&external=true', headers=headers)

        if not data.status_code == 200:
            print("Error searching for user")
            return None
        data_json=data.json()
        if len(data_json['users'])>1:
            if verbosemode:
                print("More than one user found for",first_name,last_name, emailHash, len(data_json['users']))
            if emailHash is not None:
                for user in data_json['users']:
                    if verbosemode:
                        print(user['email'], user['first_name'],user['last_name'] ,md5(user['email'].encode()).hexdigest(),emailHash)
                    if md5(user['email'].encode()).hexdigest()==emailHash:
                        return user
            return None
        elif len(data_json['users'])==0:
            if verbosemode:
                print("No user found")
            return None
        else:
            if addToUsers:
                keys=list(data_json['users'][0].keys()) 
                
                if data_json['users'][0]['id'] is None or  data_json['users'][0]['id']=='None':
                    user_id=data_json['users'][0]['identifier']
                else:
                    user_id=data_json['users'][0]['id']
                #print("keys",keys)
                add_user_info(user_id,data_json['users'][0])
                print("user added", data_json['users'][0])
                save_users()
                load_users()
                if allow_search_again:
                    if 'email' in data_json['users'][0].keys():
                        print('search again',data_json['users'][0]['email'])
                        return search_user(email=data_json['users'][0]['email'],allow_search_again=False)
            return data_json['users'][0]
        
        

#search_user


def add_user_info(user_id,user_info,date=None):
    global emailHashesDict
    global users
    global affiliations
    global skip_keys
    global rewrite_keys
    newUser=False
    if len(users)==0 or str(user_id) not in users.keys():
        users[str(user_id)]={ 'user_id' : str(user_id) }
    else:
        #print("User exists:", users[str(person_id)]['first_name'], users[str(person_id)]['last_name'], user_info['first_name'], user_info['last_name'])
        pass
    if 'affiliation_meta' in user_info.keys() and user_info['affiliation_meta'] is not None:
        if 'country_code' in user_info['affiliation_meta'].keys():
            #print("country:",user_info['affiliation_meta']['country_code'])
            user_info['country_code']=user_info['affiliation_meta']['country_code']
        if 'country_name' in user_info['affiliation_meta'].keys():
            user_info['country_name']=user_info['affiliation_meta']['country_name']
    for key in user_info.keys():
        if key not in skip_keys:
            if key in rewrite_keys:
                rewritten_key=rewrite_keys[key]
            else:
                rewritten_key=key            
            if rewritten_key in users[str(user_id)].keys():                
                if not str(users[str(user_id)][rewritten_key])==str(user_info[key]):
                    if not rewritten_key+"_all" in users[str(user_id)].keys():
                        users[str(user_id)][rewritten_key+"_all"]=[]
                        users[str(user_id)][rewritten_key+"_all"].append(users[str(user_id)][rewritten_key])
                    users[str(user_id)][rewritten_key+"_all"].append(str(user_info[key]))
                    #users[str(user_id)][rewritten_key+"_all"]=list(set(users[str(user_id)][rewritten_key+"_all"]))    
            else:
                users[str(user_id)][rewritten_key]=str(user_info[key])
    if 'email' in user_info.keys():
        #print('email in user_info')
        if str(get_email_hash(user_info['email'])) == user_id:
            #if 'id' in user_info.keys():
                #print("user_info['id']", user_info['id'])
            if 'identifier' in user_info.keys() and 'id' in user_info.keys() and user_info['id'] is not None and user_info['id'] >0:
                merge_users(user_info['id'], str(get_email_hash(user_info['email'])))                
        else:
            if not 'emailHash' in user_info.keys() or not user_info['emailHash'] == user_id:
                emailHashesDict[str(get_email_hash(user_info['email']))]=user_id
            if str(get_email_hash(user_info['email'])) in users.keys():                
                merge_users(user_id, str(get_email_hash(user_info['email'])))

#add_user_info
                
def add_paper_to_user(user_id,conf_id,paper_db_id,auth_type):
    global users
    if 'papers' not in users[str(user_id)].keys():
        users[str(user_id)]['papers']=[]
    #check if the paper is already in the list
    paperidx=-1
    for idx in range(len(users[str(user_id)]['papers'])):
        if str(users[str(user_id)]['papers'][idx][0])==str(conf_id) and str(users[str(user_id)]['papers'][idx][1])==str(paper_db_id):
            paperidx=idx
    if paperidx<0:
        users[str(user_id)]['papers'].append([conf_id,paper_db_id, [ auth_type ]])
    else:
        users[str(user_id)]['papers'][paperidx][2].append(auth_type)




def merge_users(userid1,userid2):
    global users
    global skip_keys
    global rewrite_keys
    #print("Merging", userid2 ,"into", userid1)
    if 'moved_to' in users[userid2].keys():
        print("Already merged")
        return
    if str(userid1) not in users.keys():
        userid1=str(userid1)
        users[str(userid1)]={ 'user_id' : str(userid1) }
    for key in users[userid2].keys():
        allkeys=skip_keys
        allkeys.append('papers')
        if key not in allkeys:
            if key in rewrite_keys:
                rewritten_key=rewrite_keys[key]
            else:
                rewritten_key=key
            #print("rewritten_key",rewritten_key)
            #print(users[str(userid1)].keys())
            if rewritten_key in users[str(userid1)].keys():                
                #print(users[str(userid1)][rewritten_key])
                if not (str(users[str(userid1)][rewritten_key])==str(users[str(userid2)][key])):
                    #print("rkey",rewritten_key,key )
                    if rewritten_key.endswith("_all"):
                        if type(users[str(userid1)][rewritten_key]) is not list:  
                            users[str(userid1)][rewritten_key] = [ users[str(userid1)][rewritten_key] ]
                        if type(users[str(userid2)][key]) is not list:
                            users[str(userid1)][rewritten_key].append(users[str(userid2)][key])
                        else:
                            for entry in users[str(userid2)][key]:
                                users[str(userid1)][rewritten_key].append(entry)
                        #users[str(userid1)][rewritten_key]=list(set(users[str(userid1)][rewritten_key]))
                    else:
                        #print("else")
                        if not rewritten_key+"_all" in users[str(userid1)].keys():
                            #if type() is list:
                            users[str(userid1)][rewritten_key+"_all"]=[]
                            users[str(userid1)][rewritten_key+"_all"].append(users[str(userid1)][rewritten_key])
                        if type(users[str(userid2)][key]) is list:
                            for entry in users[str(userid2)][key]:
                                users[str(userid1)][rewritten_key+"_all"].append(entry)
                        else:
                            users[str(userid1)][rewritten_key+"_all"].append(users[str(userid2)][key])
                        #users[str(userid1)][rewritten_key+"_all"]=list(set(users[str(userid1)][rewritten_key+"_all"]))

            else:
                users[str(userid1)][rewritten_key]=users[str(userid2)][key]
    if 'papers' not in users[str(userid1)].keys():
        users[str(userid1)]['papers']=[]
    for paper in users[userid2]['papers']:        
        users[str(userid1)]['papers'].append(paper)
    users.pop(userid2)
    users[userid2]={}
    users[userid2]['moved_to']=str(userid1)
#end merge_users(userid1,userid2):

def users_purity():
    #Change users emailHash as key with their real email address    
    global users
    global emailHashesDict
    #print('Keys')
    #print(users.keys())
    #print('dict')
    #print(emailHashesDict)
    #ukeys=copy.deepcopy(users.keys())
    ntot=0
    nemailHash=0
    nemailOk=0
    nredir=0
    nemailHashEmail=0
    nemailHashEmailDiff=0
    nemailHashEmailMulti=0
    nInDict=0
    ukeys=list(users.keys())
    for userid in ukeys:    
        ntot=ntot+1
        if 'moved_to' in users[userid].keys():
            nredir=nredir+1
        if 'emailHash' in users[userid].keys() and userid == users[userid]['emailHash']:
            nemailHash=nemailHash+1
            if 'email' in users[userid].keys():
                nemailHashEmail=nemailHashEmail+1
                if not users[userid]['emailHash'] == get_email_hash(users[userid]['email']):
                    nemailHashEmailDiff=nemailHashEmailDiff+1                
                if 'email_all' in users[userid].keys():
                    print("Multiple emails")
                    nemailHashEmailMulti=nemailHashEmailMulti+1
            if users[userid]['emailHash'] in emailHashesDict.keys():
                #print("in dict")
                nInDict=nInDict+1
        else:
            if 'email' in users[userid].keys():
                nemailOk=nemailOk+1
            

    print('*** Users files purity ***')
    print('Entries:',ntot)
    print('Entries linked to repository',nemailOk)
    print('Entries not linked to repository',nemailHash)
    print('Entries not linked to repository but with email address',nemailHashEmail)
    print('Entries not linked to repository with different email address',nemailHashEmailDiff)
    print('Entries not linked to repository with multiple email address',nemailHashEmailMulti)
    print('Entries not linked to repository but in link dictionnary',nInDict)
    print('Redirection entries ',nredir)
    
def clean_users():
    #Change users emailHash as key with their real email address    
    #import copy
    global users
    global emailHashesDict
    print('Cleaning...')
    #ukeys=copy.deepcopy(users.keys())
    ukeys=list(users.keys())
    for userid in ukeys:    
        if 'emailHash' in users[userid].keys() and userid == users[userid]['emailHash']:
            if 'email' in users[userid].keys():
                if users[userid]['emailHash'] == get_email_hash(users[userid]['email']):
                    pass
            if users[userid]['emailHash'] in emailHashesDict.keys():
                merge_users(emailHashesDict[users[userid]['emailHash']],userid)

    #For each user cleans the lists
    ukeys=list(users.keys())
    for userid in ukeys:
        for key in list(users[userid].keys()):
            #print('key',key)
            if key == 'papers':
                for ipaper in range(1,len(users[userid]['papers'])):
                    for jpaper in range(ipaper):
                        if users[userid]['papers'][ipaper][0]==users[userid]['papers'][jpaper][0] and users[userid]['papers'][ipaper][1]==users[userid]['papers'][jpaper][1]:
                                users[userid]['papers'][ipaper][2].extend(users[userid]['papers'][jpaper][2])
                                users[userid]['papers'][jpaper][0]=None
                papers=[]
                for paper in users[userid]['papers']:
                    if paper[0] is not None:
                        paper[2]=list(set(paper[2]))
                        papers.append(paper)
                users[userid]['papers']=papers
            elif type(users[userid][key]) is list:
                users[userid][key]=list(set(users[userid][key]))
    print('After cleaning...')
#end def clean_users():
    
def get_email_hash(email):
    return md5(email.encode()).hexdigest()



def find_user(user_id=None,last_name=None,first_name=None,email=None,verbose=False):
    #import jacow_nd_func as jnf
    load_users()
    
    return_array=[]
    nmatch=0
    for user in list(users):
        user_data=users[user]
        match=True
        #print('user',user,user_data)
        if user_id is not None:
            if not str(user_data['user_id'])==str(user_id):
                if 'user_id_all' in user_data.keys():
                    if not str(user_id) in user_data['user_id_all']:
                        match=False
                else:
                    match=False
                
        if last_name is not None:
            if 'last_name' in user_data.keys() :
                if not user_data['last_name'].lower()==last_name.lower():
                    match=False
            else:
                match=False
        if first_name is not None and 'first_name' in user_data.keys() :
            if not user_data['first_name'].lower()==first_name.lower():
                match=False
        if email is not None:
            if 'email' in user_data.keys() :
                if not user_data['email'].lower()==email.lower():
                    match=False
            else:
                match=False
                
        if match:        
            userdict={}
            if verbose:
                print("*** User match")
            if 'user_id' in user_data.keys() and 'emailHash' in user_data.keys():
                if user_data['user_id'] == user_data['emailHash']:
                    if verbose:
                        print("Matching user is not linked to repository. Checking repository for updates.")
                    search_user_id(user_data)
            ordered_keys= [ 'user_id', 'title', 'first_name', 'last_name', 'full_name', 'affiliation', 'country_code', 'country_name', 'email']
            for key in user_data:
                if key not in ordered_keys:
                    ordered_keys.append(key)
            for key in ordered_keys:
                if key in user_data.keys():
                    if key not in [ 'papers']:
                        if not key.endswith("_all"):
                            userdict[key]=user_data[key]
                            if verbose:
                                print("  ", key,user_data[key])
                            if key+"_all" in user_data.keys(): 
                                userdict[key]=user_data[key+"_all"]
                                if verbose:
                                    print("      all:",user_data[key+"_all"])
            if 'papers' in user_data.keys():
                userdict['papers']=[]
                for paper in user_data['papers']:
                    conf=paper[0].replace('41','IPAC23').replace('63','IPAC24').replace('91','IPAC25').replace('95','IPAC26')
                    userdict['papers'].append({'conf':conf , 'id': paper[1],  'role': paper[2]})
                    if verbose:
                        print("   Paper: conf",conf," id:",paper[1]," role:",paper[2])
            if verbose:
                print('=====')
            nmatch=nmatch+1
            return_array.append(userdict)
    #print(nmatch,"users matched out of",len(users))
    if verbose:
        print(nmatch,"users matched out of",len(users))
    
    if nmatch==0:
        #print(email)
        if email is not None:
            #print("jnf.email",email)
            json_data=search_user(email=email)
            return_array.append(json_data)
            if verbose:
                print(json_data)
                print(get_email_hash(email))                
        elif last_name is not None:
            jnf_info=search_user(last_name=last_name)
            return_array.append(jnf_info)
            if verbose:
                print(jnf_info)
            
    return return_array
#end find_user


#### Below: country and region functions

    
def user_is_not_region(user,region_code):
    if 'country_code' in user.keys():
        if get_user_region(user['country_code']) not in [ params.REGION_UNKNOWN_CODE , region_code ]:
            return True
    return False            


def get_user_region(country_code):
    if country_code in params.list_countries_EMEA:
        return params.EMEA_CODE
    if country_code in params.list_countries_Asia:
        return params.ASIA_CODE
    if country_code in params.list_countries_Americas:
        return params.AMERICAS_CODE
    if country_code=='':
        return params.REGION_UNKNOWN_CODE
    return params.REGION_UNKNOWN_CODE
