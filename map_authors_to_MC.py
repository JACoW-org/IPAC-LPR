#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 12:07:23 2025

Creates a map of all the authors, speakers and co-authors by subMC for he given conference(s) 

@author: delerue
"""

import jacow_nd_func as jnf
import argparse
#import numpy as np
import joblib
import users_functions as uf


parser = argparse.ArgumentParser()
parser.add_argument("--confid", help="The conference(s) id eg: 41 or 41,95")
parser.parse_args()
args = parser.parse_args()
#print(args)

if args.confid is None:
    args.confid=jnf.event_id


if (args.confid.find(",")>0):
    confids=args.confid.split(",")
else:
    confids=[args.confid ]    

uf.load_users()

for confid in confids:

    authors_map_fname=f'data/all_authors_by_subMC_for_conf_{confid}.data'
    
    json_contribs=jnf.load_contribs(confid)
    print("Loading contribution from conf id",confid,":", json_contribs["results"][0]["title"])
    the_sub_MC_list=[]
    all_authors_by_sub_MC=[]
    all_authors_by_sub_MC_speakers=[]
    all_authors_by_sub_MC_coauthors=[]
    all_authors_by_sub_MC_submitters=[]
    contribs=jnf.submitted_contribs(confid)
    for contrib in json_contribs["results"][0]['contributions']:
        if (contrib['track'] is not None):
            spacePos=contrib['track'][0:7].find(' ')
            if spacePos>0:
                subTrackName=contrib['track'][0:spacePos]
            else: 
                subTrackName=contrib['track'][0:7]
            if not subTrackName in the_sub_MC_list:
                #print("Adding",subTrackName)
                the_sub_MC_list.append(subTrackName)
                all_authors_by_sub_MC.append([])
                all_authors_by_sub_MC_submitters.append([])
                all_authors_by_sub_MC_coauthors.append([])
                all_authors_by_sub_MC_speakers.append([])
                #print(the_sub_MC_list)
            idx=the_sub_MC_list.index(subTrackName)
            #print('Contrib id',contrib['id'],' db_id',contrib['db_id'])
            the_paper=jnf.get_paper_info(str(contrib['db_id']),use_cache=True)
            if (the_paper is not None):
                #print(the_paper['last_revision']['submitter'])
                #print(the_paper['last_revision']['submitter']['id'])
                #exit()
                uf.add_user_info("s"+str(the_paper['last_revision']['submitter']['id']),the_paper['last_revision']['submitter'])
                uf.add_paper_to_user("s"+str(the_paper['last_revision']['submitter']['id']),confid,str(contrib['db_id']),"submitter")
                all_authors_by_sub_MC_submitters[idx].append("s"+str(the_paper['last_revision']['submitter']['id']))               
            for auth_type in ['speakers' , 'primaryauthors' ,'coauthors' ]:
                for speak in contrib[auth_type]:
                    #print('speak',speak)
                    speak_name=speak['first_name']+" "+speak['last_name']
                    #print('\tSpeak name:',speak_name)
                    uf.add_user_info(speak['person_id'],speak)
                    uf.add_paper_to_user(speak['person_id'],confid,str(contrib['db_id']),auth_type)
                    if auth_type == 'coauthors': 
                        all_authors_by_sub_MC_coauthors[idx].append(speak['person_id'])
                    elif auth_type == 'speakers': 
                        all_authors_by_sub_MC_speakers[idx].append(speak['person_id'])
                    else:
                        all_authors_by_sub_MC[idx].append(speak['person_id'])
    for subMC in the_sub_MC_list:
        idx=the_sub_MC_list.index(subMC)
        #print(subMC,idx)
        #print(all_authors_by_sub_MC[idx])
        #print(list(set(all_authors_by_sub_MC[idx])))
        #print(list(set(all_authors_by_sub_MC_coauthors[idx])))
        all_authors_by_sub_MC[idx]=list(set(all_authors_by_sub_MC[idx]))
        all_authors_by_sub_MC_speakers[idx]=list(set(all_authors_by_sub_MC_speakers[idx]))
        all_authors_by_sub_MC_submitters[idx]=list(set(all_authors_by_sub_MC_submitters[idx]))
        all_authors_by_sub_MC_coauthors[idx]=list(set(all_authors_by_sub_MC_coauthors[idx]))
    print("**** MC map: *****")
    print('the_sub_MC_list')
    print(the_sub_MC_list)
    print('all_authors_by_sub_MC')
    print(all_authors_by_sub_MC)
    joblib.dump([the_sub_MC_list,all_authors_by_sub_MC,all_authors_by_sub_MC_speakers,all_authors_by_sub_MC_coauthors,all_authors_by_sub_MC_submitters],authors_map_fname)
uf.clean_users()
uf.save_users()
