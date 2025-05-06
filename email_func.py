# Sending emails from python
# Nicolas Delerue, 3/2023

# Import smtplib for the actual sending function
import smtplib
import datetime
import time,sys
import traceback
# Import the email modules we'll need
from email.mime.text import MIMEText

# Import the email modules we'll need
from email.message import EmailMessage

#import jacow_nd_func as jnf

import params


try:
    params.mail_pwd
except:
    print("Mail password is not defined... Exiting...")
    sys.exit(1)

def email_file(recipients,filename,replace_dict=None,show_message=False,send_me_a_copy=True):
    with open(filename, 'r') as fp:
        lines=fp.readlines()

    txt_msg=""
    for line in lines:
        if replace_dict is not None:
            #print(replace_dict.keys())
            for the_key in replace_dict.keys():
                line=line.replace("##"+the_key+"##",str(replace_dict[the_key]))
        txt_msg=txt_msg+line
    if show_message:
        print("Message")
        print(txt_msg)
    email_txt(recipients,txt_msg,send_me_a_copy)

    
def email_txt(recipients,string_txt,show_message=False,send_me_a_copy=True):
    send_msg=True
    title=string_txt.split("\n")[0]
    msgtxt=string_txt[len(title)+1:]
    
    print("Title")
    print(title)
    if show_message:
        print("Message")
        print(msgtxt)
        
    msg = EmailMessage()
    msg.set_content(msgtxt)
    
    #message_recipients = recipients
        
    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = title
    msg['From'] =  params.email_from_txt
    msg['To'] = recipients
    if show_message:
        print(msg.as_string())
    if not send_msg:
        print("Testing, not sending!")
        exit()

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    try:
        smtp_serv = smtplib.SMTP_SSL(params.email_smtp_server)
        smtp_serv.login(params.smtp_login,params.mail_pwd)
    except:
        print("Unable to connect to server ",params.email_smtp_server," with login ", params.email_from_address)
        print(traceback.format_exc())
        sys.exit(-1)
        
    if "," in recipients:
        recips=recipients.split(",")
    else:
        recips = recipients
    print("Sending email to ", recips)
    if send_me_a_copy:
        recips.append(params.email_from_address)
    for recip in recips:
        if "<" in recip:
            the_recip=recip.split("<")[1].split(">")[0]
        else:
            the_recip = recip.strip()
        try:
            smtp_serv.sendmail(params.email_from_address, the_recip, msg.as_string())
        except:
            print("Sending to ", the_recip, " failed ")
            print(traceback.format_exc())
    smtp_serv.quit()
    print("done")
    
