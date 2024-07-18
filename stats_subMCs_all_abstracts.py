#!/usr/local/bin/python3.9

# Stats about all the abstracts
# Nicolas Delerue, 12/2023

import jacow_nd_func as jnf

import joblib

counter={}

use_online=True
#use_online=True
fname='stats_all_abstracts.data'

counter['MC']={}
counter['Track']={}

    
if use_online:
    the_range=range(500,2800)
else:
    the_range=[]
    
for the_id in the_range:
    contrib=jnf.find_contrib(the_id)
    if contrib is not None:
        if contrib['track'] is None:
            print('Contrid ',str(the_id), ' has Track None')
        else:
            if contrib['track'][0:3] not in counter['MC'].keys():
                counter['MC'][contrib['track'][0:3]]=1
            else:
                counter['MC'][contrib['track'][0:3]]=counter['MC'][contrib['track'][0:3]]+1
    
            if contrib['track'][0:7] not in counter['Track'].keys():
                counter['Track'][contrib['track'][0:7]]=1
            else:
                counter['Track'][contrib['track'][0:7]]=counter['Track'][contrib['track'][0:7]]+1



if use_online:
    joblib.dump(counter,fname)
else:
    counter=joblib.load(fname)


print("############")
            

print(counter['MC'])
print(counter['Track'])
sorted_tracks=sorted(counter['Track'])
print(sorted_tracks)

for subMC in counter['Track']:
    if counter['Track'][subMC]>5:
        print(subMC, counter['Track'][subMC])
        
#Create summary table
allSubMC=[]
for subMC in counter['Track']:
    if not subMC[4:] in allSubMC:
        allSubMC.append(subMC[4:])
        
        
#print(allSubMC)        
#print(sorted(allSubMC))  

fname="stats_by_MC_all_abstracts.html"
fhtml=open(fname,"w")
fhtml.write("<html>\n")
fhtml.write("<title>Stats for all abstracts</title>\n")
fhtml.write("<h2>Stats for all abstracts</h2>\n")


fhtml.write('<table border=3>')
fhtml.write('<tr>')
fhtml.write('<td></td>')
totalMCs=[]
for iMC in range(1,9):
    fhtml.write('<td>MC'+str(iMC)+'</td>')
    totalMCs.append(0)
fhtml.write('<td>Total</td>')
fhtml.write('</tr>\n')
allTotal=0
for subMC in sorted(allSubMC):      
    totalSubMC=0
    fhtml.write('<tr>')
    fhtml.write('<td>'+subMC+'</td>')
    for iMC in range(1,9):
        fhtml.write('<td>')
        theSubMC='MC'+str(iMC)+'.'+subMC
        if theSubMC in counter['Track'].keys():
            fhtml.write(str(counter['Track'][theSubMC]))
            totalSubMC=totalSubMC+counter['Track'][theSubMC]
            totalMCs[iMC-1]=totalMCs[iMC-1]+totalSubMC+counter['Track'][theSubMC]
            allTotal=allTotal+counter['Track'][theSubMC]
        fhtml.write('</td>')
    fhtml.write('<td>')
    fhtml.write(str(totalSubMC))
    fhtml.write('</td>')
    fhtml.write('</tr>\n')
fhtml.write('<tr>\n')
fhtml.write('<td>Total</td>')
for iMC in range(1,9):
    fhtml.write('<td>'+str(totalMCs[iMC-1])+'</td>')
fhtml.write('<td>'+str(allTotal)+'</td>')
fhtml.write('</tr>\n')


    
fhtml.write('</table>')
fhtml.write('</html>')

fhtml.close()


#to do:
# check authors
# check in referees list
# check submitter continent

        

