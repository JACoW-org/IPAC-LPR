#!/usr/local/bin/python3

# Assign referees to papers
# Nicolas Delerue, 3/2023
# Significant update May 2025

import sys
import jacow_nd_func as jnf
import reviewer_functions as revf
import email_func as ef 
import papers_functions as pf
import argparse
#import openpyxl
import datetime
#import urllib.parse
#import requests
import params



parser = argparse.ArgumentParser()
parser.add_argument('--paper',  '-p', nargs=1, help="The paper to which the referee should be assigned", required=True)
parser.add_argument("--referee", '-r',  nargs=1, help="The referee id to be assigned to the paper", required=True)
parser.add_argument("--override", action="store_true", help="Override limits on paper per referee or referees per paper")
parser.add_argument("--no-email", action="store_true", help="Does not send email")
parser.add_argument("--assign-only", action="store_true", help="Assign but does not send email")
parser.add_argument("--unassign", action="store_true", help="Unassigns the referee from the paper")
parser.add_argument("--overdue", action="store_true", help="Unassigns the referee from the paper and records him as unavailable")

#parser.parse_args()


args = parser.parse_args()

print("Referee "+args.referee[0]+"; Paper "+args.paper[0])

#Get referee info
ref_dict=revf.get_reviewer_by_id(args.referee[0])


if ref_dict is None:
    print("ref_dict is None for ",args.referee[0])
    exit()
referee_db_id=args.referee[0]
print("Reviewer name: ",ref_dict["full_name"])

#revlist=revf.get_reviewer_list()
#print(revlist)
if referee_db_id not in revf.get_reviewer_list():
    print("Reviewer is not in the reviewer list!!!")
    print(f"You must add him or her in the team of content_reviewers at https://indico.jacow.org/event/{params.event_id}/manage/papers/")
    


#Get contribution info
contrib=pf.get_contrib_info(args.paper[0])
if 'db_id' not in contrib.keys():
    contrib['db_id']=contrib['id']

if contrib is None:
    print("Contrib ",args.paper[0]," seems not to exist!!! get_contrib_info returned None")
    sys.exit()
else:
    pass
    #print("Paper ",args.paper[0]," is not None")


if args.unassign:
    revf.unassign_reviewer(contrib['db_id'],int(args.referee[0]))
    print("Unassigned")
    sys.exit()

if args.overdue:
    print("Overdue not yet implemented")
    jnf.referee_action(args.paper[0],int(args.referee[0]),"overdue")
    exit()


#Check that the referee is not one of the authors
ref_name=ref_dict["full_name"]
#print('contrib',contrib.keys())
print('Contribution title:',contrib['title'])
#print('Contribution desc:',contrib['description'])
#print('contrib',contrib['id'])
#print('contrib',contrib['persons'])
paper=pf.get_paper_info(contrib['db_id'])

if paper is None:
    print("Paper ",args.paper[0]," seems not to exist!!! get_paper_info returned None")
    exit()
else:
    print("Paper ",args.paper[0]," is not None")
#print(paper.keys())
#print(paper['revisions'][0].keys())
print("Paper title", paper['contribution']['title'])
#print(contrib['persons'])
for speak in contrib['persons']:
    #print(speak.keys())
    if 'full_name' in speak.keys() and ref_name.lower() == speak['full_name'].lower() or 'fullName' in speak.keys() and ref_name.lower() == speak['fullName'].lower():
        print(type,speak['fullName'],speak['first_name'],speak['last_name'],speak['affiliation'])
        print("Referee's name matches one of the authors name. Not assigned.")
        exit()


n_papers=0
print("Check number of paper to reviewer to be done")    

'''
print(paper.keys())
print(paper['can_review'])
print(contrib.keys())
print(paper['contribution'].keys())
print(paper['revisions'][-1].keys())
print(paper['revisions'][-1]['reviewer_data'])
print(paper['revisions'][-1]['reviewer_data'].keys())
'''
all_assigned_reviewers=[]
all_current_reviewers=[]
all_rejected_reviewers=[]

for rev in paper['revisions']:
    #print(len(rev['timeline']))
    for tim in rev['timeline']:
        #print(tim.keys())
        if 'text'in tim.keys():            
            if "Assigned reviewer" in tim['text']:
                revtxt=tim['text'].split(" ")
                all_assigned_reviewers.append(revtxt[2])
                all_current_reviewers.append(revtxt[2])
                #print(tim['text'])
            elif "Unassigned reviewer" in tim['text']:
                revtxt=tim['text'].split(" ")
                pos=99
                while (pos>=0):
                    try:
                        pos=all_current_reviewers.index(revtxt[2])
                    except:
                        pos=-1
                    if pos>=0:
                        all_current_reviewers.pop(pos)
                    #print(pos)
all_current_reviewers=list(set(all_current_reviewers))

has_warning=False
if referee_db_id in all_current_reviewers:
    print("*** Warning *** Reviewer is already assigned to this paper.")
    has_warning=True
if len(all_current_reviewers)>=2:
    print("*** Warning *** This paper has already ",len(all_current_reviewers)," reviewers.")
    has_warning=True

#Checking assignements/unassignements for this paper


#[n_referees,same_paper]=jnf.check_referees_for_paper(args.paper[0])
#print('n_referees',n_referees,'same_paper',same_paper)
#papers_for_ref=jnf.check_papers_for_referee(int(args.referee[0]))
#n_papers=papers_for_ref['n_papers']
#same_referee=""
#for sr in papers_for_ref['list_papers']:
#    print('sr',sr)
#    same_referee=same_referee+sr+"\n"
    

   
#if len(same_referee)>1:
#    print("The same referee already has the following papers",n_papers)
#    print(same_referee)

#print('can_referee_get_additional_paper(ref_id)',args.referee[0],jnf.can_referee_get_additional_paper(args.referee[0]))

##check that the paper has not been declined
#[n_declined,list_declined]=jnf.check_paper_for_declined(args.paper[0])
#for decl in list_declined:
#    print("This paper ",str(args.paper[0])," was declined by",decl)
#    if int(decl)==int(args.referee[0]):
#        print("This referee already declined this paper!")
#        exit()


        

if has_warning: 
    if args.override:
        print("Overridding warnings")
    else:
        print("Use --override to override these warnings")
        sys.exit()


#Assign
#print(contrib['db_id'])
#print(referee_db_id)
revf.assign_reviewer(contrib['db_id'],referee_db_id)
print("assigned")

if not args.assign_only:
    the_deadline=(datetime.datetime.today()+ datetime.timedelta(days=params.days_to_review_paper)).strftime("%d/%m/%Y")
    
    replace_dict={}
    replace_dict["name"]=ref_dict["full_name"]
    replace_dict["title"]=contrib['title']
    replace_dict["paper_id"]=contrib['db_id']
    replace_dict["id"]=contrib['db_id']
    replace_dict["url_paper"]=f'https://indico.jacow.org/event/{params.event_id}/papers/'+str(contrib['db_id'])
    replace_dict["abstract"]=contrib['description']
    replace_dict["deadline"]=the_deadline

    
    if args.no_email:
        print('Requested not to send emails')
    else:
        if n_papers==0:
            ef.email_file(ref_dict["email"],"messages/message_referee_request.txt",replace_dict=replace_dict,show_message=True,send_me_a_copy=True)
        else:
            ef.email_file(ref_dict["email"],"messages/message_referee_additional_request.txt",replace_dict=replace_dict,show_message=True,send_me_a_copy=True)
            
