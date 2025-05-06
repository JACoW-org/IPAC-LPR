#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 21:54:43 2025

Parameters for the IPAC Light Peer Review

@author: delerue
"""

import sys


### It is advised to override the following parameters in a file called myparams.py
#Settings
event_id = 95

email_from_address="peer-review@ipac23.org"
email_from_txt="IPAC LPR - Nicolas Delerue <"+email_from_address+">"
email_smtp_server='zrelay.in2p3.fr'


### The parameters below are less likely to change but can be changed.


#Number of days to review paper
days_to_review_paper=5


#List of all known users and their affiliation
users_file="data/users_file.data"
affiliations_file="data/affiliations_file.data"

#Maximum number of user search queries in a run
maxUserSearch=200

#Time interval to relaod the contributions
reload_contrib_from_online_seconds=5*24*60*60


#regions
list_countries_EMEA=[ 'AM', 'AT', 'BE', 'CH','CZ', 'DE', 'ES', 'FR',  'GB',  'GH', 'IL', 'IR',  'IT', 'JO', 'LV', 
                     'NL', 'NO', 'PL', 'RO', 'RU', 'TZ',  'SE',  'UK' ]
EMEA_CODE="EMEA"
list_countries_Americas=[  'BR' ,'CA', 'US' ]
AMERICAS_CODE="AMERICAS"
list_countries_Asia=[ 'JP', 'TH', 'AU', 'CN', 'TW', 'IN', 'KR' ]
ASIA_CODE="ASIA"
REGION_UNKNOWN_CODE="Region Unknown"


country_for_affiliations={
    'Science and Technology Facilities Council': { 'code': "UK" , 'name':"United Kingdom"}, 
    'Cockcroft Institute': { 'code': "UK" , 'name':"United Kingdom"},
    'DAWONSYS': { 'code': "KR" , 'name':"South Korea"},
    'Zhongke Fuhai Technology Co. Ltd.' : { 'code': "CN" , 'name':"China"},
    'Guoli Vacuum' : { 'code': "CN" , 'name':"China"},
    'Babcock Noell GmbH': { 'code': "DE" , 'name':"Germany"},
    'University of Milan; Istituto Nazionale di Fisica Nucleare, Laboratori Acceleratori e Superconduttività Applicata': { 'code': "IT" , 'name':"Italy"},
    'University of California, San Diego': { 'code': "US" , 'name':"United States"},
    'Michigan State University; Facility for Rare Isotope Beams': { 'code': "US" , 'name':"United States"},
    'SLAC National Accelerator Laboratory; Hoover Institution': { 'code': "US" , 'name':"United States"},
    'Argonne National Laboratory': { 'code': "US" , 'name':"United States"},
    'Japan Proton Accelerator Research Complex; High Energy Accelerator Research Organization': { 'code': "JP" , 'name':"Japan"},
    'High Energy Accelerator Research Organization; Japan Proton Accelerator Research Complex': { 'code': "JP" , 'name':"Japan"},
    'Research Center for Accelerator and Radioisotope Science (RARiS), Tohoku University': { 'code': "JP" , 'name':"Japan"},
    }
country_for_emails={
    'ca': { 'code': "CA" , 'name':"Canada"},
    'ch': { 'code': "CH" , 'name':"Switzerland"},
    'cn': { 'code': "CN" , 'name':"China"},
    'de': { 'code': "DE" , 'name':"Germany"},
    'fr': { 'code': "FR" , 'name':"France"},
    'it': { 'code': "IT" , 'name':"Italy"},
    'jp': { 'code': "JP" , 'name':"Japan"},
    'kr': { 'code': "KR" , 'name':"South Korea"},
    'uk': { 'code': "UK" , 'name':"United Kingdom"}, 
    }


#Calculated parameters
event_url="https://indico.jacow.org/event/"+str(event_id)+"/"

#reading secret files
if not ('api_token' in locals() or 'api_token' in globals()):
    fname="../api_token.txt"
    try:
        fpwd=open(fname)
        api_token=fpwd.readlines()[0].strip()
        fpwd.close()
    except:
        print("Unable to read ",fname)
        print("You need to create a file called api_token containing your api_token in the directory above the one where the LPR scripts are located")
        sys.exit(1)

if not ('mail_pwd' in locals() or 'mail_pwd' in globals()):
    fname="../mailpwd.txt"
    try:
        fpwd=open(fname)
        mail_pwd=fpwd.readlines()[0].strip()
        fpwd.close()
        print('mailpwd loaded')
    except:
        print("Unable to read ",fname,". You wont't be able to send emails")


