import jacow_nd_func as jnf
#import argparse
#import openpyxl
import datetime
#import urllib.parse
#import requests
import time
import matplotlib.pyplot as plt
import numpy as np

import joblib
import random

#Get the submission date of each paper
not_none=0
n_submitted=0
dates_submission=[]
dates_submission_epoch=[]
days_papers_submitted=[]
hours_before_deadline=[]
contrib_id=[]

days_1st_review_received=[]
days_2nd_review_received=[]

days_accepted_1st_round=[]
days_rejected_1st_round=[]
days_judged_1st_tbc=[]

days_accepted_2nd_round=[]
days_rejected_2nd_round=[]

days_resubmitted=[]

days_to_be_corrected_other_reason=[]

days_1st_judgment=[]
days_2nd_judgment=[]

days_papers_decided=[]

check_for_paper_with_no_reviews = True
known_papers_with_no_judgement = [ ] 
papers_resubmitted_and_not_decided = [ ]

papers_submitted_and_not_judged_2nd_round = [ ]
papers_submitted_tbc_and_not_judged_2nd_round = [ ]
papers_marked_to_be_corrected = []

fname='papers_stats.data'
#date_reference=datetime.datetime(2023,4,1,23,59)
date_reference=datetime.datetime(2023,4,1,00,59)

today=(datetime.datetime.now()-date_reference).days

list_vars=[ 'days_papers_submitted'  , 'days_1st_review_received' , 'days_2nd_review_received' , 'days_1st_judgment' , 'days_accepted_1st_round' , 'days_rejected_1st_round' , 'days_judged_1st_tbc' , 'days_resubmitted' , 'days_to_be_corrected_other_reason'   , 'days_2nd_judgment' , 'days_accepted_2nd_round' , 'days_rejected_2nd_round' , 'days_accepted' , 'days_rejected' , 'days_papers_decided' ]

use_online=False
use_online=True
if use_online:
    for the_id in range(500,2800):
        #for the_id in range(500,590):
        contrib=jnf.find_contrib(the_id)
        if contrib is not None:
            not_none=not_none+1
            print('Contrib ', the_id,' is not none; db_id=',contrib['db_id'])
            the_paper=jnf.get_paper_info(contrib['db_id'],use_cache=True,sleep_before_online=0.1)
            #the_paper=None
            if the_paper is None:
                #print("not submitted")
                pass
            else:
                #print("submitted")
                n_submitted=n_submitted+1
                #print(the_paper['revisions'][0]['submitted_dt'])
                the_date=datetime.datetime.strptime(the_paper['revisions'][0]['submitted_dt'].split(".")[0],"%Y-%m-%dT%H:%M:%S")
                #search for reviews dates
                judged=False
                judged_2nd_round=False
                judged_1st_tbc=False
                judged_on_revision=-1
                ireview=0
                date_last_review=0
                date_resubmitted=0
                for the_rev in the_paper['revisions']:
                    if judged and date_resubmitted==0:
                        #print("Resubmitted")
                        #print(the_rev.keys())
                        date_resubmitted=datetime.datetime.strptime(the_rev['submitted_dt'].split(".")[0],"%Y-%m-%dT%H:%M:%S")
                        days_resubmitted.append((date_resubmitted-date_reference).days)
                    for timel in the_rev['timeline']:
                        #print(timel)
                        #print(timel.keys())
                        #print(timel['timeline_item_type'])
                        if timel['timeline_item_type'] == "review":
                            if the_rev['judge'] is not None:
                                if not the_rev['judge']['email'] ==  "delerue@lal.in2p3.fr":
                                    print(the_rev['judge']['email'])
                            the_review_date=datetime.datetime.strptime(timel['created_dt'].split(".")[0],"%Y-%m-%dT%H:%M:%S")
                            date_last_review=the_review_date
                            ireview=ireview+1
                            #print('ireview',ireview,judged)
                            if ireview==1:
                                days_1st_review_received.append((the_review_date-date_reference).days)
                            elif ireview==2:
                                days_2nd_review_received.append((the_review_date-date_reference).days)
                        elif timel['timeline_item_type'] == "judgment":
                            #print(the_rev['state'])
                            if ireview>=2 and not judged:
                                #print("Judged")
                                #print(the_rev.keys())
                                date_judgment=datetime.datetime.strptime(the_rev['judgment_dt'].split(".")[0],"%Y-%m-%dT%H:%M:%S")                                
                                days_1st_judgment.append((date_judgment-date_reference).days)
                                judged=True
                                judged_on_revision=the_paper['revisions'].index(the_rev)
                                #print(the_rev['state'])
                                if the_rev['state'] == "to_be_corrected":
                                    days_judged_1st_tbc.append((date_judgment-date_reference).days)
                                    judged_1st_tbc=True
                                else:
                                    print("State not understood")
                                    exit()
                                    print(the_paper.keys())
                #if ireview==1:
                    #print("*** Paper with only one review ***",the_id)
                if the_paper['state']['name'] == "accepted" or the_paper['state']['name'] == "rejected":
                    date_judgment=datetime.datetime.strptime(the_paper['last_revision']['judgment_dt'].split(".")[0],"%Y-%m-%dT%H:%M:%S")
                    if not judged:
                        #if ireview<2:
                            #print("*** Decided without 2nd review",the_id,ireview,)
                            #if the_id not in [ 2138 , 2667 , 2676 , 2754 ]: 
                                #exit()
                        days_1st_judgment.append((date_judgment-date_reference).days)
                    else:
                        days_2nd_judgment.append((date_judgment-date_reference).days)
                        judged_2nd_round=True

                    if the_paper['state']['name'] == "accepted":
                        if judged:
                            #print("Judged and accepted")
                            days_accepted_2nd_round.append((date_judgment-date_reference).days)
                        else:
                            days_accepted_1st_round.append((date_judgment-date_reference).days)
                    if the_paper['state']['name'] == "rejected":
                        if judged:
                            days_rejected_2nd_round.append((date_judgment-date_reference).days)
                        else:
                            days_rejected_1st_round.append((date_judgment-date_reference).days)
                elif the_paper['state']['name']=="submitted":
                    #print("Resubmission date",date_resubmitted)
                    if date_resubmitted != 0:
                        #print("Resubmission age",(datetime.datetime.now()-date_resubmitted).days)
                        if (datetime.datetime.now()-date_resubmitted).days>0:
                            papers_resubmitted_and_not_decided.append(the_id)

                    if not judged_2nd_round:
                        papers_submitted_and_not_judged_2nd_round.append(the_id)
                        if judged_1st_tbc:
                            papers_submitted_tbc_and_not_judged_2nd_round.append(the_id)
                    pass
                elif the_paper['state']['name']=="to_be_corrected":
                    papers_marked_to_be_corrected.append(the_id)                    
                    if not judged:
                        days_to_be_corrected_other_reason.append((date_judgment-date_reference).days)
                elif len(the_paper['state']['name'])>3:
                    print("Paper state: ",the_paper['state']['name'])
                    exit()    
                if ireview>=2 and not ( judged or the_paper['state']['name'] == "accepted" or the_paper['state']['name'] == "rejected") and (datetime.datetime.now()-datetime.datetime.strptime(str(the_review_date),"%Y-%m-%d %H:%M:%S")).days > 0 and the_id not in known_papers_with_no_judgement:
                    the_paper=jnf.get_paper_info(contrib['db_id'],use_cache=False,sleep_before_online=0.1)
                    if ireview>=2 and not ( judged or the_paper['state']['name'] == "accepted" or the_paper['state']['name'] == "rejected") and (datetime.datetime.now()-datetime.datetime.strptime(str(the_review_date),"%Y-%m-%d %H:%M:%S")).days > 0 and the_id not in known_papers_with_no_judgement:
                        if not the_paper['state']['name']=="to_be_corrected":
                            print('Paper ',the_id,' has two reviews and is not judged. Last review date=',the_review_date,(datetime.datetime.now()-datetime.datetime.strptime(str(the_review_date),"%Y-%m-%d %H:%M:%S")).days)
                            exit()
                    #if judged:
                    #    exit()
                #print(the_date)
                if (ireview==0) and the_paper['state']['name']=="submitted" and check_for_paper_with_no_reviews:
                    print('Paper ',the_id,' has no reviews')
                    exit()
                contrib_id.append(the_id)
                dates_submission.append(the_date)
                dates_submission_epoch.append(int(the_date.strftime('%s')))
                days_papers_submitted.append((the_date-date_reference).days)
                hours_before_deadline.append((the_date-date_reference).seconds/(60*60)+(days_papers_submitted[-1])*24)
                #print('date ',the_date.day," ",the_date.month)
    days_papers_decided=days_accepted_1st_round+days_rejected_1st_round+days_accepted_2nd_round+days_rejected_2nd_round
    days_accepted=days_accepted_1st_round+days_accepted_2nd_round
    days_rejected=days_rejected_1st_round+days_rejected_2nd_round
    list_to_dump=[]
    for the_list in list_vars:
        list_to_dump.append(eval(the_list))
    joblib.dump(list_to_dump,fname)
else:
    list_to_dump=joblib.load(fname)
    for ilist in range(0,len(list_to_dump)):
        exec(list_vars[ilist]+'=list_to_dump[ilist]')
    
days_papers_decided=days_accepted_1st_round+days_rejected_1st_round+days_accepted_2nd_round+days_rejected_2nd_round
#print(days_1st_review_received)
#print(days_1st_judgment)

print('not_none',not_none)
print('n_submitted',n_submitted)
#print('days_papers_submitted',days_papers_submitted)

min_days=min(-70,min(days_papers_submitted)-2)
min_days=min_days-(min_days%7)
max_days=45
bins=np.arange(min_days,max_days,1)
days=bins
n_papers=np.zeros(len(days))
n_reviews=np.zeros(len(days))
n_1st_reviews=np.zeros(len(days))
n_2nd_reviews=np.zeros(len(days))
n_judgments=np.zeros(len(days))

n_vars={}
int_n_vars={}

for the_list in list_vars:
    n_var_name=the_list.replace("days","n")
    n_vars[n_var_name]=np.zeros(len(days))
    int_n_vars[n_var_name]=np.zeros(len(days))
    for the_entry in eval(the_list):
        #print('day',the_entry)
        if the_entry<min_days:
            idx=0
        elif the_entry>max_days:
            idx=list(days).index(max_days-1)
        else:
            idx=list(days).index(the_entry)
        n_vars[n_var_name][idx]=n_vars[n_var_name][idx]+1
    #print(n_vars[n_var_name])
    int_n_vars[n_var_name][0]=n_vars[n_var_name][0]

    for iday in range(1,len(days)):
        int_n_vars[n_var_name][iday]=int_n_vars[n_var_name][iday-1]+n_vars[n_var_name][iday]    
    print(n_var_name,int_n_vars[n_var_name][-1])

print("papers_submitted_and_not_judged_2nd_round",len(papers_submitted_and_not_judged_2nd_round),papers_submitted_and_not_judged_2nd_round)
print("papers_submitted_tbc_and_not_judged_2nd_round",len(papers_submitted_tbc_and_not_judged_2nd_round),papers_submitted_tbc_and_not_judged_2nd_round)
print("papers_marked_to_be_corrected",len(papers_marked_to_be_corrected),papers_marked_to_be_corrected)

random.shuffle(papers_resubmitted_and_not_decided)
print("papers_resubmitted_and_not_decided",len(papers_resubmitted_and_not_decided),papers_resubmitted_and_not_decided)


print('n_papers_decided',int_n_vars['n_papers_decided'][-1])
print("papers_marked_to_be_corrected",len(papers_marked_to_be_corrected))
print("papers_resubmitted_and_not_decided",len(papers_resubmitted_and_not_decided))
print("Sum: ", int_n_vars['n_papers_decided'][-1]+len(papers_marked_to_be_corrected)+len(papers_submitted_and_not_judged_2nd_round))

if 1==0:
    plt.hist(days_papers_submitted,bins=bins)
    plt.title('Days before the deadline')
    plt.xlabel('Days before the deadline')
    plt.ylabel('N submissions/day')
    plt.savefig("submissions_days_papers_submitted.png")
    plt.show(block=False)

if 1==0:
    plt.figure()    
    plt.hist(days_1st_review_received,bins=bins)
    plt.title('Days before the deadline')
    plt.xlabel('Days before the deadline')
    plt.ylabel('N 1st reviews/day')
    plt.savefig("1st_review_by_days.png")
    plt.show(block=False)

    plt.figure()    
    plt.hist(days_1st_review_received+days_2nd_review_received,bins=bins)
    plt.title('Days before the deadline')
    plt.xlabel('Days before the deadline')
    plt.ylabel('N reviews/day')
    plt.savefig("reviews_by_days.png")
    plt.show(block=False)

if 1==0:
    plt.figure()    
    plt.hist(days_1st_judgment,bins=bins)
    plt.title('Days before the deadline')
    plt.xlabel('Days before the deadline')
    plt.ylabel('N judgments/day')
    plt.savefig("judgments_by_days.png")
    plt.show(block=False)

    plt.figure()    
    plt.hist(days_accepted_1st_round,bins=bins)
    plt.title('Days before the deadline')
    plt.xlabel('Days before the deadline')
    plt.ylabel('N judgments/day')
    plt.savefig("judgments_by_days_accept.png")
    plt.show(block=False)

    plt.figure()    
    plt.hist(days_rejected_1st_round,bins=bins)
    plt.title('Days before the deadline')
    plt.xlabel('Days before the deadline')
    plt.ylabel('N judgments/day')
    plt.savefig("judgments_by_days_reject.png")
    plt.show(block=False)

    plt.figure()    
    plt.hist(days_judged_1st_tbc,bins=bins)
    plt.title('Days before the deadline')
    plt.xlabel('Days before the deadline')
    plt.ylabel('N judgments/day')
    plt.savefig("judgments_by_days_tbc.png")
    plt.show(block=False)


if 1==1:
    fig=plt.figure(figsize=(8, 6), dpi=100)
    #draw vertical lines
    #for the_line in [ [ 0 , 'Submission deadline' , "red" ] , [ 37 , 'Start of IPAC' , "green" ] , [ today , 'Today' , "cyan" ] ]:
    for the_line in [ [ 0 , 'Submission deadline' , "red" ] , [ 37 , 'Start of IPAC' , "green" ] ]:
        plt.plot( [the_line[0] , the_line[0]] , [0, 300], label=the_line[1] , color= the_line[2] )
    for the_list in list_vars:
        n_var_name=the_list.replace("days","n")    
        plt.plot(days,int_n_vars[n_var_name],label=the_list.replace("days_","").replace("_"," ")+" = "+str(int_n_vars[n_var_name][-1]))
    plt.title("IPAC'23 Light Peer Review progress")
    plt.xlabel('Days before the deadline')
    plt.ylabel('Papers')
    ax = plt.gca()
    ax.set_xticks(np.arange(min_days,max_days,7))
    ax.set_xticks(np.arange(min_days,max_days,1),minor=True)
    plt.minorticks_on()
    plt.grid()
    plt.legend()
    plt.savefig("submissions_days_papers_submitted_integrated.png")
    plt.show(block=False)

#plot the hours
if 1==0:
    plt.figure()
    min_hours=-120
    max_hours=2
    bins=np.arange(min_hours,max_hours,1)
    #print('bins',bins)
    plt.hist(hours_before_deadline,bins=bins)
    plt.title('Hours before the deadline')
    plt.xlabel('Hours before the deadline')
    plt.ylabel('N submissions/hours')
    #plt.xlim([-30,2])
    plt.savefig("submissions_hours_before_deadline.png")
    plt.show(block=False)

    hours=bins
    n_papers=np.zeros(len(hours))
    for the_entry in hours_before_deadline:
        if not the_entry> max_hours:
            if the_entry< min_hours:
                idx=0
            else:
                idx=list(hours).index(int(the_entry))
            n_papers[idx]=n_papers[idx]+1

    #print(n_papers)
    for ihours in range(1,len(hours)):
        n_papers[ihours]=n_papers[ihours-1]+n_papers[ihours]

    plt.figure()    
    plt.plot(hours,n_papers)
    plt.title('Hours before the deadline')
    plt.xlabel('Hours before the deadline')
    plt.ylabel('N submissions')
    plt.grid()
    plt.ylim([0 , 300])
    plt.savefig("submissions_hours_before_deadline_integrated.png")

plt.show()
    
#end of plotting
#List by hour of submission
if 1==0:

    zipped=zip(hours_before_deadline,contrib_id)
    sorted_lists=sorted(zipped)
    [ hours_before_deadline_sorted , contrib_id_sorted ] = zip(*sorted_lists)

    print(hours_before_deadline_sorted)
    print(contrib_id_sorted)
    skip_list=[]
    for isubmit in range(0,len(hours_before_deadline_sorted)):
        print(isubmit,hours_before_deadline_sorted[isubmit],contrib_id_sorted[isubmit])
        if isubmit>250:
            skip_list.append(contrib_id_sorted[isubmit])
    print(skip_list)
