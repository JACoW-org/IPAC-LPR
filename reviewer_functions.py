#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  6 09:22:04 2025

Function to handle reviewers

@author: delerue
"""


import os,sys
#import joblib
#from hashlib import md5
import time

import requests

import params
import users_functions as uf
import indico_functions as indf


event_id = params.event_id

api_token = params.api_token
event_url=params.event_url


uf.load_users()

def get_reviewer_by_email(email):
    return get_reviewer_by_xx(email,'email')
    
def get_reviewer_dict_by_email(email):
    return get_reviewer_dict_by_xx(email,'email')
    
def get_reviewer_dict_by_id(reviewer_id):
    return get_reviewer_dict_by_xx(reviewer_id,'id')
    
def get_reviewer_by_id(reviewer_id):
    return get_reviewer_by_xx(reviewer_id,'id')
    
def get_reviewer_by_xx(val, typecol):
    ref_dict=get_reviewer_dict_by_xx(val, typecol)
    if ref_dict is not None:
        return ref_dict
    else:
        print("get_reviewer returned nothing for ",typecol," ", val)
        return None
        
    
def get_reviewer_dict_by_xx(val, typecol):

    ref_dict=None
        
    if typecol=='id':
        ref_dict=uf.get_user(val)
    else:
        print("get_reviewer_dict_by_xx not implemented for type ",typecol )
        sys.exit(255)
        
    if ref_dict is None:
        print("reviewer with id ", typecol , val ,  " was not found")
        return None
        exit()
    return ref_dict

        
def get_reviewer_db_id_from_id(reviewer_id):
    vals=get_reviewer_by_id(reviewer_id)
    print('The reviewer with id ',reviewer_id,' has email ',vals[1])
    return get_reviewer_db_id_from_email(vals[1])
    
def get_reviewer_db_id_from_email(email):
    reviewer_data=get_reviewer_info_from_email(email)    
    #print('reviewer_data',reviewer_data)
    #print("reviewer_data['id']",reviewer_data['id'])
    #print("reviewer_data['avatar_url']".reviewer_data['avatar_url'])
    if reviewer_data['id'] is not None:
        return reviewer_data['id']
    #elif reviewer_data['avatar_url'] is not None:
    #    print(reviewer_data['avatar_url'].split("/")[2])
    #    exit()
    else:
        print(reviewer_data)
        print("Unable to find reviewer id for ",email)
        exit()
          
def get_reviewer_info_from_email(email):
    headers = {'Authorization': f'Bearer {api_token}'}
    data = requests.get(f'https://indico.jacow.org/user/search/?email='+email, headers=headers)
    #print(data)
    #print(data.json()['users'][0])    
    return data.json()['users'][0]

def assign_reviewer(paper_db_id,reviewer_db_id):
    print("assigning reviewer", reviewer_db_id, " to paper ", paper_db_id)
    headers = {'Authorization': f'Bearer {api_token}'}
    payload = {'contribution_id': [ paper_db_id ], 'user_id': [ reviewer_db_id ] }
    data = requests.post(f'{event_url}manage/papers/assignment-list/assign/content_reviewer', headers=headers, data=payload)
    print(data)
    indf.comment_paper(paper_db_id, "Assigned reviewer "+str(reviewer_db_id), visibility="judges",api_token=params.api_token,meeting_id=params.event_id)
    
    if not (data.status_code == 200):
        print("Error code= ", data.status_code)
        exit()

def unassign_reviewer(paper_db_id,reviewer_db_id):
    #print("db_id received by unassign_reviewer", reviewer_db_id)
    #print("db_id received by unassign_reviewer", type(reviewer_db_id))
    reviewer_db_id=str(reviewer_db_id)
    headers = {'Authorization': f'Bearer {api_token}'}
    payload = {'contribution_id': [ paper_db_id ], 'user_id': [ reviewer_db_id ] }
    data = requests.post(f'{event_url}manage/papers/assignment-list/unassign/content_reviewer', headers=headers, data=payload)
    print(data)
    indf.comment_paper(paper_db_id, "Unassigned reviewer "+str(reviewer_db_id), visibility="judges",api_token=params.api_token,meeting_id=params.event_id)
    if not (data.status_code == 200):
        print("Error code= ", data.status_code)
        exit()
    #print("Check paper ", paper_id ," for reviewer unassigned")


def assign_reviewer_in_file(contrib,ref_id,ref_name,the_deadline):
    global papers_reviewer_assignation
    file = papers_reviewer_assignation
    wb_obj = openpyxl.load_workbook(file) 

    # Read the active sheet:
    reviewers_assignation_wb = wb_obj.active

    irow=1
    if not "Paper id" in reviewers_assignation_wb.cell(row=irow,column=1).value:
        print("Error checking ", file)
        exit()

    #Check where to enter new data
    irow=1
    while (reviewers_assignation_wb.cell(row=irow,column=1).value is not None):
        irow=irow+1
        #print("Checking row if is available", irow)
    
    reviewers_assignation_wb.cell(row=irow,column=1).value=contrib['id']
    reviewers_assignation_wb.cell(row=irow,column=2).value=contrib['title']
    reviewers_assignation_wb.cell(row=irow,column=3).value=ref_id
    reviewers_assignation_wb.cell(row=irow,column=4).value=ref_name
    reviewers_assignation_wb.cell(row=irow,column=5).value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reviewers_assignation_wb.cell(row=irow,column=6).value="Email request sent"
    reviewers_assignation_wb.cell(row=irow,column=7).value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reviewers_assignation_wb.cell(row=irow,column=8).value=the_deadline

    #reviewers_assignation_wb
    wb_obj.save(file)
    entry_code=str(((int(ref_id)*10000)+int(contrib['id']))*7)

    urlassign="http://nicolas.delerue.org/ipac23/assign.php?"
    urlassign=urlassign+urllib.parse.urlencode({'key': str(entry_code), 'title': contrib['title'], 'name' : ref_name })
    #print('url',urlassign)

    data = requests.get(urlassign)
    if not data.status_code == 200:
        print("Error submitting the assignememnt: wrong response code")
    else:
        #print(data.text)
        if not data.text[-2:] == "OK":
            print("Error submitting the assignememnt: wrong reply from server")
        
        urlform="http://nicolas.delerue.org/ipac23/reviewer_acceptance_form.php?id="+entry_code
        return urlform

def update_reviewer_in_file(contrib,ref_id,update_type):
    global papers_reviewer_assignation
    file = papers_reviewer_assignation
    wb_obj = openpyxl.load_workbook(file) 

    # Read the active sheet:
    reviewers_assignation_wb = wb_obj.active

    irow=1
    if not "Paper id" in reviewers_assignation_wb.cell(row=irow,column=1).value:
        print("Error checking ", file)
        exit()

    #Check where to enter new data
    irow=2
    while (reviewers_assignation_wb.cell(row=irow,column=1).value is not None) and not ((int(reviewers_assignation_wb.cell(row=irow,column=1).value) == int(contrib['id'])) and (int(reviewers_assignation_wb.cell(row=irow,column=3).value) == int(ref_id))):
        irow=irow+1
        #print("Checking row if is available", irow)

    if ((int(reviewers_assignation_wb.cell(row=irow,column=1).value) == int(contrib['id'])) and (int(reviewers_assignation_wb.cell(row=irow,column=3).value) == int(ref_id))):
        #record the update
        if update_type=='withdrawn':
            reviewers_assignation_wb.cell(row=irow,column=6).value="Withdrawn"
        else:
            print("Update not understood")
        reviewers_assignation_wb.cell(row=irow,column=7).value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #reviewers_assignation_wb
    wb_obj.save(file)

def get_reviewer_list():            
    headers = {'Authorization': f'Bearer {params.api_token}'}
    data = requests.get(f'{event_url}manage/papers/teams/', headers=headers)
    for line in data.text.split("\\n"):
        if 'id=\\"content_reviewers' in line:
            return line.replace("&#34;","").replace("User:","").split("[")[1].split("]")[0].split(",")
    return None



def add_user_as_reviewer(user):
        jnf.update_reviewer_map(participant['email'],participant['ref_id'])
        return participant
#def add_user_as_referee(user): 

