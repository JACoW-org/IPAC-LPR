# Try to make an indico request to get json data about all papers submitted
# Nicolas Delerue, 1/2023

import requests
import json

api_token = "xxx"
event_id = 41


#Trying to reset a contribution's judgement
if 1==1:
    headers = {'Authorization': f'Bearer {api_token}'}
    #payload = {'action': 'to_be_corrected' ,  'comment': 'Paper to be corrected, see separate email.'}
    #payload = {"judgment": "To be corrected", "comment":"Paper to be corrected, see separate email", "action": "to_be_corrected"}
    data = requests.delete(f'https://indico.jacow.org/event/41/papers/api/803', headers=headers)
    print('get done', flush=True)
    print(data)
    print("---")
    print(data.text)
    print("---")
    print(data)
    print("---")
    exit()

#Trying to judge a contribution
if 1==0:
    headers = {'Authorization': f'Bearer {api_token}'}
    payload = {'action': 'to_be_corrected' ,  'comment': 'Paper to be corrected, see separate email.'}
    #payload = {"judgment": "To be corrected", "comment":"Paper to be corrected, see separate email", "action": "to_be_corrected"}
    data = requests.post(f'https://indico.jacow.org/event/41/papers/api/2818/judge', headers=headers, data=payload)
    print('get done', flush=True)
    print(data)
    print("---")
    print(data.text)
    print("---")
    print(data)
    print("---")
    exit()

#Reads a contribution based on its ID
if 1==0:
    headers = {'Authorization': f'Bearer {api_token}'}
    payload = {'contribution_id': [1881]}
    data = requests.post(f'https://indico.jacow.org/event/{event_id}/manage/papers/assignment-list/export-json', headers=headers, data=payload).json()
    print('get done', flush=True)
    print(data)
    print("---")
    print(data.keys())
    print("---")
    print(data['content_review_questions'])
    print(len(data['content_review_questions']))
    print("---")
    print(data['content_review_questions'][0])
    print(data['content_review_questions'][0].keys())
    print("---")
    print(data['papers'])
    exit()

#Reads a contribution based on its ID
if 1==0:
    headers = {'Authorization': f'Bearer {api_token}'}
    payload = {'contribution_id': [ 1660 ]}
    data = requests.post(f'https://indico.jacow.org/event/{event_id}/manage/papers/assignment-list/export-json', headers=headers, data=payload).json()

    print(data)


#Reads a contribution based on its ID
if 1==0:
    headers = {'Authorization': f'Bearer {api_token}'}
    payload = {'contribution_id': [ 1660 ]}
    data = requests.post(f'https://indico.jacow.org/event/{event_id}/manage/papers/export-json', headers=headers, data=payload)

    print(data)


#Returns a web page not working?
if 1==0:
    headers = {'Authorization': f'Bearer {api_token}'}
    payload = {'contribution_id': [1660]}
    data = requests.post(f'https://indico.jacow.org/event/{event_id}/contributions/', headers=headers, data=payload)
    print(data.text)

#trying to get the contribution rating... 
if 1==0:
    headers = {'Authorization': f'Bearer {api_token}', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    #payload = {'contribution_id': [1660]}
    data = requests.get(f'https://indico.jacow.org/event/41/papers/1537/', headers=headers)

    print(data.text)
    #print(data.json())

#Gets a user id from its email address
if 1==0:
    headers = {'Authorization': f'Bearer {api_token}'}
    data = requests.get(f'https://indico.jacow.org/user/search/?email=delerue@lal.in2p3.fr&favorites_first=true', headers=headers)
    print(data.text)
    print(data.json())

#Get info about a paper
if 1==0:
    headers = {'Authorization': f'Bearer {api_token}'}
    payload = {'contribution_id': [1660]}
    data = requests.post(f'https://indico.jacow.org/event/41/manage/papers/assignment-list/export-json', headers=headers, data=payload)
    print(data.text)
    print(data.json())
    print(' ')
    print(data.json()['papers'][0])
    print(' ')
    print(data.json().keys())
    print(data.json()['papers'][0].keys())
    
    
#Assigns a content reviewer to a paper
if 1==0:
    api_token = "indp_fAKWkervPepBObXLPJ6R1s46EJjU2iqpYAj9oFH0xD"
    event_id = 41
    #headers = {'Authorization': f'Bearer {api_token}', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    headers = {'Authorization': f'Bearer {api_token}'}
    payload = {'contribution_id': [1660], 'user_id': [877] }
    data = requests.post(f'https://indico.jacow.org/event/41/manage/papers/assignment-list/unassign/content_reviewer', headers=headers, data=payload)

    print(data.text)
    print(data.json())

#Get reviewer team 
if 1==0:
    api_token = "indp_fAKWkervPepBObXLPJ6R1s46EJjU2iqpYAj9oFH0xD"
    event_id = 41
    #headers = {'Authorization': f'Bearer {api_token}', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    headers = {'Authorization': f'Bearer {api_token}'}
    payload = {'fieldId': 'content_reviewers', 'user_id': [3193] }
    data = requests.get(f'https://indico.jacow.org/event/41/manage/papers/teams/?_=1680007113015', headers=headers)
    #print(data.text)
    for line in data.text.split("\\n"):
        #if 'id=\"content_reviewers\"' in line:
        if 'id=\\"content_reviewers' in line:
            print(line.replace("&#34;","").replace("User:","").split("[")[1].split("]")[0].split(","))

#Add user to reviewer team 
if 1==0:
    ### Not working...
    api_token = "indp_fAKWkervPepBObXLPJ6R1s46EJjU2iqpYAj9oFH0xD"
    event_id = 41
    #headers = {'Authorization': f'Bearer {api_token}', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    headers = {'Authorization': f'Bearer {api_token}'}
    payload = {'fieldId': 'content_reviewers', 'user_id': [3193] }
    data = requests.post(f'https://indico.jacow.org/event/41/manage/papers/teams/', headers=headers, data=payload)
    print(data.text)
    
#Get the paper rating and sumbmission date
if 1==0:
    api_token = "indp_fAKWkervPepBObXLPJ6R1s46EJjU2iqpYAj9oFH0xD"
    event_id = 41
    #headers = {'Authorization': f'Bearer {api_token}', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    headers = {'Authorization': f'Bearer {api_token}'}
    #payload = {'contribution_id': [1660]}
    data = requests.get(f'https://indico.jacow.org/event/41/papers/api/932', headers=headers)

    #print(data.text)
    print(data.json())
    print('  ')
    print(data.json().keys())
    print('  ')
    print(data.json()['revisions'])
    print('  ')
    print(len(data.json()['revisions']))
    print(data.json()['revisions'][0]['id'])
    print(data.json()['revisions'][0].keys())
    print(data.json()['revisions'][0]['is_last_revision'])
    print(data.json()['revisions'][0]['submitted_dt'])
    print(data.json()['last_revision']['timeline'][0]['timeline_item_type'])
    print(data.json()['last_revision']['timeline'][1]['timeline_item_type'])
    print(data.json()['last_revision']['timeline'][1]['proposed_action']['name'])
    print(data.json()['last_revision']['timeline'][1]['user'])
    print('  ')
    print(data.json()['last_revision']['timeline'][1])
    print('  ')
    print(data.json()['last_revision']['timeline'][1]['user']['id'])
    print('  ')
    print(data.json()['last_revision']['timeline'][1]['user']['email'])
    print('  ')
    print(data.json()['contribution'])
    print(data.json()['contribution']['title'])
    print('  ')
    print(data.json()['last_revision']['files'])
    print('  ')
    print(data.json()['last_revision']['files'][0]['filename'])
    print('  ')
    print(data.json()['last_revision']['number'])
    print(len(data.json()['revisions']))
    print('  ')
    print(data.json()['last_revision']['submitter'])
    print(data.json()['last_revision']['submitter']['email'])
    print(data.json()['last_revision']['submitter']['full_name'])
    print('  ')
    print(data.json()['last_revision'].keys())
    print('  ')


#trying... Not working
if 1==0:
    api_token = "indp_fAKWkervPepBObXLPJ6R1s46EJjU2iqpYAj9oFH0xD"
    event_id = 41
    headers = {'Authorization': f'Bearer {api_token}'}
    #payload = {'contribution_id': [1660]}
    #data = requests.post(f'https://indico.jacow.org/event/{event_id}.json?detail=contributions', headers=headers, data=payload)
    #data = requests.get(f'https://indico.jacow.org/event/{event_id}.json?detail=contributions&pretty=yes', headers=headers)
    #data = requests.get(f'https://indico.jacow.org/event/{event_id}.json?detail=contributions&pretty=yes', headers=headers)
    data = requests.get(f'https://indico.jacow.org/export/event/41.json?occ=yes&pretty=yes', headers=headers)

    print(data.text)
    print(data.json())



#List all contributions
if 1==0:
    api_token = "indp_fAKWkervPepBObXLPJ6R1s46EJjU2iqpYAj9oFH0xD"
    event_id = 41
    headers = {'Authorization': f'Bearer {api_token}'}
    #payload = {'contribution_id': [1660]}
    #data = requests.post(f'https://indico.jacow.org/event/{event_id}.json?detail=contributions', headers=headers, data=payload)
    #data = requests.get(f'https://indico.jacow.org/event/{event_id}.json?detail=contributions&pretty=yes', headers=headers)
    #data = requests.get(f'https://indico.jacow.org/event/{event_id}.json?detail=contributions&pretty=yes', headers=headers)
    data = requests.get(f'https://indico.jacow.org/export/event/41.json?detail=contributions&pretty=yes', headers=headers)

    #print(data.text)
    #print(data.json())

    #print(json.dumps(data.json(), indent=4))
    #Data_json=json.load(json.dumps(data.json()))
    #print(data.json()["count"])
    data_json=data.json()
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

