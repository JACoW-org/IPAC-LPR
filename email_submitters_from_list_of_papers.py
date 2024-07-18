import jacow_nd_func as jnf
import email_func as ef 

message_file='message_author_paper_not_yet_resubmitted_with_deadline.txt'

#Check remaining contributions
contributions_to_be_emailed=  [582, 617, 671, 844, 909, 917, 938, 1007, 1167, 1266, 1268, 1329, 1441, 1509, 1623, 1723, 1979, 2035, 2140, 2190, 2197, 2229, 2511, 2677, 2722]

#prevent to run the script by mistake
xxx
for the_id in contributions_to_be_emailed: 
    contrib=jnf.find_contrib(the_id)
    the_paper=jnf.get_paper_info(contrib['db_id'],use_cache=True,sleep_before_online=1)
    authors_email=the_paper['last_revision']['submitter']['email']
    if not len(authors_email)>5:
        print("No email address for paper", the_id)
        exit()
    else:
        print('authors_email',authors_email)
        substitution_dict=jnf.get_substitution_dict_for_paper(contrib)
        ef.email_file(authors_email,message_file,replace_dict=substitution_dict)
