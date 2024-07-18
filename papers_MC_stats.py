# Try to make an indico request to get json data about all papers submitted
# Nicolas Delerue, 1/2023


import requests
import re
import random

use_online=True
use_online=False
if use_online:
    url="https://www.ipac23.org/a0vqlBiz19KVJcC8/exports/reviewers-03.php"
    data = requests.get(url)
    print('get done', flush=True)
    #print(data.text)

    save_data=True
    save_data=False
    if save_data:
        fdata=open("ipac23_data.txt","w")
        fdata.write(data.text)
        fdata.close()
    thedata=data.text.split("\n")
else:
    fdata=open("ipac23_data.txt","r")
    thedata=fdata.readlines()
    fdata.close()
        
table_headers=[]
table_entries=[]

current_entry = None

in_table=False
for line in thedata:
    #for line in [ "\n" , "xxx"] :
    #print('check line ', line)
    if "<table" in line: 
        #print('table ', line)
        in_table=True
    elif "</table>" in line:
        #print('table ', line)
        in_table=False
    else:
        if in_table:
            #print('line ', line)
            if "<tr>" in line:
                current_entry=[]
            if "<th>" in line:
                val = re.search("<th>.*</th>", line)
                if val is None:
                    val = re.search("<th>.*", line)                    
                #print('val ',val.group())
                #print('val ',val.group().replace("<th>","").replace("</th>",""))
                table_headers.append(val.group().replace("<th>","").replace("</th>",""))
            if "<td>" in line:
                val = re.search("<td>.*</td>", line)
                if val is None:
                    val = re.search("<td>.*", line)                    
                #print('val ',val.group())
                #print('val ',val.group().replace("<td>","").replace("</td>",""))
                current_entry.append(val.group().replace("<td>","").replace("</td>",""))
            if "</tr>" in line:
                if current_entry is not None:
                    table_entries.append(current_entry)
                current_entry=None
                
#print('table_entries ',table_entries)

#print('table_headers ',table_headers)

mc_list=[]
submc_list=[]
country_list=[]
authors_list=[]

mc_idx=table_headers.index('mc')
submc_idx=table_headers.index('track')
country_idx=table_headers.index('speakers<br />country')
author_idx=table_headers.index('speakers')
#print('mc_idx',mc_idx)
#print('submc_idx',submc_idx)
#print('country_idx',country_idx)
#print('author_idx',author_idx)

for entry in table_entries:
    if (len(entry)>submc_idx):
        #print(entry)
        if not (entry[mc_idx] in mc_list):
            mc_list.append(entry[mc_idx])
        if not (entry[submc_idx] in submc_list):
            submc_list.append(entry[submc_idx])
        country_data=entry[country_idx].replace("<br />","")
        if "span" in country_data:
            country_data="??"
        all_countries=country_data.split(";")
        #print(country_data+"\n")
        #print(all_countries)
        #print("\n")
        for country in all_countries:
            if not (country in country_list):
                country_list.append(country)
                
        author_data=entry[author_idx].replace("<br />","")
        all_authors=author_data.split(";")
        for author in all_authors:
            if not (author in authors_list):
                authors_list.append(author)
#print('mc_list ',mc_list)
#print('submc_list ',submc_list)
#print('country_list',country_list)
#print('authors_list',authors_list)

#create mc_by_country list
mc_by_country_list=[]
for mc in mc_list:    
    all_countries=[]
    for country in country_list:
        #all_countries.append(mc+" "+country)
        all_countries.append(0)
    mc_by_country_list.append(all_countries)

#create submc_by_country list
submc_by_country_list=[]
for submc in submc_list:    
    all_countries=[]
    for country in country_list:
        #all_countries.append(mc+" "+country)
        all_countries.append(0)
    submc_by_country_list.append(all_countries)

authors_with_mc_and_country=[]
for author in authors_list:
    this_author=[]
    this_author.append([]) #MC
    this_author.append([]) #subMC
    this_author.append([]) #country
    authors_with_mc_and_country.append(this_author)
    
#print(mc_by_country_list)
#print(mc_by_country_list[2])
#print(mc_by_country_list[2][2])

#print(mc_by_country_list[2][3])
    
for entry in table_entries:
    if (len(entry)>submc_idx):
        mc_val=mc_list.index(entry[mc_idx])
        submc_val=submc_list.index(entry[submc_idx])
        country_data=entry[country_idx].replace("<br />","")
        if "span" in country_data:
            country_data="??"
        all_countries=country_data.split(";")
        all_countries_val=[]
        for country in all_countries:
            country_val=country_list.index(country)
            mc_by_country_list[mc_val][country_val]=mc_by_country_list[mc_val][country_val]+1
            submc_by_country_list[submc_val][country_val]=submc_by_country_list[submc_val][country_val]+1
            all_countries_val.append(country_val)
        author_data=entry[author_idx].replace("<br />","")
        all_authors=author_data.split(";")
        for author in all_authors:
            author_val=authors_list.index(author)
            authors_with_mc_and_country[author_val][0].append(mc_val)
            authors_with_mc_and_country[author_val][1].append(submc_val)
            authors_with_mc_and_country[author_val][2]=authors_with_mc_and_country[author_val][2]+all_countries_val

#print(mc_by_country_list)
#print(mc_by_country_list[2])
#print(mc_by_country_list[2][2])

#print(mc_by_country_list[2][3])

#print(authors_with_mc_and_country)

show_mc_by_country=False
if show_mc_by_country:
    for country in country_list:
        print('Country',country)
        country_val=country_list.index(country)
        for mc in mc_list:
            mc_val=mc_list.index(mc)
            print('       MC:',mc,mc_by_country_list[mc_val][country_val])
        
        for submc in submc_list:
            submc_val=submc_list.index(submc)
            #print('       sub-MC:',submc)
            if submc_by_country_list[submc_val][country_val]>0:
                print('       sub-MC:',submc,submc_by_country_list[submc_val][country_val])
        

#print paper parameters
the_paper=random.choice(table_entries)
paper_number=table_entries.index(the_paper)

print(table_entries[paper_number])
mc_val=mc_list.index(table_entries[paper_number][mc_idx])
submc_val=submc_list.index(table_entries[paper_number][submc_idx])
print('MC ',mc_list[mc_val])
print('subMC ',submc_list[submc_val])
country_data=table_entries[paper_number][country_idx].replace("<br />","")
if "span" in country_data:
    country_data="??"
all_countries=country_data.split(";")
all_paper_countries_val=[]
for country in all_countries:
    country_val=country_list.index(country)
    all_paper_countries_val.append(country_val)
print('Country ',all_paper_countries_val)

possible_referees=[]
for author in authors_list:
    author_val=authors_list.index(author)
    author_params=authors_with_mc_and_country[author_val]
    #print(author_params[0])
    author_match=False
    for author_mc in author_params[0]:
        if author_mc==mc_val:
            author_match=True
    #now check country
    if author_match:
        #print(author_params)
        for author_country in author_params[2]:
            if author_country in all_paper_countries_val :
                author_match=False

    if author_match:
        print('author match',author,author_params)
        possible_referees.append(author)
        
print(table_entries[paper_number])
print('MC ',mc_list[mc_val])
print('subMC ',submc_list[submc_val])
print('Country ',all_paper_countries_val,country_list[all_paper_countries_val[0]])

#print('country_list',country_list)
print('Selected referees')
referees=random.sample(possible_referees,2)
print(referees)
