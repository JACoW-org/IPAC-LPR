#!/usr/local/bin/python3

# Record referee reply
# Nicolas Delerue, 3/2023

import jacow_nd_func as jnf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--paper', '-p',   nargs=1, help="The paper for which the answer should be recorded", required=True)
parser.add_argument("--referee", '-r', nargs=1, help="The referee name or id", required=True)
parser.add_argument("--accept", action="store_true", help="Specify that the referee agreed to review the paper")
parser.add_argument("--decline", action="store_true", help="Specify that the referee declined to review the paper")
parser.add_argument("--unavailable", action="store_true", help="Specify that the referee declined to review the paper and is unavailable")
#parser.add_argument("--no-email", nargs=1, help="Do not send email notification")

parser.parse_args()


args = parser.parse_args()

[n_referees,the_refs]=jnf.check_referees_for_paper(args.paper[0])
print("There are ",n_referees," referees for paper ",args.paper[0])
print("Referees: ",the_refs)
n_matches=0
the_ref_id=None
if args.referee is not None:
    for the_ref in the_refs:
        if str(args.referee[0])==str(the_ref[0]) or str(args.referee[0]) in str(the_ref[1]):
            print('Referee ', the_ref,' matches ',args.referee[0])
            the_ref_id=the_ref[0]
            n_matches=n_matches+1
if not n_matches==1:
    if n_matches>1:
        print('Too many matches')
    exit()

action=''
if args.accept or args.decline or args.unavailable:
    if args.accept:
        action='accept'
    elif args.decline:
        action='decline'
    elif args.unavailable:
        action='unavailable'
    else:
        print("Action not known")
        exit()
else:
    print("No action specified")
    exit()

jnf.referee_action(paper_id=args.paper[0],the_ref_id=the_ref_id,action=action)
