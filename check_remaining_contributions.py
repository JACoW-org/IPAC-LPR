#Script used for the closing of the LPR to check the statu of remainig papers 

import jacow_nd_func as jnf

#Check remaining contributions
remaining_contributions=[]

#Either with check how many times a paper was declined or check the secound round status of the paper 
check_for_nref_declined=False

sorted_by_ref=[]

suggested_accept=[]
suggested_reject=[]
not_yet_suggested=[]

record_resubmit=[]

for iref in range(0,15):
    sorted_by_ref.append([ ])

for the_id in remaining_contributions: 
    contrib=jnf.find_contrib(the_id)
    if check_for_nref_declined:
        [n_declined,list_declined]=jnf.check_paper_for_declined(the_id)
        print('the_id',the_id,n_declined)
        sorted_by_ref[n_declined].append(the_id)
    else:
        secound_round_data=jnf.get_paper_in_double_reviews(contrib['id'])
        if secound_round_data is None:
            print("Paper not in second round",the_id)
        else:
            if secound_round_data['date_resubmitted'] is None or len(secound_round_data['date_resubmitted'])<5:
                record_resubmit.append(the_id)
            if secound_round_data['suggestion_spb_2nd_round'] is not None and len(secound_round_data['suggestion_spb_2nd_round'])>5:
                print("secound_round_data['suggestion_spb_2nd_round']",secound_round_data['suggestion_spb_2nd_round'])
                if secound_round_data['suggestion_spb_2nd_round'] == "accept":
                    suggested_accept.append(contrib['id'])
                else:
                    suggested_reject.append(contrib['id'])
            else:
                not_yet_suggested.append(contrib['id'])
                the_paper=jnf.get_paper_info(contrib['db_id'],use_cache=False,sleep_before_online=1)
                if the_paper['state']['name'] == "submitted":
                    print(secound_round_data['decision_1st_round'],secound_round_data['date_resubmitted'][0:10],"Not yet suggested ",contrib['id']," URL= https://indico.jacow.org/event/41/papers/"+str(contrib['db_id'])+"/")
                    for irev in range(0,3):
                        if secound_round_data[ 'decision_2nd_review'+str(irev+1) ] is not None:
                            print('\t\tdecision_2nd_review'+str(irev+1),": ", secound_round_data[ 'decision_2nd_review'+str(irev+1) ])
if check_for_nref_declined:
    for iref in range(0,15):
        print(iref,sorted_by_ref[iref])
else:
    print('suggested_accept',len(suggested_accept),suggested_accept)
    print('suggested_reject',len(suggested_reject),suggested_reject)
    print('not_yet_suggested',len(not_yet_suggested),not_yet_suggested)

    notify_accept=True
    if notify_accept:
        for the_id in record_resubmit:
            print("./find_paper.py --id ", the_id , " --record-resubmit")
        for the_id in suggested_accept:
            print("./find_paper.py --id ", the_id , " --notify-authors")
        for the_id in suggested_accept:
            print("./find_paper.py --id ", the_id )
        for the_id in suggested_reject:
            print("./find_paper.py --id ", the_id , " --notify-authors")
        for the_id in suggested_reject:
            print("./find_paper.py --id ", the_id )
