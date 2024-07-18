#!/usr/local/bin/python3.9

# Stats about the papers authors
# Nicolas Delerue, 7/2023

import jacow_nd_func as jnf
#import argparse
#import openpyxl
#import datetime
#import urllib.parse
#import requests
#import time
#import matplotlib.pyplot as plt
#import numpy as np

import joblib
#import random

counter={}
counter['in double review']=0
counter['contrib_none']=0
counter['paper_none']=0

use_online=False
#use_online=True
fname='stats_papers_author.data'

all_continents = {}
all_countries = {}

for the_type in [ 'submitter' , 'speakers' , 'primaryauthors' , 'coauthors' ]:
    counter[the_type]={}
    counter[the_type]['not found']=0
    counter[the_type]['list']={}
    counter[the_type]['participant_none']=0
    counter[the_type]['unknown_participants']=[]
    counter[the_type]['country']={}
counter['MC']={}
counter['Track']={}

    
if use_online:
    the_range=range(500,2800)
else:
    the_range=[]
    
for the_id in the_range:
    if jnf.get_paper_in_double_reviews(the_id):        
        counter['in double review']=counter['in double review']+1
        contrib=jnf.find_contrib(the_id)
        if contrib is not None:
            the_paper=jnf.get_paper_info(contrib['db_id'])
        else:
            counter['contrib_none']=counter['contrib_none']+1
            the_paper=None
        if the_paper is not None:
            print('id=',the_id,'submitter ', the_paper['last_revision']['submitter']['full_name'],the_paper['last_revision']['submitter']['email'])
            participants=[]
            participants_emails=[]
            participants_type=[]
            for the_type in [ 'submitter' , 'speakers' , 'primaryauthors' , 'coauthors' ]:
                if the_type=='submitter':
                    participant=jnf.find_participant_by_email(the_paper['last_revision']['submitter']['email'])
                    if participant is not None:
                        participants.append(participant)
                        participants_type.append(the_type)
                        participants_emails.append(participant['email'])
                        if participant['country'] in counter[the_type]['country'].keys():
                            counter[the_type]['country'][participant['country']]=counter[the_type]['country'][participant['country']]+1
                        else:
                            counter[the_type]['country'][participant['country']]=1                            

                    else:
                        counter[the_type]['participant_none']=counter[the_type]['participant_none']+1
                        contributor_name=the_paper['last_revision']['submitter']['full_name']
                        counter[the_type]['unknown_participants'].append(the_paper['last_revision']['submitter']['email']+";"+contributor_name)

                else:
                    for contributor in contrib[the_type]:
                        #print('contrib',contributor)
                        contributor_name=contributor['first_name']+" "+contributor['last_name']
                        print(the_type,'contributor name', contributor_name)
                        participant=jnf.find_participant_by_name(contributor_name)
                        if participant is not None:
                            if participant['email'] not in participants_emails:
                                participants.append(participant)
                                participants_type.append(the_type)
                                participants_emails.append(participant['email'])
                        else:
                            print('none')
                            counter[the_type]['participant_none']=counter[the_type]['participant_none']+1
                            counter[the_type]['unknown_participants'].append(""+";"+contributor_name)
                            
            for iparticipant in range(0,len(participants)):
                participant=participants[iparticipant]
                the_type=participants_type[iparticipant]
                if participant is not None:
                    print('participant', participant)
                    if participant['category'] not in counter[the_type].keys():
                        counter[the_type][participant['category']]=0
                    counter[the_type][participant['category']]=counter[the_type][participant['category']]+1
                    if not the_paper['last_revision']['submitter']['email'] in counter[the_type]['list'].keys():
                        counter[the_type]['list'][the_paper['last_revision']['submitter']['email']]=1
                    else:
                        counter[the_type]['list'][the_paper['last_revision']['submitter']['email']]=counter[the_type]['list'][the_paper['last_revision']['submitter']['email']]+1
                else:
                    counter[the_type]['not found']=counter[the_type]['not found']+1
                    
        if contrib is not None:
            if contrib['track'][0:3] not in counter['MC'].keys():
                    counter['MC'][contrib['track'][0:3]]=1
            else:
                    counter['MC'][contrib['track'][0:3]]=counter['MC'][contrib['track'][0:3]]+1

            if contrib['track'][0:7] not in counter['Track'].keys():
                    counter['Track'][contrib['track'][0:7]]=1
            else:
                    counter['Track'][contrib['track'][0:7]]=counter['Track'][contrib['track'][0:7]]+1


            geo_dict=jnf.get_countries_from_contrib(contrib)
            continent=geo_dict['continent']
            countries=geo_dict['countries']     
    
            for cont in continent:
                if cont not in all_continents.keys():
                    all_continents[cont]=1
                else:            
                    all_continents[cont]=all_continents[cont]+1
            for country in countries:
                if country not in all_countries.keys():
                    all_countries[country]=1
                else:            
                    all_countries[country]=all_countries[country]+1              
            else:
                print('Paper is none')
                counter['paper_none']=counter['paper_none']+1

counter['all_continents']=all_continents
counter['all_countries']=all_countries
print(all_continents)
print(all_countries)


if use_online:
    joblib.dump(counter,'stats_papers_author.data')
else:
    counter=joblib.load(fname)


print("############")
            
for the_type in [ 'submitter' , 'speakers' , 'primaryauthors' , 'coauthors' ]:
    print(the_type)
    max_submission=0
    for item in counter[the_type]:
        if item=='list':
            for author in counter[the_type][item]:
                if counter[the_type][item][author]>max_submission:
                    max_submission=counter[the_type][item][author]
                if counter[the_type][item][author]>2:
                    print('>2',author,counter[the_type][item][author])

print('max_submission',max_submission)
                    
for the_type in [ 'submitter' , 'speakers' , 'primaryauthors' , 'coauthors' ]:
    print(the_type)
    for item in counter[the_type]:
        if not (item=='list' or item=='unknown_participants'): 
            print(item,counter[the_type][item])
    sum_country=0
    for country in counter[the_type]['country'].keys():
        sum_country=sum_country+counter[the_type]['country'][country]
    print('sum_country',sum_country)
    for country in counter[the_type]['country'].keys():
        print(country,":",counter[the_type]['country'][country],round(100*counter[the_type]['country'][country]/sum_country,0))
    
    print('---')

'''
#Uncomment this to have the name of all participants with unknown status
for the_type in [ 'submitter' , 'speakers' , 'primaryauthors' , 'coauthors' ]:
    print(the_type)
    for participant in counter[the_type]['unknown_participants']:
        print(participant)
'''

for field in ['in double review','contrib_none','paper_none']:
    print(field,counter[field])


print(counter['all_continents'])
print(counter['all_countries'])

print(counter['MC'])
print(counter['Track'])
sorted_tracks=sorted(counter['Track'])
print(sorted_tracks)

for subMC in counter['Track']:
    if counter['Track'][subMC]>5:
        print(subMC, counter['Track'][subMC], round(counter['Track'][subMC]/284.,2),"%")
        
#Create summary table
allSubMC=[]
for subMC in counter['Track']:
    if not subMC[4:] in allSubMC:
        allSubMC.append(subMC[4:])
        
        
#print(allSubMC)        
#print(sorted(allSubMC))  

fname="stats_by_MC.html"
fhtml=open(fname,"w")
fhtml.write("<html>\n")
fhtml.write("<title>Stats for all LPR abstracts</title>\n")
fhtml.write("<h2>Stats for all LPR abstracts</h2>\n")


fhtml.write('<table border=3>')
fhtml.write('<tr>')
fhtml.write('<td></td>')
totalMCs=[]
for iMC in range(1,9):
    fhtml.write('<td>MC'+str(iMC)+'</td>')
    totalMCs.append(0)
fhtml.write('<td>Total</td>')
fhtml.write('</tr>\n')
allTotal=0
for subMC in sorted(allSubMC):      
    totalSubMC=0
    fhtml.write('<tr>')
    fhtml.write('<td>'+subMC+'</td>')
    for iMC in range(1,9):
        fhtml.write('<td>')
        theSubMC='MC'+str(iMC)+'.'+subMC
        if theSubMC in counter['Track'].keys():
            fhtml.write(str(counter['Track'][theSubMC]))
            totalSubMC=totalSubMC+counter['Track'][theSubMC]
            totalMCs[iMC-1]=totalMCs[iMC-1]+totalSubMC+counter['Track'][theSubMC]
            allTotal=allTotal+counter['Track'][theSubMC]
        fhtml.write('</td>')
    fhtml.write('<td>')
    fhtml.write(str(totalSubMC))
    fhtml.write('</td>')
    fhtml.write('</tr>\n')
fhtml.write('<tr>\n')
fhtml.write('<td>Total</td>')
for iMC in range(1,9):
    fhtml.write('<td>'+str(totalMCs[iMC-1])+'</td>')
fhtml.write('<td>'+str(allTotal)+'</td>')
fhtml.write('</tr>\n')


    
fhtml.write('</table>')
fhtml.write('</html>')

fhtml.close()


#to do:
# check authors
# check in referees list
# check submitter continent

        

