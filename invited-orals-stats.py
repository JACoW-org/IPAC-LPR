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

#sys.path.append('../jacow-ipac-lpr/')
import users_functions as uf
#import jacow_nd_func as jnf
import papers_functions as pf
import indico_functions as indf

submission_deadline='2025-03-21'

headers = {'Authorization': f'Bearer {params.api_token}'}

warnings=[]

qa_table_header="abstracts-table_header.html"


abstracts_table_header="abstracts-table_header.html"
abstracts_table_footer_no_vote="abstract-table_footer_no_vote.html"
abstracts_table_footer_with_vote="abstract-table_footer_with_vote.html"

qa_table_header="sort-table_header_generic.html"
qa_table_dict={ "Title":"IPAC'26 invited orals Quality Assessment" , "table_id": "quality_assessment"}
#qa_table_heads=[ "id" , "friendly_id" , "MC", "speaker_name", "submitter_email" , "title" , "url",  "qa_issues" ]
qa_table_heads=[ "id" , "friendly_id" , "MC", "speaker_name", "title" , "url",  "qa_issues" ]

qa_page_filename="abstracts_qa.html"

abstracts_table_no_vote_filename="abstracts_table_no_vote.html"
abstracts_table_with_vote_filename="vote_on_abstracts.html"

skip_qa_issues_on_abstracts=[ 9784 ]

all_affiliations={}
all_ids={}
    
def warning_message(abstract,message):
    warning_cleared=False
    warning_recorded=False
    for comment in abstract['comments']:
        #print("comment:",comment['text'])
        if "QA_OK" in comment['text']:
            cleared_warning=comment['text'].split(":")[1].strip()
            #print("cleared_warning",cleared_warning)
            if cleared_warning in message:
                #print("Warning cleared")
                warning_cleared=True
            else:
                #print(cleared_warning,"\n is not in\n",message)
                #print(message.find(cleared_warning))
                pass
        elif "QA issue" in comment['text']:
            written_warning=comment['text'].split(":")[1].strip()
            if written_warning in message:
                #print("Warning cleared")
                warning_recorded=True
            
            
    if not warning_cleared:
        abstract_id=abstract["id"]
        friendly_id=abstract["friendly_id"]
        warning_txt="Warning on abstract "+str(friendly_id)+" "+str(abstract_id)+" : "+str(message)+f"\nURL:   {params.event_url}abstracts/{abstract_id}/   "
        abstract["qa_issues"].append(message)
        warnings.append(warning_txt)
        print("****\n"+warning_txt)
        if not warning_recorded:
            print("Recording warning")
            indf.comment_abstract(meeting_id=params.event_id,db_id=abstract['id'],comment="QA issue: "+message, visibility="judges", api_token=params.api_token)

def show_all_warnings():
    print("********************************************************************************")
    print("********************************************************************************")
    print("********************************************************************************")
    print("********************************************************************************")
    print("********************************************************************************")
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
    
    #if abstract['state'] == 'submitted' or abstract['state'] == 'accepted':
    if not abstract['state'] == 'submitted':
        print("Skipping",abstract['id'],abstract['friendly_id'],abstract['state'])
    else:
        #print(abstract.keys())
        abstract["qa_issues"]=[] 
        
        #exit()
        the_date=abstract['submitted_dt'][0:10]
        the_date_fmt = datetime.strptime(the_date, date_format)
        delta=deadline-the_date_fmt
        all_dates.append(int(delta.days))
        print(len(all_dates))

        abstract['submitter_email']=abstract['submitter']['email']

        #print(abstract['submitter'])
        #submitter_roles=uf.has_role(email=abstract['submitter']['email'],userid=abstract['submitter']['id'])
        theroles=uf.has_role_codes(email=abstract['submitter']['email'],userid=abstract['submitter']['id'],only_codes=['OCM', 'SPM' , 'SPO' , 'SPC', 'SAM', 'SAS', 'SEU' ])
        if len(theroles)==0:
            warning_message(abstract,"Abstract submitted by submitter with no role")
        #print("Submitter role:",theroles,len(theroles))            

        MC_code=abstract['submitted_for_tracks'][0]['title'][0:3]
        MC_code=abstract['reviewed_for_tracks'][0]['title'][0:3]
        abstract['MC']=MC_code
        speaker_gender='Unknown'
        speaker_seniority='Unknown'
        for cf in abstract['custom_fields']:
            if 'speaker gender' in cf['name']:
                speaker_gender=cf['value']       
            if 'speaker seniority' in cf['name']:
                speaker_seniority=cf['value']
        
        #print(speaker_seniority)
        #if speaker_seniority=='Student':            
        #    warning_message(abstract,"Speaker is student")                                        
        
        speaker_region="Region Unknown"
        thespeaker=None
        for person in abstract['persons']:
            if person['is_speaker']:
                if thespeaker is None:
                    thespeaker=person
                else:
                    warning_message(abstract,"multiple speakers defined "+person['first_name']+" "+person['last_name']+" and "+thespeaker['first_name']+" "+thespeaker['last_name']) 
        if thespeaker is None:
                    warning_message(abstract,"no speaker")                                                    
        if 'affiliation_link' in thespeaker.keys():
            if  thespeaker['affiliation_link'] is not None and 'country_code' in thespeaker['affiliation_link'].keys():
                #print(thespeaker['affiliation_link']['country_code'])
                if len(thespeaker['affiliation_link']['country_code'])==0:
                    uf.fix_user_country(thespeaker)
                if len(thespeaker['affiliation_link']['country_code'])==0:
                    warning_message(abstract,"Empty country code for the speaker's affiliation "+thespeaker['last_name']+" "+thespeaker['affiliation'])
                speaker_region=uf.get_user_region(thespeaker['affiliation_link']['country_code'])
                speaker_affiliation=thespeaker['affiliation_link']['country_code']
            else:
                uf.fix_user_country(thespeaker)
                if  thespeaker['affiliation_link'] is None or not 'country_code' in thespeaker['affiliation_link'].keys():                
                    warning_message(abstract,"Unable to identify the speaker's affiliation or country. Speaker: "+thespeaker['last_name']+"; Affiliation: "+thespeaker['affiliation'])                    
                    speaker_affiliation="Unknown"
                    speaker_region="Unknown"
                    if int(abstract['id'])>300:
                        print("Unable to identify the speaker's affiliation")
                        print(thespeaker)
                        #exit()
                else:
                    speaker_region=uf.get_user_region(thespeaker['affiliation_link']['country_code'])
                    speaker_affiliation=thespeaker['affiliation_link']['country_code']                    
        else:
            #speaker without affiliation link
            uf.fix_user_country(thespeaker)
            speaker_region=uf.get_user_region(thespeaker['affiliation_link']['country_code'])
            speaker_affiliation=thespeaker['affiliation_link']['country_code']
        if speaker_region=="Region Unknown":
            print("speaker_region", speaker_region)
            print(thespeaker)
            print('country_code',thespeaker['affiliation_link']['country_code'])
            exit()
        #print(thespeaker.keys())
        #print(thespeaker['affiliation'])
        #exit()
        if not thespeaker['affiliation'] in all_affiliations:
            all_affiliations[thespeaker['affiliation']]=[]
        all_affiliations[thespeaker['affiliation']].append(abstract['id'])
   
                
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
        abstract_url=f"{params.event_url}abstracts/{abstract['id']}"
        abstract['url']=abstract_url
        abstract['speaker_name']=f"{thespeaker['first_name']} {thespeaker['last_name']}"
        abstracts_page.write(f"<tr id=\"{abstract['id']}\">")
        abstracts_page.write(f"<td>{abstract['id']}</td>")
        abstracts_page.write(f"<td>{abstract['friendly_id']}</td>")
        abstracts_page.write(f"<td>{MC_code}</td>")
        abstracts_page.write(f"<td>{abstract['title']}</td>")
        abstracts_page.write(f"<td>{thespeaker['first_name']} {thespeaker['last_name']}</td>")
        abstracts_page.write(f"<td>{thespeaker['affiliation']}</td>")
        abstracts_page.write(f"<td>{speaker_region}  - {speaker_affiliation}</td>")
        abstracts_page.write(f"<td>{speaker_gender}</td>")
        abstracts_page.write(f"<td>{speaker_seniority_short}</td>")
        abstracts_page.write(f"<td><A HREF='{abstract_url}'>Details</A>")
        #abstracts_page.write("<BR><A>Show abstract</A>")
        abstracts_page.write("</td>")
        abstracts_page.write("<td> ")
        abstracts_page.write(f"<form><button type=button onClick='update_abstract(\"{abstract_url}\")'>Reload</button></form>");
        abstracts_page.write("</td>")
        abstracts_page.write(f"<td>{MC_code} </td>")
        abstracts_page.write("</tr>\n")
        if 1==0:
            abstracts_page.write(f"<tr id=\"abstract_{abstract['id']}\" style=\"display: none;\">\n")
            abstracts_page.write("<td> Abstract:\n")
            abstracts_page.write("</td>")
            abstracts_page.write("</tr>\n")
                
        #Quality checks
        if len(abstract['content'])<10:
            warning_message(abstract,"Short abstract")

        if speaker_region=="Region Unknown":
            warning_message(abstract,"Unknown region")  
            
        #print(thespeaker['email'])
        if thespeaker['email'] is None or len(thespeaker['email'])<3:
            warning_message(abstract,"no email for speaker")
        else:
            if abstract['submitter']['email'] == thespeaker['email']:
                warning_message(abstract,"Submitter and speaker have the same email address")
            speakroles=uf.has_role_codes(email=thespeaker['email'],only_codes=['OCM', 'SPM' , 'SPO' , 'SPC' ])
            if len(speakroles)>0:
                    warning_message(abstract,"Abstract speaker "+str(thespeaker['email'])+" has a role: "+str(speakroles))

            speaker_data=uf.find_user(email=thespeaker['email'])            
            if speaker_data is None or len(speaker_data)==0 or speaker_data[0] is None or len(speaker_data)>2:
                if len(speaker_data)>2:
                    warning_message(abstract,"undefined speaker "+str(speaker_data))
                else:
                    print("undefined speaker (speaker data empty)")
                    #warning_message(abstract,"undefined speaker (speaker data empty)")
            else:
                if thespeaker['email'] in suggested_speakers_list_emails:
                    #warning_message(abstract,"Speaker (email) suggested multiple times "+str(thespeaker['email']))
                    suggested_speakers_list_emails_multiple.append(thespeaker['email'])
                elif 'user_id' in speaker_data[0].keys():                  
                    if speaker_data[0]['user_id'] in suggested_speakers_list_userids:
                        #warning_message(abstract,"Speaker (userid) suggested multiple times "+str(thespeaker['email'])+" "+str(speaker_data[0]['user_id']))
                        suggested_speakers_list_userids_multiple.append(speaker_data[0]['user_id'])
                    suggested_speakers_list_userids.append(speaker_data[0]['user_id'])
                suggested_speakers_list_emails.append(thespeaker['email'])

                if 1==0:
                    #this part is creating problem
                    if 'user_id_all' in speaker_data[0].keys():    
                        for userid in speaker_data[0]['user_id_all']:
                            if userid in suggested_speakers_list_userids:
                                #warning_message(abstract,"Speaker (userid) suggested multiple times "+str(thespeaker['email'])+" "+str(speaker_data[0]['user_id'])+" (all)"+userid)
                                suggested_speakers_list_userids_multiple.append(speaker_data[0]['user_id'])
                            suggested_speakers_list_userids.append(userid)
                if 'papers' not in speaker_data[0].keys():
                    pass
                    #warning_message(abstract,"no papers in speaker_data "+str(speaker_data[0]['last_name'])+" "+str(speaker_data[0]['first_name'])+"; Search Jacow:\n https://search.cern.ch/Pages/results.aspx?k=+domain%3Daccelconf%2Eweb%2Ecern%2Ech++%2Bauthor%3A%"+str(speaker_data[0]['last_name'])+"%22%20%20FileExtension%3Dpdf%20-url%3Aabstract%20-url%3Aaccelconf/jacow \n\n")
                elif len(speaker_data[0]['papers'])==0:
                    pass
                    #warning_message(abstract,"speaker is not associated with any IPAC papers in the past 3 years")       
                else:                    
                    for paper in speaker_data[0]['papers']:
                        #print(speaker_data[0]['papers'])
                        if 'speakers' in paper['role']:
                            paper_data=pf.get_contrib_info(paper['id'],event_id=paper['conf-id'])
                            #print("Paper type", paper_data['type']['name'])
                            #print("poster?", paper_data['type']['name'].find('Poster'))
                            if paper_data['type']['name'].find('Poster')<0: 
                                warning_message(abstract,"Speaker was speaker for "+str(paper_data['type']['name'])+" at conf "+paper['conf']+" "+paper['conf-id']+" with paper <A HREF=https://indico.jacow.org/event/"+paper['conf-id']+"/contributions/"+paper['id']+"/ > #"+paper['id']+" </A>")
        #print(abstract['id'])
        
        
        #fill qa_table    
        if len(abstract["qa_issues"])>0 and not int(abstract['id']) in skip_qa_issues_on_abstracts:
            for iissue in range(len(abstract["qa_issues"])):
                qa_page.write(f"<tr id=\"{abstract['id']}\">")        
                for head in qa_table_heads:            
                    qa_page.write("<td>\n")
                    if head=="qa_issues":
                        #print(iissue)
                        qa_page.write(str(abstract["qa_issues"][iissue]))                     
                        #elif head=="MC":
                        #    qa_page.write(MC_code) 
                    elif head=="url":
                        qa_page.write("<A HREF='"+str(abstract[head])+"'>"+str(abstract[head])+"</A>")
                    else:
                        qa_page.write(str(abstract[head]))
                    qa_page.write("</td>\n")
                qa_page.write("</tr>\n")
        '''
        if len(abstract["qa_issues"])>1:
            print(str(abstract["qa_issues"]))
            print(str(abstract["qa_issues"][0]))
            print(str(abstract["qa_issues"][1]))
        '''
        '''
        if str(abstract['id']) == '9569':
            print(thespeaker)
            #print(abstract['judgment_comment'])
            print(len(abstract['comments']))
            print(abstract['comments'][0])
            #print(speaker_data[0])
            #print(speaker_data[0]['papers'])
            sys.exit()
        '''

abstracts_page.close()

qa_page.write("</table>")

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

duplicate_skip_dict={}
duplicate_skip_dict['frank.zimmermann@cern.ch']=[ 9264 , 9565 ]
#duplicate_skip_dict['andrea.latina@cern.ch']=[ 9587 , 9590 ]
duplicate_skip_dict['c.a.lindstrom@fys.uio.no']=[ 9635 ]
#duplicate_skip_dict['francis.cullinan@maxiv.lu.se'] = [ 9259 , 9646 ]
#duplicate_skip_dict['michael.benedikt@cern.ch'] = [ 9267 , 9614 ]
duplicate_skip_dict['haehnel@iap.uni-frankfurt.de'] = [ 9686 , 9921 ]
duplicate_skip_dict['natalia.milas@esss.se'] = [ 9745 ]
duplicate_skip_dict['eleonore.roussel@univ-lille.fr'] = [ 9647, 9932 ]
duplicate_skip_dict['sebastien.corde@polytechnique.edu'] = [ 9660, 9681 ]
duplicate_skip_dict['iryna.chaikovska@ijclab.in2p3.fr'] = [ 9590, 9969]
duplicate_skip_dict['pedro.fernandes_tavares@maxiv.lu.se'] = [ 9580, 9602 ]
duplicate_skip_dict['r.apsimon@lancaster.ac.uk'] = [ 9726 ]




duplicate_dict={}
for email in suggested_speakers_list_emails_multiple:
    #print('email',email)
    speaker_data=uf.find_user(email=email)
    duplicate_dict[email]=[]
    for abstract in data['abstracts']:
        #print(".*",end='',flush=True)
        if abstract['state'] == 'submitted':
            for person in abstract['persons']:
                #print(".",end='',flush=True)
                if person['is_speaker']:
                    if person['email'] == email:                        
                        duplicate_dict[email].append(abstract['id'])

for key in duplicate_dict.keys():
    if not key in duplicate_skip_dict.keys() or len(duplicate_dict[key])>len(duplicate_skip_dict[key]):
        print('*** Multiple suggestion for ',key,'***') 
        qa_page.write('\n<P>*** Multiple suggestion for '+key+'***</Br>\n')
        for theid in duplicate_dict[key]:
            for abstract in data['abstracts']:
                if abstract['id']==theid:
                    print(abstract,"submitted by",abstract['submitter']['email'],"Title:",abstract['title'],"MC",abstract['MC'])          
                    abstract_url=f"{params.event_url}abstracts/{abstract['id']}"
                    qa_page.write(f"Abstract <A HREF={abstract_url}>{abstract['MC']}: {abstract['id']}: {abstract['title']} </A><BR/>submitted by {abstract['submitter']['email']} <BR/><BR/>\n")


    '''
                    else:
                        if 1==0:
                            #This is slowing too much the script
                            if len(person['email'])>3:
                                person_data=uf.find_user(email=person['email'])
                                for theperson in person_data:
                                    if theperson is not None:
                                        if 'email' in theperson.keys():
                                            if theperson['email'] == email:
                                                print('*',abstract,"submitted by",abstract['submitter']['email'],"Title:",abstract['title'])

    '''

#url2023="https://indico.jacow.org/event/41/manage/abstracts/abstracts.json"
#indico_get(url2023,headers=headers,cachable=True,filetype='json')

#date plot    
#print(data['abstracts'])
#print(len(data['abstracts']))
#print(all_dates)
#print("np.max(all_dates)",np.max(all_dates))
all_days=np.zeros(np.max(all_dates)+5)
for day in all_dates:
    for iday in range(np.max(all_dates)-day,len(all_days)):
        all_days[iday]=all_days[iday]+1
#print(all_days)
fig=plt.figure(figsize=(8, 6), dpi=100)
max_day=len(all_days)
plt.plot(range(len(all_days)-5,-5,-1),all_days)
plt.xlabel("days before deadline",size=18)
plt.ylabel("# applications",size=18)
plt.xlim(max_day,-5)
plt.xticks(size=18)   
plt.yticks(size=18)   
plt.title("Applications as of "+datetime.today().strftime('%d/%m/%Y %H:%M'),size=20)
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

qa_page.close()

#indf.update_to_meeting(meeting_id='100',filename="invited_orals_timeline.png",filetype='image/png',indico_server="jacow.org",api_token=params.api_token,delete_key='775')
#indf.update_to_meeting(meeting_id='100',filename="invited_orals_stats_Main_Classifications_with_region.png",filetype='image/png',indico_server="jacow.org",api_token=params.api_token,delete_key='775')
#indf.update_to_meeting(meeting_id='100',filename="invited_orals_stats_Main_Classifications_with_seniority.png",filetype='image/png',indico_server="jacow.org",api_token=params.api_token,delete_key='775')
#indf.update_to_meeting(meeting_id='100',filename="invited_orals_stats_Gender.png",filetype='image/png',indico_server="jacow.org",api_token=params.api_token,delete_key='775')
#indf.update_to_meeting(meeting_id='100',filename="invited_orals_stats_Region.png",filetype='image/png',indico_server="jacow.org",api_token=params.api_token,delete_key='775')
indf.update_to_meeting(meeting_id='100',filename=abstracts_table_no_vote_filename,filetype='text/html',indico_server="jacow.org",api_token=params.api_token,delete_key='775')
indf.update_to_meeting(meeting_id='100',filename=abstracts_table_with_vote_filename,filetype='text/html',indico_server="jacow.org",api_token=params.api_token,delete_key='775')
#indf.update_to_meeting(meeting_id='100',filename=qa_page_filename,filetype='text/html',indico_server="jacow.org",api_token=params.api_token,delete_key='775')


#print(all_affiliations)
print("****** Affiliations *******")
for key in sorted(all_affiliations.keys()):
    if len(all_affiliations[key])<20:
        print(key, all_affiliations[key] )
    else:
        print(key, "Many abstracts" )

#print("Don't show warnings")
show_all_warnings()

