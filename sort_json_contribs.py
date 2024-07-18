# Try to make an indico request to get json data about all papers submitted
# Nicolas Delerue, 1/2023


def printv(txt):
    print(txt," : ",eval(txt))

import jacow_nd_func as jnf

#jnf.load_contribs()

#contrib=jnf.find_contrib(the_id='512')
contrib=jnf.find_contrib(the_db_id=1660)

print(contrib)
print('---')
print('id',contrib['id'])
print('db_id',contrib['db_id'])
print('title',contrib['title'])
print('speakers',contrib['speakers'])
print('---')
print(contrib.keys())
print('---')
print('material',contrib['material'])

exit()
result_json=jnf.data_json["results"][0]
#print(list(result_json.keys()))
#print(result_json['contributions'])
print(len(result_json['contributions']))
#print(result_json['contributions'][0])    
contribution_json=result_json['contributions'][0]
print("***")
#result_json['contributions']=result_json['contributions'][0:5]
for contrib in result_json['contributions']:
    if contrib['id'] == '512':
        print(contrib)
        print('id',contrib['id'])
        print('db_id',contrib['db_id'])
        print('title',contrib['title'])
        print('speakers',contrib['speakers'])
        #print(contrib['primaryauthors'])
        #print(contrib['coauthors'])
        #print("len",len(contrib['speakers']))    
        #speaker_json=contrib['speakers'][0]
        print(contrib.keys())
        print('material',contrib['material'])
        print("---")
    
#print(list(contribution_json.keys()))

