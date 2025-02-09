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
import jacow_nd_func as jnf

#List of all known users
users_file="data/users_file.data"
affiliations_file="data/affiliations_file.data"
global skip_keys
skip_keys=[ 'affiliation_meta' , '_type' ,  '_fossil' , 'avatar_url' ]
global rewrite_keys
#rewrite_keys={ 'id': 'db_id' }
rewrite_keys={  }
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
        users={}
    if os.path.isfile(affiliations_file):
        affiliations=joblib.load(affiliations_file)
    else:
        affiliations={}
    emailHashesDict={}

def save_users():
    global users
    global affiliations

    joblib.dump(users,users_file)
    joblib.dump(affiliations,affiliations_file)

        
def add_user_info(user_id,user_info,date=None):
    global emailHashesDict
    global users
    global affiliations
    global skip_keys
    global rewrite_keys
    if len(users)==0 or str(user_id) not in users.keys():
        users[str(user_id)]={ 'user_id' : str(user_id) }
    else:
        #print("User exists:", users[str(person_id)]['first_name'], users[str(person_id)]['last_name'], user_info['first_name'], user_info['last_name'])
        pass
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
        if not str(get_email_hash(user_info['email'])) == user_id:
            if not 'emailHash' in user_info.keys() or not user_info['emailHash'] == user_id:
                emailHashesDict[str(get_email_hash(user_info['email']))]=user_id
                
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

                
def get_user(db_id):
    print('In get_user(db_id)')
    global users
    if len(users)>0 and str(db_id) in users.keys():
        return users[str(db_id)]
    else:
        return None


def get_user_id(emailHash):
    global emailHashesDict
    if len(emailHashesDict)>0 and emailHash in list(emailHashesDict.keys()):
        print('user id found from email hash',emailHashesDict[emailHash])
        #exit()
        return emailHashesDict[emailHash]
    return emailHash
    
    
def search_user_id(user):
    if 'email' in user.keys():
        data=jnf.search_user(email=user['email'])
        return data['id']
    elif 'last_name' in user.keys():
        data=jnf.search_user(last_name=user['last_name'],verbosemode=False)
        if data is None:
            if 'first_name' in user.keys():
                data=jnf.search_user(last_name=user['last_name'],first_name=user['first_name'],verbosemode=False)
        if data is None:
            if 'emailHash' in user.keys():
                data=jnf.search_user(last_name=user['last_name'],emailHash=user['emailHash'],verbosemode=False)
        if data is None:
            if 'emailHash' in user.keys() and 'first_name' in user.keys():
                data=jnf.search_user(last_name=user['last_name'],first_name=user['first_name'],emailHash=user['emailHash'])
        if data is not None:
            return data['id']
    print('No userid found', user['last_name'], user['first_name'], user['emailHash'])
    return None

'''
def get_user_from_person_id(person_id):
    global users
    matchid=[]
    for userid in users.keys(): 
        if 'person_id' in users[userid].keys():
            if str(users[userid]['person_id'])==str(person_id):
                 matchid.append(userid)
        if 'person_id_all' in users[userid].keys():
            if str(person_id) in users[userid]['person_id_all']:
                matchid.append(userid)
    matchid=list(set(matchid))
    #print(matchid)
    if len(matchid)==0:
        print("No user match for the person id!!!", person_id,matchid)
        return None
    elif len(matchid)==1:
        return users[matchid[0]]
    else:
        print("More than one user match the person_id!!!", person_id,matchid)
        for uid in matchid:
            print(users[uid])
        #exit()
        return users[matchid[0]]
#end get_user_from_person_id(db_id):

def get_user_from_id(db_id):
    global users
    matchid=[]
    for userid in users.keys(): 
        if 'id' in users[userid].keys():
            if str(users[userid]['id'])==str(db_id):
                 matchid.append(userid)
        if 'id_all' in users[userid].keys():
            if str(db_id) in users[userid]['id_all']:
                matchid.append(userid)
    matchid=list(set(matchid))
    #print(matchid)
    if len(matchid)==0:
        print("No user match for the id!!!", db_id,matchid)
        return None
    elif len(matchid)==1:
        return users[matchid[0]]
    else:
        print("More than one user match the id!!!", db_id,matchid)
        for uid in matchid:
            print(users[uid])
        #exit()
        return users[matchid[0]]
#end get_user_from_id(db_id):
'''


def merge_users(userid1,userid2):
    global users
    global skip_keys
    global rewrite_keys
    for key in users[userid2].keys():
        allkeys=skip_keys
        allkeys.append('papers')
        if key not in allkeys:
            if key in rewrite_keys:
                rewritten_key=rewrite_keys[key]
            else:
                rewritten_key=key
            if rewritten_key in users[userid1].keys():                
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
                        if not rewritten_key+"_all" in users[userid1].keys():
                            #if type() is list:
                            users[userid1][rewritten_key+"_all"]=[]
                            users[userid1][rewritten_key+"_all"].append(users[userid1][rewritten_key])
                        if type(users[str(userid2)][key]) is list:
                            for entry in users[str(userid2)][key]:
                                users[userid1][rewritten_key+"_all"].append(entry)
                        else:
                            users[userid1][rewritten_key+"_all"].append(users[str(userid2)][key])
                        #users[str(userid1)][rewritten_key+"_all"]=list(set(users[str(userid1)][rewritten_key+"_all"]))

            else:
                users[userid1][rewritten_key]=users[str(userid2)][key]
    for paper in users[userid2]['papers']:
        users[userid1]['papers'].append(paper)
    users.pop(userid2)
#end merge_users(userid1,userid2):

def users_purity():
    #Change users emailHash as key with their real email address    
    global users
    global emailHashesDict
    print('Keys')
    print(users.keys())
    print('dict')
    print(emailHashesDict)
    #ukeys=copy.deepcopy(users.keys())
    ntot=0
    nemailHash=0
    nemailHashEmail=0
    nemailHashEmailDiff=0
    nemailHashEmailMulti=0
    nInDict=0
    ukeys=list(users.keys())
    for userid in ukeys:    
        ntot=ntot+1
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
                print("in dict")
                nInDict=nInDict+1

    print('*** Users files purity ***')
    print('Entries:',ntot)
    print('Entries not linked to repository',nemailHash)
    print('Entries not linked to repository but with email address',nemailHashEmail)
    print('Entries not linked to repository with different email address',nemailHashEmailDiff)
    print('Entries not linked to repository with multiple email address',nemailHashEmailMulti)
    print('Entries not linked to repository but in link dictionnary',nInDict)
    
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

'''
def clean_users():
    #Remove duplicate users in the list 
    global users
    emails=[]
    ide=[]
    for userid in users.keys():        
        for key in users[userid].keys():
            if key.endswith("_all"):
                print("key", key)
                print(users[userid][key])
                users[userid][key]=sorted(list(set(users[userid][key])))
        ide.append(userid)
        if 'email' in users[userid]:
            emails.append(users[userid]['email'])
        else:
            emails.append('')
        
    emails, ide = (list(t) for t in zip(*sorted(zip(emails, ide))))
    #print(ide)
    #print(emails)
    
    for iemail in range(1,len(emails)):
        if not emails[iemail]=='':
            if emails[iemail-1].lower()==emails[iemail].lower():
                print("** Two users with the same email **")
                print('--- ',ide[iemail-1])
                print(users[ide[iemail-1]])
                print('---',ide[iemail])
                print(users[ide[iemail]])
                merge_users(ide[iemail-1],ide[iemail])
                ide[iemail]=ide[iemail-1]

    emailhashes=[]
    idh=[]
    for userid in users.keys():        
        idh.append(userid)
        if 'emailHash' in users[userid]:
            emailhashes.append(users[userid]['emailHash'])
        else:
            emailhashes.append('')
        
    emailhashes, idh = (list(t) for t in zip(*sorted(zip(emailhashes, idh))))
    print(idh)
    #print(emails)
    
    for iemail in range(1,len(emailhashes)):
        if not emailhashes[iemail]=='' and not emailhashes[iemail]=='None':
            if emailhashes[iemail-1]==emailhashes[iemail]:
                print("** Two users with the same hash **")
                print(':::',idh[iemail],idh[iemail-1])
                print(users[idh[iemail-1]])
                print('---',idh[iemail])
                print(users[idh[iemail]])
                merge_users(idh[iemail-1],idh[iemail])
                idh[iemail]=idh[iemail-1]
#end clean_users():
'''
    
def get_email_hash(email):
    return md5(email.encode()).hexdigest()
