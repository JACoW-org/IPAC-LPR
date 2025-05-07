#!/usr/local/bin/python3

# Extracts the evaluation report from a single paper
# Nicolas Delerue, 5/2025


import datetime
import sys
import argparse
import papers_functions as pf

    

parser = argparse.ArgumentParser()
parser.add_argument('--paper',  '-p', nargs=1, help="The paper for which the report shold be generated", required=True)
parser.add_argument('--hide-reviewers',  action="store_true", help="Hiide reviewer information")
parser.add_argument('--export',  action="store_true", help="Save the report in a file named report_xxx.txt where xxx is the paper db_id")

args = parser.parse_args()

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

the_paper=pf.get_paper_info(contrib['db_id'])

if the_paper is None:
    print("Paper ",args.paper[0]," seems not to exist!!! get_paper_info returned None")
    exit()
else:
    print("Paper ",args.paper[0]," is not None")
#print(the_paper.keys())
print("Paper title", the_paper['contribution']['title'])

#report
print(" ======================================= ")

if args.export:
    fname="report_"+str(args.paper[0])+".txt"
    fsave=open(fname,"w")


def print_and_save(txt):
    print(txt)
    if args.export:
        fsave.write(txt+"\n")        


print_and_save("ID: "+str( the_paper['contribution']['id']))
print_and_save("Title: "+ the_paper['contribution']['title'])
print_and_save("Submitter:  "+ the_paper['revisions'][0]['submitter']['full_name'])
print_and_save("affiliation: "+ the_paper['revisions'][0]['submitter']['affiliation'])
print_and_save("email address: "+ the_paper['revisions'][0]['submitter']['email'])

for irevision in range(0,len(the_paper['revisions'])):
    print_and_save("Revision "+str(irevision+1))
    the_rev=the_paper['revisions'][irevision]
    print_and_save("Date submitted:"+str( the_rev['submitted_dt']))
    #print_and_save(len( the_rev['timeline']))
    for itimeline in range(len( the_rev['timeline'])):
        spacer="    "
        the_item=the_rev['timeline'][itimeline]
        #print_and_save(the_item['timeline_item_type'])
        if the_item['timeline_item_type']=="review":
            print_and_save(spacer+"Review:")
            spacer=spacer+"   "
            print_and_save(spacer+"Created: "+str( the_item['created_dt']))
            if not args.hide_reviewers:
                print_and_save(spacer+"Reviewer: "+ the_item['user']['full_name']+"  "+the_item['user']['affiliation']+"  "+the_item['user']['affiliation_meta']['country_name'])
            spacer=spacer+"   "
            for irat in range(len(the_item['ratings'])):
                the_rat=the_item['ratings'][irat]
                if not "PRAB" in the_rat['question']['title']:
                    print_and_save(spacer+ the_rat['question']['title'])
                    print_and_save(spacer+ str(the_rat['value']))
        if the_item['timeline_item_type']=="judgment":
            #print_and_save(the_rev.keys())
            #print_and_save(the_rev['judge']['full_name'])
            print_and_save(spacer+"Judgement")
            spacer=spacer+"   "
            if "IoP proceedings" in the_rev['judgment_comment']:
                print_and_save(spacer+"Accepted - file to be resubmitted in the correct format")
            elif "IoP guidelines" in the_rev['judgment_comment']:
                print_and_save(spacer+"File format to be corrected")                        
            else:
                print_and_save(spacer+"Decision "+ the_rev['state'])
                print_and_save(spacer+"Decision comment"+ the_rev['judgment_comment'])
            
print_and_save("   ")

if args.export:
    fsave.close()
    
