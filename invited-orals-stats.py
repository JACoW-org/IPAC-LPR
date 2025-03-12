#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 21:47:52 2025

LIst all talks suggested for invited orals

@author: delerue
"""

import params

import sys
#import requests,json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

sys.path.append('../jacow-ipac-lpr/')
import users_functions as uf
#import jacow_nd_func as jnf
import papers_functions as pf
import indico_functions as indf

submission_deadline='2025-03-21'

headers = {'Authorization': f'Bearer {params.api_token}'}

warnings=[]

abstracts_table_header="../jacow-ipac-lpr/abstracts-table_header.html"
abstracts_table_footer_no_vote="../jacow-ipac-lpr/abstract-table_footer_no_vote.html"
abstracts_table_footer_with_vote="../jacow-ipac-lpr/abstract-table_footer_with_vote.html"
abstracts_table_no_vote_filename="abstracts_table_no_vote.html"
abstracts_table_with_vote_filename="vote_on_abstracts.html"

    
def warning_message(abstract_id,friendly_id,message):
    warning_txt="Warning on abstract "+str(friendly_id)+" "+str(abstract_id)+" : "+str(message)+f"\nURL:   {params.event_url}abstracts/{abstract_id}/   "
    warnings.append(warning_txt)
    print("****\n"+warning_txt)

def show_all_warnings():
    print("***** WARNINGS *****")
    for txt in warnings:
        print(txt)


#url2023="https://indico.jacow.org/event/41/manage/abstracts/abstracts.json"
#indico_get(url2023,headers=headers,cachable=True,filetype='json')
'''
url2025="https://indico.jacow.org/event/63/manage/abstracts/abstracts.json"
data_2025=indico_get(url2025,headers=headers,cachable=True,datatype='json')
print(data_2025)
print(data_2025.keys())

for abstract in data_2025['abstracts'][0:100]:
    the_date=abstract['submitted_dt'][0:10]
    print(the_date)
exit()
'''

abstracts_page=open(abstracts_table_no_vote_filename,"w")
opr=open(abstracts_table_header,"r")
for line in opr:
    abstracts_page.write(line)
opr.close()



data = indf.indico_get(f'{params.event_url}/manage/abstracts/abstracts.json',datatype='json',headers=headers)
#print(data.text)
#print(data.json().keys())
'''
print(len(data.json()['abstracts']))
print(data.json()['abstracts'][20]['id'])
print(data.json()['abstracts'][20]['friendly_id'])
print(data.json()['abstracts'][20]['submitter'])
print(data.json()['abstracts'][20]['title'])
print(data.json()['abstracts'][20]['state'])
print(data.json()['abstracts'][20]['persons'])
print(data.json()['abstracts'][20]['persons'][0])
print(data.json()['abstracts'][20]['content'])
print(data.json()['abstracts'][20]['submitted_for_tracks'])
print(data.json()['abstracts'][20]['custom_fields'])
print(data.json()['abstracts'][20].keys())
'''


MC_codes_with_gender={}
MC_codes_with_seniority={}
MC_codes_with_region={}
speakers_region={}
speakers_gender={}
speakers_seniority={}
suggested_speakers_list_emails=[]
suggested_speakers_list_userids=[]
suggested_speakers_list_emails_multiple=[]
suggested_speakers_list_userids_multiple=[]

date_format = "%Y-%m-%d"
deadline = datetime.strptime(submission_deadline, date_format)
all_dates=[]

for abstract in data['abstracts']:
    if abstract['state'] == 'submitted':
        #print(abstract.keys())
        #exit()
        the_date=abstract['submitted_dt'][0:10]
        the_date_fmt = datetime.strptime(the_date, date_format)
        delta=deadline-the_date_fmt
        all_dates.append(int(delta.days))


        #print(abstract['submitter'])
        #submitter_roles=uf.has_role(email=abstract['submitter']['email'],userid=abstract['submitter']['id'])
        theroles=uf.has_role_codes(email=abstract['submitter']['email'],userid=abstract['submitter']['id'],only_codes=['OCM', 'SPM' , 'SPO' , 'SPC', 'SAM', 'SAS', 'SEU' ])
        if len(theroles)==0:
            warning_message(abstract['id'],abstract['friendly_id'],"Abstract submitted by submitter with no role")
        #print("Submitter role:",theroles,len(theroles))            

        MC_code=abstract['submitted_for_tracks'][0]['title'][0:3]
        speaker_gender='Unknown'
        speaker_seniority='Unknown'
        for cf in abstract['custom_fields']:
            if 'speaker gender' in cf['name']:
                speaker_gender=cf['value']       
            if 'speaker seniority' in cf['name']:
                speaker_seniority=cf['value']
        
        #print(speaker_seniority)
        if speaker_seniority=='Student':            
            warning_message(abstract['id'],abstract['friendly_id'],"Speaker is student")                                        
        
        speaker_region="Region Unknown"
        thespeaker=None
        for person in abstract['persons']:
            if person['is_speaker']:
                if thespeaker is None:
                    thespeaker=person
                else:
                    warning_message(abstract['id'],abstract['friendly_id'],"multiple speakers defined")                                        
        if thespeaker is None:
                    warning_message(abstract['id'],abstract['friendly_id'],"no speaker")                                                    
        if 'affiliation_link' in thespeaker.keys():
            if  thespeaker['affiliation_link'] is not None and 'country_code' in thespeaker['affiliation_link'].keys():
                #print(thespeaker['affiliation_link']['country_code'])
                speaker_region=uf.get_user_region(thespeaker['affiliation_link']['country_code'])
                speaker_affiliation=thespeaker['affiliation_link']['country_code']
            else:
                warning_message(abstract['id'],abstract['friendly_id'],"unable to identify the speaker's affiliation or country")  
                speaker_affiliation="Unknown"
            
                
        #Statistics
        indf.accumulate(MC_code, MC_codes_with_gender,speaker_gender)
        indf.accumulate(MC_code, MC_codes_with_region,speaker_region)
        indf.accumulate(MC_code, MC_codes_with_seniority,speaker_seniority)
        indf.accumulate(speaker_gender, speakers_gender,speaker_region)
        indf.accumulate(speaker_seniority,speakers_seniority)
        indf.accumulate(speaker_region, speakers_region,speaker_gender)
        
        speaker_seniority_short=speaker_seniority.split("(")[0].strip()
            
        #Creates the abstracts table
        #print(abstract)
        #print(abstract.keys())
        abstract_url=f"{params.event_url}/abstracts/{abstract['id']}"
        abstracts_page.write("<tr id=\"{abstract['id']}\">")
        abstracts_page.write(f"<td>{abstract['id']}</td>")
        abstracts_page.write(f"<td>{abstract['friendly_id']}</td>")
        abstracts_page.write(f"<td>{MC_code} </td>")
        abstracts_page.write(f"<td>{abstract['title']}</td>")
        abstracts_page.write(f"<td>{thespeaker['first_name']} {thespeaker['last_name']}</td>")
        abstracts_page.write(f"<td>{thespeaker['affiliation']}</td>")
        abstracts_page.write(f"<td>{speaker_affiliation} - {speaker_region} </td>")
        abstracts_page.write(f"<td>{speaker_gender}</td>")
        abstracts_page.write(f"<td>{speaker_seniority_short}</td>")
        abstracts_page.write(f"<td><A HREF='{abstract_url}'>Details</A>")
        #abstracts_page.write("<BR><A>Show abstract</A>")
        abstracts_page.write("</td>")
        abstracts_page.write("<td> --- </td>")
        abstracts_page.write(f"<td>{MC_code} </td>")
        abstracts_page.write("</tr>\n")
        if 1==0:
            abstracts_page.write(f"<tr id=\"abstract_{abstract['id']}\" style=\"display: none;\">\n")
            abstracts_page.write("<td> Abstract:\n")
            abstracts_page.write("</td>")
            abstracts_page.write("</tr>\n")
        
        #Quality checks
        if len(abstract['content'])<100:
            warning_message(abstract['id'],abstract['friendly_id'],"Short abstract")

        if speaker_region=="Region Unknown":
            warning_message(abstract['id'],abstract['friendly_id'],"Unknown region")  
            
        #print(thespeaker['email'])
        if thespeaker['email'] is None or len(thespeaker['email'])<3:
            warning_message(abstract['id'],abstract['friendly_id'],"no email for speaker")
        else:
            if abstract['submitter']['email'] == thespeaker['email']:
                warning_message(abstract['id'],abstract['friendly_id'],"Submitter and speaker have the same email address")
            speakroles=uf.has_role_codes(email=thespeaker['email'],only_codes=['OCM', 'SPM' , 'SPO' , 'SPC' ])
            if len(speakroles)>0:
                    warning_message(abstract['id'],abstract['friendly_id'],"Abstract speaker "+str(thespeaker['email'])+" has a role: "+str(speakroles))

            speaker_data=uf.find_user(email=thespeaker['email'])            
            if len(speaker_data)==0 or len(speaker_data)>2:
                warning_message(abstract['id'],abstract['friendly_id'],"undefined speaker "+str(speaker_data))
            else:
                if thespeaker['email'] in suggested_speakers_list_emails:
                    warning_message(abstract['id'],abstract['friendly_id'],"Speaker (email) suggested multiple times "+str(thespeaker['email']))
                    suggested_speakers_list_emails_multiple.append(thespeaker['email'])

                suggested_speakers_list_emails.append(thespeaker['email'])
                if 'user_id' in speaker_data[0].keys():                  
                    if speaker_data[0]['user_id'] in suggested_speakers_list_userids:
                        warning_message(abstract['id'],abstract['friendly_id'],"Speaker (userid) suggested multiple times "+str(thespeaker['email'])+" "+str(speaker_data[0]['user_id']))
                        suggested_speakers_list_userids_multiple.append(speaker_data[0]['user_id'])
                    suggested_speakers_list_userids.append(speaker_data[0]['user_id'])
                if 1==0:
                    #this part is creating problem
                    if 'user_id_all' in speaker_data[0].keys():    
                        for userid in speaker_data[0]['user_id_all']:
                            if userid in suggested_speakers_list_userids:
                                warning_message(abstract['id'],abstract['friendly_id'],"Speaker (userid) suggested multiple times "+str(thespeaker['email'])+" "+str(speaker_data[0]['user_id'])+" (all)"+userid)
                                suggested_speakers_list_userids_multiple.append(speaker_data[0]['user_id'])
                            suggested_speakers_list_userids.append(userid)
                if 'papers' not in speaker_data[0].keys():
                    warning_message(abstract['id'],abstract['friendly_id'],"no papers in speaker_data "+str(speaker_data[0]['last_name'])+" "+str(speaker_data[0]['first_name'])+"; Search Jacow:\n https://search.cern.ch/Pages/results.aspx?k=+domain%3Daccelconf%2Eweb%2Ecern%2Ech++%2Bauthor%3A%"+str(speaker_data[0]['last_name'])+"%22%20%20FileExtension%3Dpdf%20-url%3Aabstract%20-url%3Aaccelconf/jacow \n\n")
                elif len(speaker_data[0]['papers'])==0:
                    warning_message(abstract['id'],abstract['friendly_id'],"speaker is not associated with any IPAC papers in the past 3 years")       
                    
                    for paper in speaker_data[0]['papers']:
                        if 'speakers' in paper['role']:
                            paper_data=pf.get_contrib_info(paper['id'],event_id=paper['conf-id'])
                            if not paper_data['type']['name']=='Poster Presentation': 
                                warning_message(abstract['id'],abstract['friendly_id'],"speaker was speaker for "+str(paper_data['type'])+" "+paper['conf-id']+"  "+paper['conf']+" "+paper['id'])               


abstracts_page.close()

abstracts_page_with_vote=open(abstracts_table_with_vote_filename,"w")
opr=open(abstracts_table_no_vote_filename,"r")
for line in opr:
    abstracts_page_with_vote.write(line)
opr.close()
opr=open(abstracts_table_footer_with_vote,"r")
for line in opr:
    abstracts_page_with_vote.write(line)
opr.close()
abstracts_page_with_vote.close()


abstracts_page_no_vote=open(abstracts_table_no_vote_filename,"a")
opr=open(abstracts_table_footer_no_vote,"r")
for line in opr:
    abstracts_page_no_vote.write(line)
opr.close()
abstracts_page_no_vote.close()

print("suggested_speakers_list_userids_multiple",suggested_speakers_list_userids_multiple)
for userid in suggested_speakers_list_userids_multiple:
    speaker_data=uf.find_user(user_id=userid)
    for speak in speaker_data:
        if 'email' in speak.keys():
            suggested_speakers_list_emails_multiple.append(speak['email'])

suggested_speakers_list_emails_multiple=list(set(suggested_speakers_list_emails_multiple))
print("suggested_speakers_list_emails_multiple",suggested_speakers_list_emails_multiple)

for email in suggested_speakers_list_emails_multiple:
    print('email',email)
    speaker_data=uf.find_user(email=email)
    print('*** Multiple suggestion for ',email,'***') 
    for abstract in data['abstracts']:
        #print(".*",end='',flush=True)
        if abstract['state'] == 'submitted':
            for person in abstract['persons']:
                #print(".",end='',flush=True)
                if person['is_speaker']:
                    if person['email'] == email:
                        print(abstract['id'],abstract['friendly_id'],"submitted by",abstract['submitter']['email'],"Title:",abstract['title'])                        
                    else:
                        if 1==0:
                            #This is slowing too much the script
                            if len(person['email'])>3:
                                person_data=uf.find_user(email=person['email'])
                                for theperson in person_data:
                                    if theperson is not None:
                                        if 'email' in theperson.keys():
                                            if theperson['email'] == email:
                                                print('*',abstract['id'],abstract['friendly_id'],"submitted by",abstract['submitter']['email'],"Title:",abstract['title'])



#url2023="https://indico.jacow.org/event/41/manage/abstracts/abstracts.json"
#indico_get(url2023,headers=headers,cachable=True,filetype='json')

#date plot    
all_days=np.zeros(np.max(all_dates)+5)
for day in all_dates:
    for iday in range(np.max(all_dates)-day,len(all_days)):
        all_days[iday]=all_days[iday]+1
#print(all_days)
fig=plt.figure(figsize=(8, 6), dpi=100)
max_day=len(all_days)
plt.plot(range(len(all_days)-5,-5,-1),all_days)
plt.xlabel("days before deadline")
plt.ylabel("# applications")
plt.xlim(max_day,-5)
plt.title("Applications as of "+datetime.today().strftime('%d/%m/%Y %H:%M'))
plt.grid(True)
plt.legend()
plt.savefig("invited_orals_timeline.png")
plt.show()


for key in [ 'Main Classifications with gender' ,'Main Classifications with seniority' ,'Main Classifications with region' , 'Gender' , 'Seniority', 'Region']:    
    fig=plt.figure(figsize=(8, 6), dpi=100)
    #fig=plt.figure()
    if 'Main' in key:
        if 'gender' in key:
            thedict=MC_codes_with_gender
        if 'seniority' in key:
            thedict=MC_codes_with_seniority
        if 'region' in key:
            thedict=MC_codes_with_region
    if 'Gender' in key:
        thedict=speakers_gender
    if 'Seniority' in key:
        thedict=speakers_seniority
    if 'Region' in key:
        thedict=speakers_region

    thekeys=[]
    vals=[]
    subvals={}
    for dat in thedict:
        thekeys.append(dat.split('(')[0].strip().split('/')[0].strip())    
        vals.append(thedict[dat]['All'])
        #print(thedict[dat])
        for subval in thedict[dat].keys():
            if not subval=='All':
                if not subval in subvals.keys():
                    subvals[subval]=[]
                while(len(subvals[subval])<len(vals)-1):
                    subvals[subval].append(0)
                subvals[subval].append(thedict[dat][subval])
                #print(subval,subvals[subval])
        
    for subval in subvals.keys():
        while(len(subvals[subval])<len(vals)):
            subvals[subval].append(0)
    bins_edges=np.linspace(-0.5,len(thekeys)-0.5,len(thekeys)+1)
    #print(bins_edges)
    values, bins, bars =plt.hist(thekeys,weights=vals,edgecolor='black',linewidth=1.2,bins=bins_edges,color='green',label='_nolegend_')
    plt.bar_label(bars, fontsize=18, color='navy')
    icolor=0
    colors=[ 'lightsteelblue' , 'plum' , 'palegreen' , 'salmon' , 'yellow' , 'brown' ]
    baseval=np.array(vals)
    for subval in subvals.keys():
        if subval=='Male':
            thecolor='lightsteelblue' 
        elif subval=='Female':
            thecolor='pink' 
        elif subval=='Non binary':
            thecolor='lightgrey' 
        elif subval=="Don't know":
            thecolor='grey' 
        else:
            thecolor=colors[icolor]
        
        #print(subval,subvals[subval],baseval,baseval-subvals[subval])
        plt.hist(thekeys,weights=baseval,bins=bins_edges,edgecolor='black',color=thecolor,label=subval.split('(')[0].strip().split('/')[0].strip())
        baseval=baseval-subvals[subval]
        icolor=icolor+1
    '''
    plt.hist(thekeys,weights=valsMr,bins=bins_edges,edgecolor='black',color='lightsteelblue',label="Mr")
    plt.hist(thekeys,weights=valsOverseas,bins=bins_edges,edgecolor='black',color='red',label="Overseas")
    '''
    #plt.title(key+ " - "+year_data +" - Sum="+str(np.sum(vals))+" - "+datetime.today().strftime('%d/%m/%Y %H:%M'))
    plt.title(key+ " - Sum="+str(np.sum(vals))+" - "+datetime.today().strftime('%d/%m/%Y %H:%M'),size=20)
    plt.xticks(rotation = 90,size=18)   
    plt.yticks(size=18)   
    #plt.margins(x=0.01, y=0.2)
    fig.tight_layout()
    plt.legend( prop={'size': 18})
    #plt.grid(True)
    filename="invited_orals_stats_"+key.replace(" ","_")+".png"
    print(filename)
    plt.savefig(filename)
    
    plt.show()

indf.update_to_meeting(meeting_id='100',filename="invited_orals_timeline.png",filetype='image/png',indico_server="jacow.org",api_token=params.api_token,delete_key='775')
indf.update_to_meeting(meeting_id='100',filename="invited_orals_stats_Main_Classifications_with_region.png",filetype='image/png',indico_server="jacow.org",api_token=params.api_token,delete_key='775')
indf.update_to_meeting(meeting_id='100',filename="invited_orals_stats_Main_Classifications_with_seniority.png",filetype='image/png',indico_server="jacow.org",api_token=params.api_token,delete_key='775')
indf.update_to_meeting(meeting_id='100',filename="invited_orals_stats_Gender.png",filetype='image/png',indico_server="jacow.org",api_token=params.api_token,delete_key='775')
indf.update_to_meeting(meeting_id='100',filename="invited_orals_stats_Region.png",filetype='image/png',indico_server="jacow.org",api_token=params.api_token,delete_key='775')
indf.update_to_meeting(meeting_id='100',filename=abstracts_table_no_vote_filename,filetype='text/html',indico_server="jacow.org",api_token=params.api_token,delete_key='775')
indf.update_to_meeting(meeting_id='100',filename=abstracts_table_with_vote_filename,filetype='text/html',indico_server="jacow.org",api_token=params.api_token,delete_key='775')

#print("Don't show warnings")
show_all_warnings()
