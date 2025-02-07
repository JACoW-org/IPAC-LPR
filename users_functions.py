#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:17:29 2025

User functions

@author: delerue
"""

import os
import joblib

#List of all known users
users_file="data/users_file.data"
affiliations_file="data/affiliations_file.data"
global skip_keys
skip_keys=[ 'affiliation_meta' , '_type' ,  '_fossil' ]
global rewrite_keys
#rewrite_keys={ 'id': 'db_id' }
rewrite_keys={  }
global users
global affiliations
def load_users():
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

def save_users():
    global users
    global affiliations

    joblib.dump(users,users_file)
    joblib.dump(affiliations,affiliations_file)

def add_paper_to_user(user_person_id,conf_id,paper_db_id,auth_type):
    global users
    if 'papers' not in users[str(user_person_id)].keys():
        users[str(user_person_id)]['papers']=[]
    #check if the paper is already in the list
    paperidx=-1
    for idx in range(len(users[str(user_person_id)]['papers'])):
        if str(users[str(user_person_id)]['papers'][idx][0])==str(conf_id) and str(users[str(user_person_id)]['papers'][idx][1])==str(paper_db_id):
            paperidx=idx
    if paperidx<0:
        users[str(user_person_id)]['papers'].append([conf_id,paper_db_id, [ auth_type ]])
    else:
        users[str(user_person_id)]['papers'][paperidx][2].append(auth_type)
        
def add_user_info(person_id,user_info,date=None):
    global users
    global affiliations
    global skip_keys
    global rewrite_keys
    if len(users)==0 or str(person_id) not in users.keys():
        users[str(person_id)]={ 'db_id' : str(person_id) }
    else:
        #print("User exists:", users[str(person_id)]['first_name'], users[str(person_id)]['last_name'], user_info['first_name'], user_info['last_name'])
        pass
    for key in user_info.keys():
        if key not in skip_keys:
            if key in rewrite_keys:
                rewritten_key=rewrite_keys[key]
            else:
                rewritten_key=key
            if rewritten_key in users[str(person_id)].keys():                
                if not str(users[str(person_id)][rewritten_key])==str(user_info[key]):
                    if not rewritten_key+"_all" in users[str(person_id)].keys():
                        users[str(person_id)][rewritten_key+"_all"]=[]
                        users[str(person_id)][rewritten_key+"_all"].append(users[str(person_id)][rewritten_key])
                    users[str(person_id)][rewritten_key+"_all"].append(str(user_info[key]))
            else:
                users[str(person_id)][rewritten_key]=str(user_info[key])
                
def get_user(db_id):
    print('In get_user(db_id)')
    global users
    if len(users)>0 and str(db_id) in users.keys():
        return users[str(db_id)]
    else:
        return None

def get_user_from_db_id(db_id):
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
        return None
    elif len(matchid)==1:
        return users[matchid[0]]
    else:
        print("More than one user match the db_id!!!", db_id,matchid)
        for uid in matchid:
            print(users[uid])
        #exit()
        return users[matchid[0]]
#end get_user_from_db_id(db_id):

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
            else:
                users[userid1][rewritten_key]=users[str(userid2)][key]
    for paper in users[userid2]['papers']:
        users[userid1]['papers'].append(paper)
    users.pop(userid2)
#end merge_users(userid1,userid2):

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