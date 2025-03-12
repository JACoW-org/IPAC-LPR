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
#parser.add_argument("--show_affiliation", action="store_true",  help="Show the full affiliation")
parser.add_argument("--force_search", action="store_true",  help="Force a query to the indico.jacow database.")
parser.parse_args()
args = parser.parse_args()
#print(args)

user_data=uf.find_user(user_id=args.user_id,last_name=args.last_name,first_name=args.first_name,email=args.email,verbose=True,force_search=args.force_search)
