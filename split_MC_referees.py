#!/usr/local/bin/python3

# Check the subMC if referees in split MC
# Nicolas Delerue, 3/2023

import jacow_nd_func as jnf
import joblib

jnf.load_contribs()
result_json=jnf.data_json_contribs["results"][0]
ref_results=[]
for contrib in result_json['contributions']:
    if contrib['track'] is not None:
        if int(contrib['track'][2]) in [6, 7, 8]:
            print(contrib['track'])
            print(contrib['track'][0:7])
            #print('match')
            for type in [ 'speakers' , 'primaryauthors' , 'coauthors' ]:
                for author in contrib[type]:
                    print(author['last_name'],author['first_name'])
                    retval=jnf.find_referee_by_name(author['last_name'])
                    print(retval)
                    for val in retval:
                        theref=jnf.get_referee_by_id(val)
                        print(theref)
                        if author['first_name'].lower() in theref[0].lower():
                            print(theref[0]+" matches")
                            ref_results.append([ val , theref[0] , type, contrib['track'][0:7], theref[4]])

print("---")
print(len(ref_results))
print(ref_results)

#sort by subMC
print('###')
ref_list=[ ref[3] for ref in ref_results]
ref_list_sorted=list(set([ ref[3] for ref in ref_results]))

print("---")
print(ref_list_sorted)
print(len(ref_list_sorted))

for ref in ref_list_sorted:
    indices = [i for i, x in enumerate(ref_list) if x == ref ]
    print(indices)
    for idx in indices:
        print(ref_results[idx])
    print("***")
#sort by referee
print('###')
ref_list=[ ref[0] for ref in ref_results]
ref_list_sorted=list(set([ ref[0] for ref in ref_results]))

all_refs=[]

print("---")
print(ref_list_sorted)
print(len(ref_list_sorted))

for ref in ref_list_sorted:
    all_refs.append([ref, []])
    indices = [i for i, x in enumerate(ref_list) if x == ref ]
    print(indices)
    theSubMCs=[]
    for idx in indices:
        print(ref_results[idx])
        val=0
        if 'speakers' in ref_results[idx][2]: 
            val=1
        elif 'primaryauthors' in ref_results[idx][2]:
            val=0.8
        else:
            val=0.1
        if ref_results[idx][3] in theSubMCs:
            jdx=theSubMCs.index(ref_results[idx][3])
            if all_refs[-1][1][jdx][1] < val:
                all_refs[-1][1][jdx][1]=val
        else:
            theSubMCs.append(ref_results[idx][3])
            all_refs[-1][1].append([ref_results[idx][3] , val ])
            jdx=-1
    print("***")
print("+++")
print(all_refs)
print(len(all_refs))


fname='split_MC_referees.data'
joblib.dump(all_refs,fname)


print("+++")
new_refs=joblib.load(fname)

print(new_refs)
print(len(new_refs))


