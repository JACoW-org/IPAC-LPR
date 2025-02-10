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
import params

parser = argparse.ArgumentParser()
parser.add_argument("--confid", help="The conference(s) id eg: 41 or 41,95")
parser.add_argument("--subMC", help="The subMC for which we want the map")
parser.add_argument("--check_reviewers", action="store_true", help="Check the sub MC of each reviewer")
parser.add_argument("--only_reviewers", action="store_true", help="Returns answers only for the members of the reviewers team")
parser.parse_args()
args = parser.parse_args()
#print(args)

if args.confid is None:
    args.confid=str(params.event_id)


if (args.confid.find(",")>0):
    confids=args.confid.split(",")
else:
    confids=[args.confid ]    

uf.load_users()

if args.check_reviewers or args.only_reviewers :
    #print("Checking reviewers...")
    reflist=jnf.get_referees_list()
    #for each reviewer we check that s/he is know
    for refid in reflist:
        refdata=uf.get_user(refid)
        if refdata is None:
            print("Downloading info on reviewer ", refid)
            refnewdata=uf.search_user_by_id(refid)
            if refnewdata is not None:
                uf.add_user_info(refid, refnewdata)
                uf.save_users()
    #print("Checked")

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
                    thekey='person_id'
                elif auth_type=='speakers' :
                    all_authors=all_authors_by_sub_MC_speakers[idx]
                    thekey='person_id'
                elif auth_type=='coauthors' :
                    all_authors=all_authors_by_sub_MC_coauthors[idx]
                    thekey='person_id'
                elif auth_type=='submitter' :
                    all_authors=all_authors_by_sub_MC_submitters[idx]
                    thekey='id'
                    
                for author in all_authors :
                    auth_data=uf.get_user(author)
                    showdata=True
                    if auth_data is None:
                        print("Author ",author,"returned None!")
                        auth_data=uf.get_user(author)
                        print(auth_data)
                        exit()
                        showdata=False
                    if auth_data is not None:
                        if args.only_reviewers:
                            showdata=False
                            #print("thekey",thekey)
                            if thekey in auth_data.keys():
                                if auth_data[thekey] in reflist:
                                    showdata=True
                                if thekey+'_all' in auth_data.keys():
                                    for dbid in auth_data[thekey+'_all']:
                                        if dbid in reflist:
                                            showdata=True
                    if showdata:
                        #print(auth_data)
                        print(auth_type,auth_data['first_name'],auth_data['last_name'],' ',end='') 
                        if 'email' in auth_data.keys():
                            print(auth_data['email'],' ',end='')
                        if 'country_code' in auth_data.keys():
                            print(auth_data['country_code'],' ',end='')
                        print()
                        #print("Papers", auth_data['papers'])
    elif args.check_reviewers:
        for theref in reflist:
            auth_data=uf.get_user_from_db_id(theref)
            if auth_data is None:
                print("No entry for db_id",theref)
            else:
                if 'email' in auth_data.keys():
                    print(theref,auth_data['first_name'],auth_data['last_name'],auth_data['email'])
                else:
                    print(theref,auth_data['first_name'],auth_data['last_name'])
                for auth_type in ['primaryauthors' , 'speakers' , 'coauthors' , 'submitter' ]:
                    auth_MC=[]
                    for idx in range(len(the_sub_MC_list)):
                        if auth_type=='primaryauthors' :
                            all_authors=all_authors_by_sub_MC[idx]
                            thekey='person_id'
                        elif auth_type=='speakers' :
                            all_authors=all_authors_by_sub_MC_speakers[idx]
                            thekey='person_id'
                        elif auth_type=='coauthors' :
                            all_authors=all_authors_by_sub_MC_coauthors[idx]
                            thekey='person_id'
                        elif auth_type=='submitter' :
                            all_authors=all_authors_by_sub_MC_submitters[idx]
                            thekey="id"
                        if thekey in auth_data.keys():
                            if str(auth_data[thekey]) in str(all_authors):
                                auth_MC.append(the_sub_MC_list[idx])
                            if thekey+'_all' in auth_data.keys():
                                for dbid in auth_data[thekey+'_all']:
                                    if str(dbid) in str(all_authors):
                                        auth_MC.append(the_sub_MC_list[idx])
                    if len(auth_MC)>0:
                        auth_MC=sorted(list(set(auth_MC)))
                        print("   ",auth_type,auth_MC)                        
    if idx<0:
        print("Sub MC's available:", sorted(the_sub_MC_list))
        
        