# Requestion date abut one contribution
# Nicolas Delerue, 3/2023

import requests
import json


#Reads a submitted contribution based on its ID
api_token = "indp_fAKWkervPepBObXLPJ6R1s46EJjU2iqpYAj9oFH0xD"
event_id = 41
headers = {'Authorization': f'Bearer {api_token}'}
payload = {'contribution_id': [1660]}
data = requests.post(f'https://indico.jacow.org/event/{event_id}/manage/papers/assignment-list/export-json', headers=headers, data=payload).json()

print(data)
print("---")
#print(data["content_review_questions"])
print("Keys")
print(data.keys())
#print(data["papers"])
print("---")
print(data["papers"][0])
print("---")
print(data["papers"][0].keys())
print("---")
print(data["papers"][0]["contribution"])
print("---")
print(data["papers"][0]["state"])
print("---")
print(data["papers"][0]["revisions"])
print("---")
print(len(data["papers"][0]["revisions"]))
print("---")
print(data["papers"][0]["revisions"][0].keys())
print("---")
print(data["papers"][0]["revisions"][0]["judge"])
