#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 12:07:23 2025

Creates a map of all the authors, speakers and co-authors by subMC for he given conference(s) 

@author: delerue
"""

import params
import jacow_nd_func as jnf
import argparse,sys
#import numpy as np
import joblib
import users_functions as uf
import papers_functions as pf

#import time

parser = argparse.ArgumentParser()
parser.add_argument("--confid", help="The conference(s) id eg: 41 or 41,63,81,95")
parser.add_argument("--create-orals-page", action="store_true",  help="If this option is set will create an HTML page with all orales at the selected conferences.")
parser.parse_args()
args = parser.parse_args()
#print(args)

orals_page_name="IPAC_past_orals.html"
orals_page_header="sort-table_header.html"
orals_page_footer="sort-table_footer.html"

if args.confid is None:
    args.confid=str(params.event_id)

if (args.confid.find(",")>0):
    confids=args.confid.split(",")
else:
    confids=[args.confid ]    

uf.load_users()
all_oral_speakers=[]

for confid in confids:

    authors_map_fname=f'data/all_authors_by_subMC_for_conf_{confid}.data'
    #print(len(json_contribs["results"]))
    the_sub_MC_list=[]
    all_authors_by_sub_MC=[]
    all_authors_by_sub_MC_speakers=[]
    all_authors_by_sub_MC_coauthors=[]
    all_authors_by_sub_MC_submitters=[]
    #contribs=jnf.submitted_contribs(confid)
    contribs=jnf.load_contribs(confid)
    print("Loading contribution from conf id",confid,":", contribs["results"][0]["title"])
    for contrib in contribs["results"][0]['contributions']:
        print(".",end='')       
        sys.stdout.flush()
        keep_contrib=True
        if (contrib['track'] is None):
            if contrib['type'] == 'Invited Oral Presentation':
                contrib['track']='MC0.00'
            elif contrib['type'] == 'Special (Award) Presentation' or contrib['type'] == 'Poster Presentation':
                keep_contrib=False
            elif contrib['type']==None:
                #Some contributions witout type or track exist in indico...
                #We ignore them
                keep_contrib=False
            else:
                print(contrib)
                print(contrib['track'])
                print(contrib['type'])
                print(contrib['speakers'][0]['first_name'])
                print(contrib['speakers'][0]['last_name'])
                print("Contrib without track nor type")                
                keep_contrib=False
                exit()
        if keep_contrib:
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
            the_paper=pf.get_paper_info(str(contrib['db_id']),event_id=confid,use_cache=True,file_age_to_renew=-1)
            if (the_paper is not None):
                #print(the_paper['last_revision']['submitter'])
                #print(the_paper['last_revision']['submitter']['id'])
                #exit()
                uf.add_user_info(str(the_paper['last_revision']['submitter']['id']),the_paper['last_revision']['submitter'])
                uf.add_paper_to_user(str(the_paper['last_revision']['submitter']['id']),confid,str(contrib['db_id']),"submitter")
                all_authors_by_sub_MC_submitters[idx].append(str(the_paper['last_revision']['submitter']['id']))   
                #if (the_paper['last_revision']['submitter']['last_name']).lower()=='delerue':
                    #print("sub:", the_paper['last_revision']['submitter'],the_paper['last_revision']['submitter'].keys(),"subm")
                    #else:
                    #print("sub name: ", the_paper['last_revision']['submitter']['last_name'])                      
            the_contrib=pf.get_contrib_info(str(contrib['db_id']),event_id=confid,use_cache=True,file_age_to_renew=-1)
            if (the_contrib is not None):
                for theperson in the_contrib['persons']:
                    if 'email_hash' in theperson.keys() and theperson['email_hash'] is not None and len(theperson['email_hash'])>3:
                        userid=uf.get_user_id(theperson['email_hash'])
                        uf.add_user_info(userid,theperson)
                        if theperson['is_speaker']:
                            uf.add_paper_to_user(userid,confid,str(contrib['db_id']),'speakers')
                            all_authors_by_sub_MC_speakers[idx].append(userid)
                            if 'oral' in  the_contrib['type']['name'].lower():
                                all_oral_speakers.append({ 'user_id': userid , 'contrib_id': str(contrib['db_id'])  , "conf_id": confid })                        
                        if theperson['author_type']=='primary':
                            auth_type='primaryauthors'
                        elif theperson['author_type']=='secondary':
                            auth_type='coauthors'
                        elif theperson['author_type'] is None or theperson['author_type']=='none':
                            auth_type=None
                        else:
                            print("theperson['author_type']", theperson['author_type'],": case unknown in the map")
                            print(theperson)
                            exit()
                        if auth_type is not None:
                            uf.add_paper_to_user(userid,confid,str(contrib['db_id']),auth_type)
                            if auth_type == 'coauthors': 
                                all_authors_by_sub_MC_coauthors[idx].append(userid)
                            elif auth_type == 'speakers': 
                                all_authors_by_sub_MC_speakers[idx].append(userid)
                            else:
                                all_authors_by_sub_MC[idx].append(userid)

            for auth_type in ['speakers' , 'primaryauthors' ,'coauthors' ]:
                for speak in contrib[auth_type]:
                    #print('speak',speak)
                    #speak_name=speak['first_name']+" "+speak['last_name']
                    #print('\tSpeak name:',speak_name)
                    if 'email_hash' in speak.keys() and speak['email_hash'] is not None and len(speak['email_hash'])>3:
                        userid=uf.get_user_id(speak['emailHash'])
                        uf.add_user_info(userid,speak)
                        uf.add_paper_to_user(userid,confid,str(contrib['db_id']),auth_type)
                        if auth_type == 'coauthors': 
                            all_authors_by_sub_MC_coauthors[idx].append(userid)
                        elif auth_type == 'speakers': 
                            all_authors_by_sub_MC_speakers[idx].append(userid)
                            if 'oral' in  contrib['type']['name'].lower():                            
                                all_oral_speakers.append({ 'user_id': userid , 'contrib_id': str(contrib['db_id']) , "conf_id": confid})                        
                        else:
                            all_authors_by_sub_MC[idx].append(userid)
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
    print("\n**** MC map: *****")
    print('the_sub_MC_list')
    print(the_sub_MC_list)
    #print('all_authors_by_sub_MC')
    #print(all_authors_by_sub_MC)
    joblib.dump([the_sub_MC_list,all_authors_by_sub_MC,all_authors_by_sub_MC_speakers,all_authors_by_sub_MC_coauthors,all_authors_by_sub_MC_submitters],authors_map_fname)
#Adding reviewers to database
reflist=jnf.get_referees_list()
uf.search_and_add_users_by_id(reflist)
uf.save_users()
uf.clean_users()
uf.users_purity()
uf.save_users()

if args.create_orals_page:
    print(" *** Creating orals page. ***")
    print(len(all_oral_speakers)," speakers found.")

    oral_page=open(orals_page_name,"w")
    opr=open(orals_page_header,"r")
    for line in opr:
        oral_page.write(line)
    opr.close()
    #check for duplicates
    print("Checking for duplicate speakers")
    for ispeaker in range(len(all_oral_speakers)):
        for jspeaker in range(0,ispeaker):
            #print(ispeaker,jspeaker,all_oral_speakers[ispeaker]['contrib_id'],all_oral_speakers[jspeaker]['contrib_id'],all_oral_speakers[ispeaker]['user_id'],all_oral_speakers[jspeaker]['user_id'])
            if all_oral_speakers[ispeaker]==all_oral_speakers[jspeaker]:
                print("duplicate 1")
                exit()
            if all_oral_speakers[ispeaker]['contrib_id']==all_oral_speakers[jspeaker]['contrib_id']:
                if all_oral_speakers[ispeaker]['user_id']==all_oral_speakers[jspeaker]['user_id']:
                    print("duplicate 2")
                    exit()
    print("Checked for duplicate speakers")
                    
    for speaker in all_oral_speakers:
        #print("Speaker",speaker)
        speaker_data=uf.find_user(user_id=speaker['user_id'])
        if len(speaker_data)==1:
            speaker_data=speaker_data[0]
        else:
            print("Speaker data not understood",speaker_data)
            exit()
        #print(speaker_data["first_name"],speaker_data["last_name"])
        the_contrib=pf.get_contrib_info(speaker['contrib_id'],event_id=confid,use_cache=True,file_age_to_renew=-1)
        #print(the_contrib)
        if type(the_contrib["type"]) is dict:
            contrib_type=the_contrib["type"]['name']
        if the_contrib["track"] is None:
            contrib_track="MC0.00"
        elif type(the_contrib["track"]) is dict:
            if len(the_contrib["track"]['code'])>2:
                contrib_track=the_contrib["track"]['code']
            elif len(the_contrib["track"]['title'])>2:
                contrib_track=the_contrib["track"]["title"][0:7]
            else:
                print(the_contrib["track"])
                exit()
        contrib_url="<A HREF='https://indico.jacow.org/event/"+speaker['conf_id']+"/contributions/"+speaker['contrib_id']+"/'>"+speaker['contrib_id']+"</A>"
        speaker_found=False
        for person in the_contrib['persons']:
            #print(person['is_speaker'])
            if person['is_speaker']:
                print("***", speaker['contrib_id'], person['last_name'],speaker_data['last_name'])
                if person['last_name']==speaker_data['last_name']:
                    if speaker_found:
                        print("Multiple speakers found")
                    oral_page.write('<tr style="border: 1px solid black;" >\n')                
                    for txt in [ person["first_name"],person["last_name"],person["affiliation"],contrib_track,contrib_type,the_contrib["title"],pf.get_conf_from_id(speaker['conf_id']) , contrib_url ]:
                        print(txt,end=' ')
                        oral_page.write('<td style="border: 1px solid black;">\n')
                        oral_page.write(txt+"\n")
                        oral_page.write("</td>\n")
                    oral_page.write("</tr>\n")
                    speaker_found=True

    opf=open(orals_page_footer,"r")
    for line in opf:
        oral_page.write(line)
    opf.close()
    oral_page.close()
        
