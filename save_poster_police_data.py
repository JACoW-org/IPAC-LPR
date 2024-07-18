#Reads and parse the poster police data and dumps into an array

#import jacow_nd_func as jnf
import requests
import time
import joblib

fname="ipac23_org_cws_page_papers_index.html"

fdata=open(fname,"r")
data_text=fdata.read()
fdata.close()

all_entries=[]

lines=data_text.split("\n")
record_code=-1
iline=0
db_id=-1
for line in lines:
    print(iline,"==>",line)
    if "https://indico.jacow.org/event/41/contributions/" in line:
        if not "editing" in line:
            the_entry={}
            iline=0
            elems=line.split('"')
            print(elems)
            print(elems[3])
            db_id=int(elems[3].replace("https://indico.jacow.org/event/41/contributions/",""))
            print('db_id',db_id)
            id_elems=elems[6][1:].split('<')
            #print(id_elems[0])
            print('contrib_id',id_elems[0])
            the_entry['contrib_id']=int(id_elems[0])
            the_entry['db_id']=db_id
        else:
            elems=line.split('"')
            id_elems=elems[4][1:].split('<')
            #print(id_elems[0])
            print('code',id_elems[0])
            the_entry['code']=id_elems[0]
    if db_id>0 and iline==3:
        print(line)
        title=line.replace("</td>","").split(">")[1]
        print("title", title)
        the_entry['title']=title
    if db_id>0 and iline==4 and not "<td>"in line:
        title=title+line.replace("</td>","")
        print("title", title)
        the_entry['title']=title
    if db_id>0 and iline==5:
        #print(line)
        status=line.replace("</td>","").split(">")[1]
        print("status", status)
        the_entry['status']=status
    if db_id>0 and iline==7:
        pdf_status=line.replace("</td>","").split(">")[1]
        print("pdf status", pdf_status)
        the_entry['pdf_status']=pdf_status
    if db_id>0 and iline==8:
        police_status=line.replace("</td>","").split(">")[1]
        print("police status", police_status)
        the_entry['police_status']=police_status        
    if db_id>0 and iline==10:
        author_status=line.replace("</td>","").split(">")[1]
        print("author status", author_status)
        the_entry['author_status']=author_status        
    if db_id>0 and iline==11:
        author_present_status=line.replace("</td>","").split(">")[1]
        print("author present status", author_present_status)
        the_entry['author_present_status']=author_present_status
        #save the record
        all_entries.append(the_entry)
        the_entry={}
        db_id=-1
        iline=-1
    if "<td" in line:
        iline=iline+1
print(all_entries)
joblib.dump(all_entries,"poster_police_results.jlib")


#find paper with given contrib_id
the_entry=None
paper_contrib_id=1789
for entry in all_entries:
    if int(entry['contrib_id'])==int(paper_contrib_id):
        the_entry=entry
print(the_entry)
