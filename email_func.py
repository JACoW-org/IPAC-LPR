# Sending emails from python
# Nicolas Delerue, 3/2023

# Import smtplib for the actual sending function
import smtplib
import datetime
import time,sys
# Import the email modules we'll need
from email.mime.text import MIMEText

import jacow_nd_func as jnf

global mailpwd

try:
    mailpwd
except:
    fname="../mailpwd.txt"
    try:
        fpwd=open(fname)
        mailpwd=fpwd.readlines()[0]
        fpwd.close()
        print('mailpwd loaded')
    except:
        print("Unable to read ",fname)
        sys.exit(1)
    
textfile='message_referee_request_v2.txt'
def send_email(referee_id,paper_id,msgfile='message_referee_request_v2.txt',url=None,deadline=None,substitution_dict=None):
    send_msg=True
    #send_msg=False

    #Get referee info
    [ref_name, ref_email, ref_affiliation, ref_country, ref_MC, ref_ID]=jnf.get_referee_by_id(int(referee_id))

    #Get contribution info
    #jnf.find_contrib(the_id=None,the_db_id=None):
    contrib=jnf.find_contrib(the_id=paper_id)

    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    title=None
    msg = ""
    with open(msgfile, 'r') as fp:
        lines=fp.readlines()

    for line in lines:
        # Create a text/plain message
        if title is None:
            title= line
        else:
            line=line.replace("##name##",ref_name)
            line=line.replace("##title##",contrib['title'])
            line=line.replace("##paper_id##",contrib['id'])
            line=line.replace("##abstract##",contrib['description'])
            line=line.replace("##url_paper##","https://indico.jacow.org/event/41/papers/"+str(contrib['db_id'])+"/")
            line=line.replace("##url_papier##","https://indico.jacow.org/event/41/papers/"+str(contrib['db_id'])+"/")
            if deadline is not None:
                line=line.replace("##deadline##",deadline)
            if url is not None:
                line=line.replace("##url##",url)
            if substitution_dict is not None:
                for the_key in substitution_dict.keys():
                    line=line.replace("##"+the_key+"##",substitution_dict[the_key])
            if "##" in line:
                print("Some replacement tags have not been replaced!")
                print(line)
                print("Some replacement tags have not been replaced!")
                time.sleep(120)
                #exit()
            msg = msg + line
    msg = msg + "\nMessage sent on: "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" @"+str(referee_id)
    
    print("Message")
    print(msg)
    msg = MIMEText(msg,_charset='utf-8')

    me = "nicolas.delerue@ijclab.in2p3.fr"
    peer_review_address= "peer-review@ipac23.org"
    #message_recipient = "nicolas.delerue@universite-paris-saclay.fr"
    message_recipient = ref_email
    #message_recipient = "nico@delerue.org"


    #print("title",title)
    print('message_recipient:',message_recipient)
    #print("---")
    #print("msg", msg)
        
    if not send_msg:
        print("Testing, not sending!")
        exit()
    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = title
    msg['From'] = "IPAC'23 LPR - Nicolas Delerue <"+me+">"
    msg['To'] = ref_name + "<" +ref_email +">"
    msg['Cc'] = "IPAC'23 Peer Review <peer-review@ipac23.org>" 

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    try:
        smtp_serv = smtplib.SMTP_SSL('zrelay.in2p3.fr')
        smtp_serv.login(me,mailpwd)
        try:
            smtp_serv.sendmail(me, [message_recipient,peer_review_address], msg.as_string())
        finally:
            smtp_serv.quit()
    except:
        sys.exit( "mail failed; %s" % "CUSTOM_ERROR" )
    print("done")

def email_file(recipients,filename,replace_dict=None):
    with open(filename, 'r') as fp:
        lines=fp.readlines()

    txt_msg=""
    for line in lines:
        if replace_dict is not None:
            #print(replace_dict.keys())
            for the_key in replace_dict.keys():
                line=line.replace("##"+the_key+"##",str(replace_dict[the_key]))
        txt_msg=txt_msg+line
    print("Message")
    print(txt_msg)
    email_txt(recipients,txt_msg)

    
def email_txt(recipients,string_txt):
    send_msg=True
    
    print("Title")
    title=string_txt.split("\n")[0]
    print(title)
    print("Message")
    msg=string_txt[len(title)+1:]
    print(msg)
    
    msg = MIMEText(msg,_charset='utf-8')

    me = "nicolas.delerue@ijclab.in2p3.fr"
    peer_review_address= "peer-review@ipac23.org"
    peer_review_address= "nicolas.delerue@ijclab.in2p3.fr"
    #message_recipient = "nicolas.delerue@universite-paris-saclay.fr"
    message_recipients = recipients
    #message_recipient = "nico@delerue.org"


    #print("title",title)
    #print('message_recipient:',message_recipient)
    #print("---")
    #print("msg", msg)
        
    if not send_msg:
        print("Testing, not sending!")
        exit()
    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = title
    msg['From'] = "IPAC'23 LPR - Nicolas Delerue <"+peer_review_address+">"
    msg['To'] = recipients
    #msg['Cc'] = "IPAC'23 Peer Review <peer-review@ipac23.org>" 

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    try:
        smtp_serv = smtplib.SMTP_SSL('zrelay.in2p3.fr')
        smtp_serv.login(me,mailpwd)
        try:
            #print(recipients)
            recips=recipients.split(",")
            print(recips)
            recips.append(peer_review_address)
            print(recips)
            for recip in recips:
                if "<" in recip:
                    the_recip=recip.split("<")[1].split(">")[0]
                else:
                    the_recip = recip.strip()
                smtp_serv.sendmail(me, [the_recip], msg.as_string())
        finally:
            smtp_serv.quit()
    except:
        sys.exit( "mail failed; %s" % "CUSTOM_ERROR" )
    print("done")
    
