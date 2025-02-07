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

parser = argparse.ArgumentParser()
parser.add_argument("--db_id", help="The db_id of the user")
parser.add_argument("--last_name", help="The last name of the user")
parser.add_argument("--first_name", help="The first name of the user")
parser.parse_args()
args = parser.parse_args()
#print(args)


uf.load_users()

nmatch=0
for user in uf.users:
    user_data=uf.users[user]
    match=True
    #print('user',user,user_data)
    if args.db_id is not None:
        if not str(user_data['db_id'])==str(args.db_id):
            if 'db_id_all' in user_data.keys():
                if not str(args.db_id) in user_data['db_id_all']:
                    match=False
            else:
                match=False
            
    if args.last_name is not None and 'last_name' in user_data.keys() :
        if not user_data['last_name'].lower()==args.last_name.lower():
            match=False
    if args.first_name is not None and 'first_name' in user_data.keys() :
        if not user_data['first_name'].lower()==args.first_name.lower():
            match=False
    if match:
        print("User match",user_data)
        nmatch=nmatch+1
print(nmatch,"users matched out of",len(uf.users))
