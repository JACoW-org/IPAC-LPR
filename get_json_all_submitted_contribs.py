# Try to make an indico request to get json data about all papers submitted
# Nicolas Delerue, 1/2023

import requests
import json


api_token = "indp_fAKWkervPepBObXLPJ6R1s46EJjU2iqpYAj9oFH0xD"
event_id = 41
headers = {'Authorization': f'Bearer {api_token}'}
data = requests.get(f'https://indico.jacow.org/export/event/41.json?detail=contributions&pretty=yes', headers=headers)

data_json=data.json()
#print(data_json["results"])
print("--- count ")
print(data_json["count"])
print("--- keys")
print(data_json.keys())
print(list(data_json.keys()))
print("--- len")
print(len(data_json["results"]))
print("---")
#print(data_json["results"][0])


#result_json=json.load(data_json["results"][0])
result_json=data_json["results"][0]
print(list(result_json.keys()))
#print(result_json['contributions'])
print(len(result_json['contributions']))
#print(result_json['contributions'][0])    
contribution_json=result_json['contributions'][0]
print("***")
for contrib in result_json['contributions']:
    if (contrib['db_id']=='1660'):
        print(contrib)
        print("###")
        print(contrib['id'])
        print(contrib['title']+"\n")
        print(contrib['speakers'])
        print(contrib['primaryauthors'])
        print(contrib['coauthors'])
        print("len",len(contrib['speakers']))    
        #speaker_json=contrib['speakers'][0]
        print("---")
        print(contrib['speakers'])
#print(list(contribution_json.keys()))

