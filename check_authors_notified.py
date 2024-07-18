import jacow_nd_func as jnf

#Check that all authors have been notified
for the_id in range(500,2800):
    contrib=jnf.find_contrib(the_id)
    if contrib is not None:
        print('Checking paper for contrib ', the_id,' that is not none; db_id ',contrib['db_id'])
        secound_round_data=jnf.get_paper_in_double_reviews(the_id)
        if secound_round_data is not None:
            if secound_round_data['suggestion_spb_2nd_round'] is not None and len(secound_round_data['suggestion_spb_2nd_round'])>5 and (secound_round_data['date_resubmitted'] is None or len(secound_round_data['date_resubmitted'])<5):
                print(the_id)
                print(secound_round_data)
                print("./find_paper.py --id ",the_id," --record-resubmit")
                print("./find_paper.py --id ",the_id," --notify-authors")
                exit()
