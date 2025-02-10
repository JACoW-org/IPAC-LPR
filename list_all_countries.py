#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 17:21:44 2025

@author: delerue
"""
import users_functions as uf
import params

uf.load_users()

#List all countries
all_countries=[]
unknown_countries=[]
for user in list(uf.users):
    user_data=uf.users[user]
    if 'country_code' in user_data.keys():
        print(user_data['country_code'],user_data['country_name'],uf.get_user_region(user_data['country_code']))
        all_countries.append(user_data['country_code'])
        if uf.get_user_region(user_data['country_code']) == params.REGION_UNKNOWN_CODE:
            unknown_countries.append(user_data['country_code'])               
print(list(set(all_countries)))
print(list(set(unknown_countries)))

