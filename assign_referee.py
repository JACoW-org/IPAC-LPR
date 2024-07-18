#!/usr/local/bin/python3

# Assign referees to papers
# Nicolas Delerue, 3/2023

import jacow_nd_func as jnf
import email_func as ef 
import argparse
import openpyxl
import datetime
import urllib.parse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--paper',  '-p', nargs=1, help="The paper to which the referee should be assigned", required=True)
parser.add_argument("--referee", '-r',  nargs=1, help="The referee id to be assigned to the paper", required=True)
parser.add_argument("--override", action="store_true", help="Override limits on paper per referee or referees per paper")
parser.add_argument("--no-email", action="store_true", help="Does not send email")
parser.add_argument("--assign-only", action="store_true", help="Does not send email")
parser.add_argument("--unassign", action="store_true", help="Unassigns the referee from the paper")
parser.add_argument("--overdue", action="store_true", help="Unassigns the referee from the paper and recors him as unavailable")

parser.parse_args()


args = parser.parse_args()

print("Assigning referee "+args.referee[0]+" to paper "+args.paper[0])

#Get referee info
[ref_name, ref_email, ref_affiliation, ref_country, ref_MC, ref_ID]=jnf.get_referee_by_id(int(args.referee[0]))

referee_db_id=jnf.get_referee_db_id_from_id(int(args.referee[0]))
if referee_db_id is None:
    print("referee_db_id is None for ",int(args.referee[0]))
    exit()
    
#Get contribution info
contrib=jnf.find_contrib(the_id=args.paper[0])

if args.unassign:
    jnf.unassign_referee(contrib['db_id'],referee_db_id)
    print("unassigned")
    exit()

if args.overdue:
    jnf.referee_action(args.paper[0],int(args.referee[0]),"overdue")
    exit()
    
[n_referees,same_paper]=jnf.check_referees_for_paper(args.paper[0])
print('n_referees',n_referees,'same_paper',same_paper)
papers_for_ref=jnf.check_papers_for_referee(int(args.referee[0]))
n_papers=papers_for_ref['n_papers']
same_referee=""
for sr in papers_for_ref['list_papers']:
    print('sr',sr)
    same_referee=same_referee+sr+"\n"
    

ref_line=jnf.referee_data_file_get_line(int(args.referee[0]))
print(ref_line)
print('len(same_paper)', len(same_paper))
if n_referees>0:
    print("The same paper already has the following referees",n_referees)
    print(same_paper)
    for other_ref in same_paper:
        if int(other_ref[0])==int(args.referee[0]):
            print("This referee is already assigned to this paper!!!")
            if not args.assign_only:
                exit()
   
if len(same_referee)>1:
    print("The same referee already has the following papers",n_papers)
    print(same_referee)

print('can_referee_get_additional_paper(ref_id)',args.referee[0],jnf.can_referee_get_additional_paper(args.referee[0]))

#check that the paper has not been declined
[n_declined,list_declined]=jnf.check_paper_for_declined(args.paper[0])
for decl in list_declined:
    print("This paper ",str(args.paper[0])," was declined by",decl)
    if int(decl)==int(args.referee[0]):
        print("This referee already declined this paper!")
        exit()

#Check that the referee is not one of the authors
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
    print([ int(sr[0]) for sr in same_paper])
    if not int(args.referee[0]) in [int(sr[0]) for sr in same_paper]:
        print("This referees has not yet been assigned to this paper")
        print([int(sr[0]) for sr in same_paper])
        exit()
        
if not jnf.can_referee_get_additional_paper(args.referee[0]) or n_referees>=2:
    if args.override:
        print("Overriding paper limitation")
    elif args.assign_only:
        pass
    else:
        print("Exiting, use --override to force assignation")
        exit()

#Assign
#print(contrib['db_id'])
#print(referee_db_id)
jnf.assign_referee(contrib['db_id'],referee_db_id)
print("assigned")

ref_data={}
ref_data['accepting_papers']='wait'
if ref_line['papers_assigned'] is None:
    ref_line['papers_assigned']=0
ref_data['papers_assigned']=ref_line['papers_assigned']+1
jnf.referee_data_file_write_line(int(args.referee[0]),ref_data)

if not args.assign_only:
    the_deadline=(datetime.datetime.today()+ datetime.timedelta(days=10)).strftime("%d/%m/%Y")
    urlform=jnf.assign_referee_in_file(contrib,args.referee[0],ref_name,the_deadline)
    
    if args.no_email:
        print('no email')
    else:
        if n_papers==0:
            ef.send_email(referee_id=args.referee[0],paper_id=args.paper[0],url=urlform,msgfile='message_referee_request_v2.txt',deadline=the_deadline)
        else:
            ef.send_email(referee_id=args.referee[0],paper_id=args.paper[0],url=urlform,msgfile='message_referee_additional_request.txt',deadline=the_deadline)
            
