# Try to make an indico request to get json data about all papers submitted
# Nicolas Delerue, 1/2023



import requests
import json

api_token = "R1s46EJjU2iqpYAj9oFH0xD"

#Trying to judge a contribution
if 1==1:
    event_id = 41
    headers = {'Authorization': f'Bearer {api_token}'}
    payload = {'action': 'accept' ,  'comment': 'Accepted for test'}
    #payload = {"judgment": "To be corrected", "comment":"Paper to be corrected, see separate email", "action": "to_be_corrected"}
    data = requests.post(f'https://indico.jacow.org/event/37/papers/api/149/judge', headers=headers, data=payload)
    print('get done', flush=True)
    print(data)

if 1==1:
    event_id = 37
    headers = {'Authorization': f'Bearer {api_token}'}

    data = requests.delete(f'https://indico.jacow.org/event/37/papers/api/149', headers=headers)
    print(data)
    print(data.status_code)
exit()

event_id = 37
headers = {'Authorization': f'Bearer {api_token}'}
payload = {'contribution_id': [149]}
#data = requests.post(f'https://indico.jacow.org/event/{event_id}/manage/papers/assignment-list/export-json', headers=headers, data=payload).json()

#print(data)


event_id = 37
headers = {'Authorization': f'Bearer {api_token}'}
payload = {'contribution_id': [149]}
#data = requests.post(f'https://indico.jacow.org/event/{event_id}/contributions/', headers=headers, data=payload)

#print(data.text)

event_id = 37
headers = {'Authorization': f'Bearer {api_token}'}
payload = {'contribution_id': [149]}
#data = requests.post(f'https://indico.jacow.org/event/{event_id}.json?detail=contributions', headers=headers, data=payload)
data = requests.get(f'https://indico.jacow.org/event/{event_id}.json?detail=contributions', headers=headers)
data = requests.get(f'https://indico.jacow.org/export/event/37.json?detail=contributions&pretty=yes', headers=headers)

#print(data.text)
print(data.json())

#print(json.dumps(data.json(), indent=4))
#data_json=json.load(json.dumps(data.json()))
print(data.json()["count"])
data_json=data.json()
print(data_json["count"])
print("after load")
print(data_json["results"])
print(data_json["count"])
print(data_json.keys())
print(list(data_json.keys()))
print(len(data_json["results"]))
print(data_json["results"][0])

#result_json=json.load(data_json["results"][0])
result_json=data_json["results"][0]
print(list(result_json.keys()))
print(result_json['contributions'])
print(len(result_json['contributions']))
print(result_json['contributions'][0])    
contribution_json=result_json['contributions'][0]
for contrib in result_json['contributions']:
    print(contrib['title']+"\n")
    print(contrib['speakers'])
    print(contrib['primaryauthors'])
    print(contrib['coauthors'])
    print("len",len(contrib['speakers']))    
    #speaker_json=contrib['speakers'][0]
    
print(list(contribution_json.keys()))

