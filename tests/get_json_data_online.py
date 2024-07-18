# Try to make an indico request to get json data about all papers submitted
# Nicolas Delerue, 1/2023

import requests
import json
import pickle

def printv(txt):
    print(txt," : ",eval(txt))

import jacow_nd_func as jnf

api_token = "xxx"
event_id = 41
headers = {'Authorization': f'Bearer {api_token}'}
#payload = {'contribution_id': [1660]}
#data = requests.post(f'https://indico.jacow.org/event/{event_id}.json?detail=contributions', headers=headers, data=payload)
#data = requests.get(f'https://indico.jacow.org/event/{event_id}.json?detail=contributions&pretty=yes', headers=headers)
#data = requests.get(f'https://indico.jacow.org/event/{event_id}.json?detail=contributions&pretty=yes', headers=headers)

#use_online=True
use_online=False
data_json=None
fname="ipac23_contribs.json"
if use_online:
    data = requests.get(f'https://indico.jacow.org/export/event/41.json?detail=contributions&pretty=yes', headers=headers)
    data_json=data.json()
    print('get done', flush=True)
    print(data_json["results"])
    print(data_json["count"])
    print("---")
    
    save_data=True
    #save_data=False
    if save_data:
        fdata=open(fname,"w")
        json.dump(data_json,fdata)
        #pickle.dump()
        fdata.close()
else:
    fdata=open(fname,"r")
    data_json=json.load(fdata)
    fdata.close()


print(data_json["results"])
print(data_json["count"])
print("---")
print(data_json.keys())
print(list(data_json.keys()))
print("---")
print(len(data_json["results"]))
print("---")
print(data_json["results"][0])


#result_json=json.load(data_json["results"][0])
result_json=data_json["results"][0]
print(list(result_json.keys()))
print(result_json['contributions'])
print(len(result_json['contributions']))
print(result_json['contributions'][0])    
contribution_json=result_json['contributions'][0]
print("***")
for contrib in result_json['contributions']:
    print(contrib['title']+"\n")
    print(contrib['speakers'])
    print(contrib['primaryauthors'])
    print(contrib['coauthors'])
    print("len",len(contrib['speakers']))    
    #speaker_json=contrib['speakers'][0]
    print("---")
    exit()
    
#print(list(contribution_json.keys()))

