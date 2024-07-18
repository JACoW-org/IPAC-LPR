import jacow_nd_func as jnf
import email_func as ef 
import argparse
import openpyxl
import datetime
import urllib.parse
import requests
import time


jnf.load_referee_files()

#read all referee acceptance emails
urlreplies="http://nicolas.delerue.org/ipac23/referee_reply.txt"
data = requests.get(urlreplies)
if not data.status_code == 200:
    print("Error getting the replies")
else:
    #print(data.text)
    lines=data.text.split("\n")
    check_found=False
    skip_rest=False
    #for line in reversed(lines):
    for line in lines:
        vals=line.split(";")
        if len(vals)>2 and not skip_rest:
            print('vals',vals)
            v1=vals[1].split(":")
            if v1[0]=='check':
                #print('check mark')
                pass
            elif v1[0]=='ref':
                referee_id=int((int(v1[1])/7)/10000)
                paper_id=int((int(v1[1])/7)%10000)
                print('referee_id',referee_id,'paper_id',paper_id)
                v2=vals[2].split(":")
                if not ( v2[0]=='answer' or v2[0]=='add_answer' or v2[0]=='origin'):
                    print("Not understood v2")
                    print(vals)
                    print(v2[0])
                    exit()
                elif v2[0]=='answer':                    
                    file_data=jnf.referee_assignation_file_get_line(paper_id,referee_id)
                    print(file_data)
                    was_recorded=False
                    action=''
                    if v2[1]=='yes':
                        action='accept'
                        if file_data['status']=='Accepted':
                            was_recorded=True
                    elif v2[1]=='other_field':                    
                        action='decline'
                        if file_data['status']=='Declined':
                            was_recorded=True
                    elif v2[1]=='unavailable':
                        action='unavailable'
                        data={}
                        data['accepting_papers']='unavailable'
                        jnf.referee_data_file_write_line(referee_id,data)
                        if file_data['status']=='Declined':
                            was_recorded=True
                    print('referee_id',referee_id,'paper_id',paper_id,'action',action)
                    if not was_recorded and not file_data['status'] in ['Review received']:
                        print("Not recorded",vals[0])
                        last_com=datetime.datetime.strptime(file_data['last_communication'],"%Y-%m-%d %H:%M:%S")
                        print(vals[0].split(":")[1])
                        date_reply=datetime.datetime.fromtimestamp(int(vals[0].split(":")[1]))
                        delta_com=last_com-date_reply
                        print('last com',last_com)
                        print('date_reply',date_reply)
                        print('delta_com',delta_com)
                        if not vals[0] in [ 'time:1679807355' , 'time:1679908889' , 'time:1680381880' ]:
                            exit()
                    print('was_recorded',was_recorded)
                    if file_data is None:
                        print('error data not found!')
                    else:
                        pass
                    #jnf.referee_action(paper_id=paper_id,the_ref_id=referee_id,action=action)
                elif v2[0]=='origin':                    
                    print('origin',line,vals[3])
                    v3=vals[3].split(":")
                    print(v3)
                    if v3[0] == "addtime":
                        v3=vals[6].split(":")
                        print(v3)
                    if not v3[0] == "add_answer":
                        exit()
                    else:
                        data={}
                        if v3[1]=="yes":
                            print('yes')
                            data['accepting_papers']='yes'
                            jnf.referee_data_file_write_line(referee_id,data)
                        elif v3[1]=="no":
                            data['accepting_papers']='no'
                            jnf.referee_data_file_write_line(referee_id,data)
                            print('no')
                        else:
                            exit()
                        
                    
            else:
                print("Not understood v1")
                print(vals)
                if vals[0]=='_answer:yes':
                    print('ignoring')
                else:
                    exit()
print('done')
