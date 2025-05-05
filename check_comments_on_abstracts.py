#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 16:40:34 2025

Checks comments on abstracts

@author: delerue
"""

import params

#import sys
#import json
#import requests,json
from datetime import datetime
#import matplotlib.pyplot as plt
#import numpy as np

#sys.path.append('../jacow-ipac-lpr/')
import users_functions as uf
#import jacow_nd_func as jnf
#import papers_functions as pf
import indico_functions as indf

headers = {'Authorization': f'Bearer {params.api_token}'}

qa_table_header="sort-table_header_generic.html"
qa_table_dict={ "Title":"IPAC'26 invited orals Quality Assessment" , "table_id": "quality_assessment"}
#qa_table_heads=[ "id" , "friendly_id" , "MC", "speaker_name", "submitter_email" , "title" , "url",  "qa_issues" ]
qa_table_heads=[ "id" , "friendly_id" , "state", "MC", "title" , "user", "url",  "date" , "proposed_action",  "comment" , "id_date" ]

qa_page_filename="abstracts_mcqa.html"


data = indf.indico_get(f'{params.event_url}/manage/abstracts/abstracts.json',datatype='json',headers=headers)
#print(data.text)
#print(data.json().keys())

'''
if 1==0:
    print(len(data['abstracts']))
    iabstract=53
    print(data['abstracts'][iabstract]['id'])
    print(data['abstracts'][iabstract]['friendly_id'])
    #print(data['abstracts'][iabstract]['submitter'])
    print(data['abstracts'][iabstract].keys())
    print(data['abstracts'][iabstract]['comments'])
    print(len(data['abstracts'][iabstract]['comments']))
'''

date_format = "%Y-%m-%d"
last_check="2025-03-26"
date_checked = datetime.strptime(last_check, date_format)

ncomments=1

comments_per_person={}

heads_txt=""
for head in qa_table_heads:
    heads_txt=heads_txt+"<th>\n<button>\n"+head+"<span aria-hidden=\"true\"></span>\n</button>\n</th>\n"
qa_table_dict["col_heads"]=heads_txt

qa_page=open(qa_page_filename,"w")
opr=open(qa_table_header,"r")
for line in opr:
    for key in qa_table_dict.keys():
        #print(key,"%%"+key+"%%",line.find(key),line.find("%%"+key+"%%"),line)
        line=line.replace("%%"+key+"%%",qa_table_dict[key])
        #print(line)
    qa_page.write(line)
opr.close()

skip_qa_issues_on_abstracts=[]

print("Checking comments")
for abstract in data['abstracts']:
    #print(abstract.keys())
    if (len(abstract['comments'])>0) and not int(abstract['id']) in skip_qa_issues_on_abstracts:
        first_comment=True
        for comment in abstract['comments']:
            if not comment['user']['full_name'] in comments_per_person:
                comments_per_person[comment['user']['full_name']]={}
                comments_per_person[comment['user']['full_name']]['n_comments']=0
                comments_per_person[comment['user']['full_name']]['id']=comment['user']['id']
            comments_per_person[comment['user']['full_name']]['n_comments']=comments_per_person[comment['user']['full_name']]['n_comments']+1
            if not abstract['state'] in [ 'duplicate' ,'withdrawn' , 'rejected' ]:
                date_submitted = datetime.strptime(comment['created_dt'][0:10], date_format)
                if (date_submitted>date_checked):
                    if first_comment:
                        print("Comment ",ncomments,"id",abstract['id'],abstract['friendly_id'],abstract['submitted_for_tracks'][0]['title'][0:3],abstract['state'],f"{params.event_url}abstracts/{abstract['id']}/")
                        first_comment=False
                    theroles=uf.has_role_codes(userid=comment['user']['id'])
                    print("    user:",comment['user']['id'],comment['user']['full_name'],theroles)
                    print("    text:",comment['text'])
                    print("    date:",comment['created_dt'][0:20])
                    ncomments=ncomments+1
                    #print(comment.keys())
                    #print(comment['user'].keys())
                    print("   ")
                    if len(comment['text'])>0:
                        qa_page.write(f"<tr id=\"{abstract['id']}\">")        
                        for head in qa_table_heads:            
                             qa_page.write("<td>\n")
                             if head=="user":
                                 qa_page.write(str(comment['user']['full_name'])+" "+str(theroles))
                             elif head=="url":
                                 abstract_url=f"{params.event_url}abstracts/{abstract['id']}"
                                 abstract['url']=abstract_url
                                 qa_page.write("<A HREF='"+str(abstract[head])+"'>"+str(abstract[head])+"</A>")
                             elif head=="id_date":
                                 qa_page.write(str(abstract['id'])+" "+str(comment['created_dt'][0:20]))
                             elif head=="date":
                                 qa_page.write(str(comment['created_dt'][0:20]))
                             elif head=="MC":
                                qa_page.write(abstract['submitted_for_tracks'][0]['title'][0:3])
                             elif head=="comment":
                                 qa_page.write(str(comment['text']))
                             elif head=="proposed_action":
                                 qa_page.write(" ")
                             else:
                                 if head in abstract.keys():
                                     qa_page.write(str(abstract[head]))
                                 else:
                                     qa_page.write(str(comment[head]))                                    
                             qa_page.write("</td>\n")
                        qa_page.write("</tr>\n")
    
        if (len(abstract['reviews'])>0):
            first_comment=True
            for comment in abstract['reviews']:
                if not comment['user']['full_name'] in comments_per_person:
                    comments_per_person[comment['user']['full_name']]={}
                    comments_per_person[comment['user']['full_name']]['n_comments']=0
                    comments_per_person[comment['user']['full_name']]['id']=comment['user']['id']
                comments_per_person[comment['user']['full_name']]['n_comments']=comments_per_person[comment['user']['full_name']]['n_comments']+1
                if not abstract['state'] in [ 'duplicate' ,'withdrawn' , 'rejected' ]:
                    date_submitted = datetime.strptime(comment['created_dt'][0:10], date_format)                
                    if (date_submitted>date_checked):
                        #print(comment.keys())
                        if first_comment:
                            print("Review ",ncomments,"id",abstract['id'],abstract['friendly_id'],abstract['submitted_for_tracks'][0]['title'][0:3],abstract['state'],f"{params.event_url}abstracts/{abstract['id']}/")
                            first_comment=False
                        theroles=uf.has_role_codes(userid=comment['user']['id'])
                        print("    user:",comment['user']['id'],comment['user']['full_name'],theroles)
                        print("    action:",comment['proposed_action'])
                        print("    text:",comment['comment'])
                        print("    date:",comment['created_dt'][0:20])
                        ncomments=ncomments+1
                        #print(comment)
                        #print(comment['user'].keys())
                        print("   ")

                        if len(comment['comment'])>0 or not comment["proposed_action"]=="accept":
                            qa_page.write(f"<tr id=\"{abstract['id']}\">")        
                            for head in qa_table_heads:            
                                 qa_page.write("<td>\n")
                                 if head=="user":
                                     qa_page.write(str(comment['user']['full_name'])+" "+str(theroles))
                                 elif head=="url":
                                     abstract_url=f"{params.event_url}abstracts/{abstract['id']}"
                                     abstract['url']=abstract_url
                                     qa_page.write("<A HREF='"+str(abstract[head])+"'>"+str(abstract[head])+"</A>")
                                 elif head=="id_date":
                                     qa_page.write(str(abstract['id'])+" "+str(comment['created_dt'][0:20]))
                                 elif head=="date":
                                     qa_page.write(str(comment['created_dt'][0:20]))
                                 elif head=="MC":
                                    qa_page.write(abstract['submitted_for_tracks'][0]['title'][0:3])
                                 else:
                                     if head in abstract.keys():
                                         qa_page.write(str(abstract[head]))
                                     else:
                                         qa_page.write(str(comment[head]))                                    
                                 qa_page.write("</td>\n")
                            qa_page.write("</tr>\n")

qa_page.write("</table>")
qa_page.close()

for key in comments_per_person.keys():
    theroles=uf.has_role_codes(userid=comments_per_person[key]['id'])
    print(key, comments_per_person[key]['n_comments'] , theroles)
#print(comments_per_person)