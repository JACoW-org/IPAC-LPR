#!/usr/local/bin/python3

# Check for new submissions and suggest referees
# Nicolas Delerue, 3/2023

def printv(txt):
    print(txt," : ",eval(txt))

import jacow_nd_func as jnf
import requests
import time
import urllib.parse

papers_without_referees=[]
papers_with_one_referees=[]
papers_without_review=[]
papers_with_one_review=[]
papers_with_n_referees= [ 0, 0, 0, 0, 0, 0 ]
papers_with_n_reviews=[0, 0, 0, 0, 0 ]
skip_list=[1979, 1619, 1440, 2156, 790, 2134, 1144, 1499, 860, 2732, 678, 1478, 2112, 2225, 1498, 2046, 676, 824, 2754, 2635, 661, 1150, 2727, 2511, 2213, 2154, 928, 1504, 1906, 2054, 2138, 1243, 1575, 1245, 2514, 2442, 1846, 1505]
skip_list=[ ]
todo=jnf.all_actions_todo
papers_with_missing_referees=[ ]
n_actions_todo=0
#TrackList=[ 'MC6' , 'MC7' ]         
#TrackList=[ 'MC6' , 'MC7' , 'MC8' ]         
#TrackList=[ 'MC5' ]         
#TrackList=[ 'MC6' ]         
#TrackList=[ 'MC8' ]         
#TrackList=[ 'MC5' , 'MC6' , 'MC7' , 'MC8' ]         
TrackList=[ 'MC1', 'MC2' , 'MC3', 'MC4', 'MC5' , 'MC6' , 'MC7' , 'MC8' ]         

print('### Update files if needed ###')
jnf.load_referee_files()        
jnf.load_contribs()

print('### Check All papers ###')
jnf.check_all_papers()
jnf.check_double_reviews_validated()

print('### Check new replies ###')
print("We bypass reading replies")
if 1==0:
    urlmark="http://nicolas.delerue.org/ipac23/referee_answer.php"
    payload = {'check': 'checking file' , 'answer':'check'}
    data = requests.post(urlmark,data=payload)
    #print(data)
    #print(data.text)
    if not data.status_code == 200:
        print("Error makring the assignement file")
    else:
        print("File marked")

    urlreplies="http://nicolas.delerue.org/ipac23/referee_reply.txt"
    data = requests.get(urlreplies)
    if not data.status_code == 200:
        print("Error getting the replies")
    else:
        #print(data.text)
        lines=data.text.split("\n")
        check_found=False
        skip_rest=False
        for line in reversed(lines):
            vals=line.split(";")
            if len(vals)>2 and not skip_rest:
                print('vals',vals)
                v1=vals[1].split(":")
                if v1[0]=='check':
                    if not check_found:
                        check_found=True
                    else:
                        skip_rest=True
                        print('Skipping the rest')
                        time.sleep(1)
                elif v1[0]=='ref':
                    referee_id=int((int(v1[1])/7)/10000)
                    paper_id=int((int(v1[1])/7)%10000)
                    print('referee_id',referee_id,'paper_id',paper_id)
                    v2=vals[2].split(":")
                    if not ( v2[0]=='answer' or v2[0]=='add_answer' or v2[0]=='origin'):
                        print("Not understood v2")
                        print(vals)
                        print(v2[0])
                        exit()
                    elif v2[0]=='answer':                    
                        action=''
                        if v2[1]=='yes':
                            action='accept'
                        elif v2[1]=='other_field':                    
                            action='decline'
                        elif v2[1]=='unavailable':
                            action='unavailable'
                        print('referee_id',referee_id,'paper_id',paper_id,'action',action)
                        time.sleep(4)
                        jnf.referee_action(paper_id=paper_id,the_ref_id=referee_id,action=action)
                    elif v2[0]=='origin':                    
                        print('origin',line,vals[3])
                        v3=vals[3].split(":")
                        print(v3)
                        if v3[0] == "addtime":
                            v3=vals[6].split(":")
                            print(v3)
                        if not v3[0] == "add_answer":
                            exit()
                        else:
                            data={}
                            if v3[1]=="yes":
                                print('yes')
                                data['accepting_papers']='yes'
                                jnf.referee_data_file_write_line(referee_id,data)
                            elif v3[1]=="no":
                                data['accepting_papers']='no'
                                jnf.referee_data_file_write_line(referee_id,data)
                                print('no')
                            else:
                                exit()
                else:
                    print("Not understood v1")
                    print(vals)
                    exit()
                

print('### Check new contributions ###')
if len(jnf.all_actions_todo)>0:
    jnf.all_actions_todo.append("Check new contributions")
contribs=jnf.submitted_contribs()
jnf.load_affiliations_countries_file()
for the_contrib_id in contribs:
    contrib=jnf.find_contrib(the_db_id=the_contrib_id)
    [n_referees,same_paper]=jnf.check_referees_for_paper(contrib['id'])
    print('Contrib #',contrib['id'],'has already ',n_referees,' referees and ',jnf.n_reviews[contribs.index(the_contrib_id)],' reviews')
    #check that there is a pdf of docx file
    the_paper=jnf.get_paper_info(contrib['db_id'])
    readable_file_found=False
    for the_file in the_paper['last_revision']['files']:
        if ".docx" in the_file['filename'].lower() or ".pdf"in the_file['filename'].lower():
            readable_file_found=True
    if not readable_file_found:
        print("Contribution ",contrib['id']," seems to have no readable file")
        for the_file in the_paper['last_revision']['files']:
            print('filename',the_file['filename'])
        #todo.append("#### \nContrib: "+ contrib['id'] +" Check for missing readable file url: https://indico.jacow.org/event/41/papers/"+str(contrib['db_id'])+"/")
        #n_actions_todo=n_actions_todo+1

    if the_paper is not None and not jnf.check_paper_in_double_reviews(contrib['id']):
        papers_with_n_referees[n_referees]=papers_with_n_referees[n_referees]+1    
        papers_with_n_reviews[jnf.n_reviews[contribs.index(the_contrib_id)]]=papers_with_n_reviews[jnf.n_reviews[contribs.index(the_contrib_id)]]+1
        if len(the_paper)>10:
            if jnf.n_reviews[contribs.index(the_contrib_id)]==0:
                papers_without_review.append(contrib['id'])
            if jnf.n_reviews[contribs.index(the_contrib_id)]==1:
                papers_with_one_review.append(contrib['id'])
    print('Track', contrib['track'])
    if contrib['id'] in skip_list:
        print('Skipping this contribution...')
    if (n_referees<2) and not contrib['id'] in skip_list and contrib['track'][0:3] in TrackList and the_paper is not None:
        print('###')
        print('Contribution with less than 2 referees:',contrib['id'])
        
        geo_dict=jnf.get_countries_from_contrib(contrib)
        continent=geo_dict['continent']
        countries=geo_dict['countries']
        print('title',contrib['title'])
        print('track',contrib['track'])
        print('id',contrib['id'])
        print('---')
        #print('Continent ',continent)
        #print('Continent ',set(continent))
        print('Continent ',list(set(continent)))
        if (len(list(set(continent)))>1):
            print('Multiple continents')
            #exit()
        #We bypass this stage for now
        print("Referee asignment bypassed")
        #referees=jnf.randomly_suggest_two_referees(contrib['track'],list(set(continent)),paper_id=contrib['id'],n_referees_needed=2-n_referees)
        referees=None
        if referees is None or len(referees)==0:
            print("Unable to assign referees for this paper")
            papers_with_missing_referees.append('===')
            papers_with_missing_referees.append('id: '+ contrib['id'] +': '+contrib['title'] )
            if len(contrib['speakers'])>0:
                print("Affiliation", contrib['speakers'][0]['affiliation'])
                papers_with_missing_referees.append(contrib['speakers'][0]['affiliation'])
            papers_with_missing_referees.append(list(set(countries)))
            papers_with_missing_referees.append(contrib['track'])
            papers_with_missing_referees.append("url: https://indico.jacow.org/event/41/papers/"+str(contrib['db_id'])+"/")
            papers_without_referees.append(contrib['id'])
            [n_declined,list_declined]=jnf.check_paper_for_declined(contrib['id'])
            papers_with_missing_referees.append("This paper "+str(contrib['id'])+" was declined by "+str(n_declined)+" referees")
            for decl in list_declined:
                print("This paper ",str(contrib['id'])," was declined by",decl)
                papers_with_missing_referees.append("Declined by "+str(decl))
        else:
            for the_ref in referees:
                print(jnf.get_referee_by_id(the_ref))
            if len(referees)==1:
                papers_with_one_referees.append(contrib['id'])
            print('---')
            if (len(referees)>0):
                jnf.all_actions_todo.append('===')
                jnf.all_actions_todo.append('id: '+ contrib['id'] +': '+contrib['title'] )
                if len(contrib['speakers'])>0:
                    print("Affiliation", contrib['speakers'][0]['affiliation'])
                    jnf.all_actions_todo.append(contrib['speakers'][0]['affiliation'])
                jnf.all_actions_todo.append(list(set(countries)))
                jnf.all_actions_todo.append(contrib['track'])
                jnf.all_actions_todo.append("url: https://indico.jacow.org/event/41/papers/"+str(contrib['db_id'])+"/")
            for the_ref in referees:
                refdata=jnf.get_referee_by_id(the_ref)
                print(refdata[1])
                jnf.all_actions_todo.append('Referee '+refdata[1])
            print('To notify the selected referees type:')
            if (len(referees)==2):
                jnf.all_actions_todo.append('./assign_referee.py --paper '+str(contrib['id'])+' --referee '+str(referees[0])+' && ./assign_referee.py --paper '+str(contrib['id'])+' --referee '+str(referees[1]))
                n_actions_todo=n_actions_todo+1
            elif (len(referees)==1):
                jnf.all_actions_todo.append('./assign_referee.py --paper '+str(contrib['id'])+' --referee '+str(referees[0]))
                n_actions_todo=n_actions_todo+1
            #else:
                #jnf.all_actions_todo.append("No referee:")

                
print('### Check all papers data ###')
if len(jnf.all_actions_todo)>0:
    jnf.all_actions_todo.append("Check all papers")
jnf.check_all_papers()
                
print('### Check overdue referee replies ###')
print("We bypass referees reminder")
#jnf.remind_referees()
    

print('********')
print("Papers with missing referees:")
for line in papers_with_missing_referees:
    print(line)
    
print('********')
print("To do list:")
know_issues = [ ]
#[ 824 , "Waiting for resubmission " ] , [ 2024 , "Waiting for resubmission " ] ,
#[ 2213 , "Wait for 3rd review" ] , [ 995 , "Waiting for resubmission " ] , [ 1383 , "Waiting for resubmission " ] , [ 1400 , "Waiting for resubmission " ] ]
print('know_issues',know_issues)
#print('jnf.all_actions_todo',jnf.all_actions_todo)
for line in jnf.all_actions_todo:
    for issue in know_issues:
        if str(issue[0]) in line:
            print("know issue")
            line=""
        if len(line)>0:
            if str(issue[0]) in line[1]:
                print("know issue")
                line=""
    print(line)
    
print('N submitted contributions ',len(contribs))
print('n_actions_todo',n_actions_todo)
if (len(jnf.no_country_affiliation)>0):
    print('Affiliations with no country',list(set(jnf.no_country_affiliation)))
if len(skip_list)>0:
    print('Skip list',skip_list)
#if (len(papers_without_referees)>0):
print('papers_without_referees',len(papers_without_referees),papers_without_referees)
print('papers_with_one_referees',len(papers_with_one_referees),papers_with_one_referees)
print('papers_without_review',len(papers_without_review),papers_without_review)
print('papers_with_one_review',len(papers_with_one_review),papers_with_one_review)
print('papers_with_n_referees',papers_with_n_referees)
print('papers_with_n_reviews',papers_with_n_reviews)

jnf.print_contrib_stats()
jnf.print_stats_double_reviews()
