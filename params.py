#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 21:54:43 2025

Parameters for the IPAC Light Peer Review

@author: delerue
"""

import sys

#Settings
event_id = 41


#List of all known users and their affiliation
users_file="data/users_file.data"
affiliations_file="data/affiliations_file.data"

#Maximum number of user search queries in a run
maxUserSearch=200

#Time interval to relaod teh contributions
reload_contrib_from_online_seconds=5*24*60*60

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

