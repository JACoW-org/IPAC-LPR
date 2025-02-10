#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 14:26:36 2025

Finds info about a user

@author: delerue
"""

#import jacow_nd_func as jnf
import argparse
import users_functions as uf
import jacow_nd_func as jnf


parser = argparse.ArgumentParser()
parser.add_argument("--user_id", help="The user_id of the user")
parser.add_argument("--last_name", help="The last name of the user")
parser.add_argument("--first_name", help="The first name of the user")
parser.add_argument("--email", help="The email address of the user")
parser.parse_args()
args = parser.parse_args()
#print(args)


uf.load_users()

nmatch=0
for user in list(uf.users):
    user_data=uf.users[user]
    match=True
    #print('user',user,user_data)
    if args.user_id is not None:
        if not str(user_data['user_id'])==str(args.db_id):
            if 'user_id_all' in user_data.keys():
                if not str(args.db_id) in user_data['user_id_all']:
                    match=False
            else:
                match=False
            
    if args.last_name is not None:
        if 'last_name' in user_data.keys() :
            if not user_data['last_name'].lower()==args.last_name.lower():
                match=False
        else:
            match=False
    if args.first_name is not None and 'first_name' in user_data.keys() :
        if not user_data['first_name'].lower()==args.first_name.lower():
            match=False
    if args.email is not None:
        if 'email' in user_data.keys() :
            if not user_data['email'].lower()==args.email.lower():
                match=False
        else:
            match=False
            
    if match:
        print("*** User match")
        if 'user_id' in user_data.keys() and 'emailHash' in user_data.keys():
            if user_data['user_id'] == user_data['emailHash']:
                print("Matching user is not linked to repository. Checking repository for updates.")
                uf.search_user_id(user_data)
        ordered_keys= [ 'user_id', 'title', 'first_name', 'last_name', 'full_name', 'affiliation', 'email', 'country_code', 'country_name']
        for key in user_data:
            if key not in ordered_keys:
                ordered_keys.append(key)
        for key in ordered_keys:
            if key in user_data.keys():
                if key not in [ 'papers']:
                    if not key.endswith("_all"):
                        print("  ", key,user_data[key])
                        if key+"_all" in user_data.keys(): 
                            print("      all:",user_data[key+"_all"])
        if 'papers' in user_data.keys():
            for paper in user_data['papers']:
                conf=paper[0].replace('41','IPAC23').replace('63','IPAC24').replace('91','IPAC25').replace('95','IPAC26')
                print("   Paper: conf",conf," id:",paper[1]," role:",paper[2])
        print('=====')
        nmatch=nmatch+1
print(nmatch,"users matched out of",len(uf.users))

if nmatch==0:
    print(args.email)
    if args.email is not None:
        print("jnf.email",args.email)
        json_data=jnf.search_user(email=args.email)
        print(json_data)
        print(uf.get_email_hash(args.email))
    elif args.last_name is not None:
        print(jnf.search_user(last_name=args.last_name))
