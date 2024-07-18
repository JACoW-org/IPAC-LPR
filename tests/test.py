import jacow_nd_func as jnf
import email_func as ef 
import openpyxl
#import time
#import joblib


all_refs=jnf.get_all_referees_from_file()
with_papers_reviewed=0
for the_ref in all_refs:
    hist=jnf.check_history_for_referee(the_ref)
    #print("\t",hist)
    paper_reviewed=False
    for paper_hist in hist:
        #print('hist',paper_hist)
        if paper_hist['status'] in [ 'Email request sent' , "Reminder sent" , "2nd Reminder sent" , "Declined" , "Withdrawn" , "Deadline reminder sent"]:
            #print("Not accepted")
            pass
        elif paper_hist['status'] in [ "Review received" , "Accepted" ]:
            paper_reviewed=True
        else:
            print(paper_hist['status'])
            
    if paper_reviewed:
        with_papers_reviewed=with_papers_reviewed+1    
        print("+")
    else:
        print("-")
        
print('Total referees ',len(all_refs))
print('N referees with papers', with_papers_reviewed)
