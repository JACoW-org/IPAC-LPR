#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 12:53:22 2025

Reads the map of authors by MC for a given conference

@author: delerue
"""


import jacow_nd_func as jnf
import argparse
#import numpy as np
import joblib
import users_functions as uf


parser = argparse.ArgumentParser()
parser.add_argument("--confid", help="The conference(s) id eg: 41 or 41,95")
parser.add_argument("--subMC", help="The subMC for which we want the map")
parser.add_argument("--check_reviewers", action="store_true", help="Check the sub MC of each reviewer")
parser.add_argument("--only_reviewers", action="store_true", help="Returns answers only for the members of the reviewers team")
parser.parse_args()
args = parser.parse_args()
#print(args)

if args.confid is None:
    args.confid=str(jnf.event_id)


if (args.confid.find(",")>0):
    confids=args.confid.split(",")
else:
    confids=[args.confid ]    


if args.check_reviewers or args.only_reviewers :
    reflist=jnf.get_referees_list()

uf.load_users()

for confid in confids:
    authors_map_fname=f'data/all_authors_by_subMC_for_conf_{confid}.data'
    [the_sub_MC_list,all_authors_by_sub_MC,all_authors_by_sub_MC_speakers,all_authors_by_sub_MC_coauthors,all_authors_by_sub_MC_submitters]=joblib.load(authors_map_fname)

    idx=-1    
    if args.subMC is not None:
        idx=the_sub_MC_list.index(args.subMC)
        if idx<0:
            print("Sub MC not found")
        else:
            for auth_type in ['primaryauthors' , 'speakers' , 'coauthors' , 'submitter' ]:
                if auth_type=='primaryauthors' :
                    all_authors=all_authors_by_sub_MC[idx]
                elif auth_type=='speakers' :
                    all_authors=all_authors_by_sub_MC_speakers[idx]
                elif auth_type=='coauthors' :
                    all_authors=all_authors_by_sub_MC_coauthors[idx]
                elif auth_type=='submitter' :
                    all_authors=all_authors_by_sub_MC_submitters[idx]
                    
                for author in all_authors :
                    auth_data=uf.get_user_from_db_id(author)
                    showdata=True
                    if args.only_reviewers:
                        showdata=False
                        if auth_data['db_id'] in reflist:
                            showdata=True
                        if 'db_id_all' in auth_data.keys():
                            for dbid in auth_data['db_id_all']:
                                if dbid in reflist:
                                    showdata=True
                    if showdata:
                        if 'email' in auth_data.keys():
                            print(auth_type,auth_data['first_name'],auth_data['last_name'],auth_data['email'])
                        else:
                            print(auth_type,auth_data['first_name'],auth_data['last_name'])
                        #print("Papers", auth_data['papers'])
    elif args.check_reviewers:
        for theref in reflist:
            auth_data=uf.get_user_from_db_id(theref)
            if auth_data is None:
                print("No entry for db_id",theref)
            else:
                if 'email' in auth_data.keys():
                    print(auth_data['first_name'],auth_data['last_name'],auth_data['email'])
                else:
                    print(auth_data['first_name'],auth_data['last_name'])
                for auth_type in ['primaryauthors' , 'speakers' , 'coauthors' , 'submitter' ]:
                    auth_MC=[]
                    for idx in range(len(the_sub_MC_list)):
                        if auth_type=='primaryauthors' :
                            all_authors=all_authors_by_sub_MC[idx]
                        elif auth_type=='speakers' :
                            all_authors=all_authors_by_sub_MC_speakers[idx]
                        elif auth_type=='coauthors' :
                            all_authors=all_authors_by_sub_MC_coauthors[idx]
                        elif auth_type=='submitter' :
                            all_authors=all_authors_by_sub_MC_submitters[idx]
                        if str(auth_data['db_id']) in str(all_authors):
                            auth_MC.append(the_sub_MC_list[idx])
                        if 'db_id_all' in auth_data.keys():
                            for dbid in auth_data['db_id_all']:
                                if str(dbid) in str(all_authors):
                                    auth_MC.append(the_sub_MC_list[idx])
                    if len(auth_MC)>0:
                        auth_MC=sorted(list(set(auth_MC)))
                        print("   ",auth_type,auth_MC)                        
    if idx<0:
        print("Sub MC's available:", sorted(the_sub_MC_list))
        
        