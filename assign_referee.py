#!/usr/local/bin/python3

# Assign referees to papers
# Nicolas Delerue, 3/2023
#Significant update May 2025

#import sys
import jacow_nd_func as jnf
import reviewer_functions as revf
import email_func as ef 
import argparse
import openpyxl
import datetime
import urllib.parse
import requests
import params

parser = argparse.ArgumentParser()
parser.add_argument('--paper',  '-p', nargs=1, help="The paper to which the referee should be assigned", required=True)
parser.add_argument("--referee", '-r',  nargs=1, help="The referee id to be assigned to the paper", required=True)
parser.add_argument("--override", action="store_true", help="Override limits on paper per referee or referees per paper")
parser.add_argument("--no-email", action="store_true", help="Does not send email")
parser.add_argument("--assign-only", action="store_true", help="Assign but does not send email")
#parser.add_argument("--unassign", action="store_true", help="Unassigns the referee from the paper")
#parser.add_argument("--overdue", action="store_true", help="Unassigns the referee from the paper and records him as unavailable")

parser.parse_args()


args = parser.parse_args()

print("Assigning referee "+args.referee[0]+" to paper "+args.paper[0])

#Get referee info
ref_dict=revf.get_referee_by_id(int(args.referee[0]))

if ref_dict is None:
    print("ref_dict is None for ",int(args.referee[0]))
    exit()
referee_db_id=int(args.referee[0])

print("To be done: check that reviewer is in the pool")
exit()


#Get contribution info
contrib=jnf.find_contrib(the_id=args.paper[0])

if args.unassign:
    print("Unassign not yet implemented")
    exit()
    revf.unassign_reviewer(contrib['db_id'],int(args.referee[0]))
    print("unassigned")
    exit()

if args.overdue:
    print("Overdue not yet implemented")
    jnf.referee_action(args.paper[0],int(args.referee[0]),"overdue")
    exit()

n_papers=0
print("Check number of paper to reviewer to be done")    
#[n_referees,same_paper]=jnf.check_referees_for_paper(args.paper[0])
#print('n_referees',n_referees,'same_paper',same_paper)
#papers_for_ref=jnf.check_papers_for_referee(int(args.referee[0]))
#n_papers=papers_for_ref['n_papers']
#same_referee=""
#for sr in papers_for_ref['list_papers']:
#    print('sr',sr)
#    same_referee=same_referee+sr+"\n"
    

#ref_line=jnf.referee_data_file_get_line(int(args.referee[0]))
#print(ref_line)
#print('len(same_paper)', len(same_paper))
#if n_referees>0:
#    print("The same paper already has the following referees",n_referees)
#    print(same_paper)
#    for other_ref in same_paper:
#        if int(other_ref[0])==int(args.referee[0]):
#            print("This referee is already assigned to this paper!!!")
#            if not args.assign_only:
#                exit()
   
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

#Check that the referee is not one of the authors
ref_name=ref_dict["full_name"]
print("Referee name is", ref_name)
paper=jnf.get_paper_info(contrib['db_id'])
if paper is None:
    print("Paper ",args.paper[0]," seems not to exist!!! get_paper_info returned None")
    exit()
else:
    print("Paper ",args.paper[0]," is not None")
for type in [ 'speakers' , 'primaryauthors' , 'coauthors']:
    for speak in contrib[type]:
        if ref_name.lower() == (speak['first_name'].lower()+" "+speak['last_name'].lower()):
            print(type,speak['fullName'],speak['first_name'],speak['last_name'],speak['affiliation'])
            print("Referee's name matches one of the authors name. Not assigned.")
            exit()

if args.assign_only:
    print("Re-assigning referees")
    print("not implemented")
    exit()
#    print([ int(sr[0]) for sr in same_paper])
#    if not int(args.referee[0]) in [int(sr[0]) for sr in same_paper]:
#        print("This referees has not yet been assigned to this paper")
#        print([int(sr[0]) for sr in same_paper])
#        exit()
        
#if not jnf.can_referee_get_additional_paper(args.referee[0]) or n_referees>=2:
#    if args.override:
#        print("Overriding paper limitation")
#    elif args.assign_only:
#        pass
#    else:
#        print("Exiting, use --override to force assignation")
#        exit()

#Assign
#print(contrib['db_id'])
#print(referee_db_id)
revf.assign_reviewer(contrib['db_id'],referee_db_id)
print("assigned")

if not args.assign_only:
    the_deadline=(datetime.datetime.today()+ datetime.timedelta(days=params.days_to_review_paper)).strftime("%d/%m/%Y")
    
    if args.no_email:
        print('Requested not to send emails')
    else:
        if n_papers==0:
            ef.send_email(referee_id=args.referee[0],paper_id=args.paper[0],url=urlform,msgfile='message_referee_request_v2.txt',deadline=the_deadline)
        else:
            ef.send_email(referee_id=args.referee[0],paper_id=args.paper[0],url=urlform,msgfile='message_referee_additional_request.txt',deadline=the_deadline)
            
