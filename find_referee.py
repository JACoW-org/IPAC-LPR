#!/usr/local/bin/python3

# Find info about a referee
# Nicolas Delerue, 3/2023

import jacow_nd_func as jnf
import argparse
import numpy as np
import joblib



parser = argparse.ArgumentParser()
parser.add_argument("--id", nargs=1, help="The referee id")
parser.add_argument("--name", nargs=1, help="The referee name")
parser.add_argument("--MC", nargs=1, help="Find all referee for a given MC")
parser.add_argument("--subMC", nargs=1, help="Find all referee for a given subMC in any MC")
parser.add_argument("--extra", action="store_true", help="Looks for extra referees")
parser.add_argument("--all", action="store_true", help="List all referees taht can receive a paper")
parser.add_argument("--map-subMC", action="store_true", help="Create a map of referees and participants by sub MC")
parser.add_argument("--paper","-p", nargs=1, help="Suggest referees matching this paper")
parser.add_argument("--search-MC", nargs=1, help="Search for referee in the specified MC instead of the paper MC")
parser.parse_args()
args = parser.parse_args()
#print(args)

allrefdata_fname=jnf.allrefdata_fname

ref_id=None

if args.id is not None:
    print("Looking for info about referee "+args.id[0])
    ref_id=[ args.id[0] ]
                    
if args.name is not None:
    ref_id=jnf.find_referee_by_name(args.name[0])
    if ref_id is None:
        print("No referee natching this name or this id.")

if ref_id is not None:            
    #Get referee info    
    for the_id in ref_id:
        print('Checking ref id',the_id)
        print(jnf.get_referee_by_id(the_id))
        print(jnf.check_papers_for_referee(the_id))
        print(jnf.check_history_for_referee(the_id))
        print('Can get more?', jnf.can_referee_get_additional_paper(the_id))
        
if (args.MC is not None):
    refs_dict=jnf.find_referees_for_MC(MC=args.MC[0])
elif (args.subMC is not None):
    refs_dict=jnf.find_referees_for_MC(sub=args.subMC[0])
    
if (args.MC is not None or args.subMC is not None):

    print("*** Can not get ***")
    for the_ref in refs_dict['can_not_get']:        
        print('Referee info (can not get more papers): ',the_ref[0],the_ref[1])
    print("*** Additionals ***")
    for the_ref in refs_dict['additionals']:
        print("=> Possible additional: ", the_ref[0],  the_ref[1],  the_ref[2]) 
    print("*** Can get ***")
    #print(can_get)
    for the_ref in refs_dict['can_get']:     
        ref=jnf.get_referee_by_id(the_ref[1])
        print('=> Referee info (available): ',the_ref[0],the_ref[1],the_ref[2],ref)
        for hist in jnf.check_history_for_referee(int(the_ref[1])):
            print("\t",hist)
    if args.MC is not None:
        print("+++ Query was MC",args.MC[0])
    if args.subMC is not None:
        print("+++ Query was subMC",args.subMC[0])

def sort_list_other_area_ref(list_ref,geodict):
    list_match_other_continent=[]
    list_match_other_country=[]
    for ref in list_ref:
        ref_dict=jnf.get_referee_dict_by_id(ref[1])
        ref_cont=jnf.get_continent(ref_dict['country'])
        if ref_cont not in geodict['continent']:
            list_match_other_continent.append(ref)
        if ref_dict['country'] not in geodict['countries']:
            list_match_other_country.append(ref)
    other_area_dict={}
    other_area_dict['country']=list_match_other_country
    other_area_dict['continent']=list_match_other_continent
    return other_area_dict

def sort_list_other_area_add(list_ref,geodict):
    list_match_other_continent=[]
    list_match_other_country=[]
    for ref in list_ref:
        ref_dict=ref[2]
        ref_cont=jnf.get_continent(ref_dict['country'])
        if ref_cont not in geodict['continent']:
            list_match_other_continent.append(ref)
        if ref_dict['country'] not in geodict['countries']:
            list_match_other_country.append(ref)
    other_area_dict={}
    other_area_dict['country']=list_match_other_country
    other_area_dict['continent']=list_match_other_continent
    return other_area_dict

def print_auth_list(the_list):
    for auth in the_list:
        print(auth)

if args.paper is not None:
    contrib=jnf.find_contrib(the_id=args.paper[0])
    print("Looking for referees suitable for paper "+args.paper[0]," Track: ", contrib['track'][0:7])
    geodict=jnf.get_countries_from_contrib(contrib)

    [n_declined,list_declined]=jnf.check_paper_for_declined(contrib['id'])
    #print('Declined by ',list_declined)
    if args.search_MC is None:
        the_track=contrib['track']
    else:
        the_track=args.search_MC[0]
        print("Overriding paper's track",the_track," instead of ", contrib['track'])

    refs_dicts={}
    shown_list=[]
    n_found=0
    txt=""
    suggested_reviewer=""

    for get_type in ['can_get' , 'additionals']:
        for auth_type in  ['author','co-author' , 'additional' ] :
            for full_match in  [ True, False]:
                if n_found<5:
                    if auth_type == 'author':
                        if full_match:
                            refs_dicts[str(full_match)]=jnf.find_reviewer_for_MC(MC=the_track[0:7])
                        else:
                            refs_dicts[str(full_match)]=jnf.find_reviewer_for_MC(sub=the_track[4:7],excepted=the_track[0:7])
                    if full_match:
                        txt_match="Full match: "+the_track
                    else:
                        txt_match="Sub match: "+the_track[4:7]
                    
                    refs_dicts[str(full_match)][get_type]=jnf.remove_authors_from_list(contrib,refs_dicts[str(full_match)][get_type])

                    #print(refs_dicts[str(full_match)][get_type])
                    list_authors=[ auth for auth in refs_dicts[str(full_match)][get_type] if auth[0] == auth_type and str(auth[1]) not in list_declined]
                    if get_type == 'additionals':
                        list_other_area=sort_list_other_area_add(list_authors,geodict)
                    else:
                        list_other_area=sort_list_other_area_ref(list_authors,geodict)
                    #print('list_other_area',list_other_area)
                    if list_other_area is not None:
                        n_found=n_found+len(list_other_area['country'])
                        #print(list_other_area['continent'])
                        #print(list_other_area['country'])
                        print(txt_match,auth_type,"found: ", len(list_other_area['country'])," total:",n_found)
                        group_txt=""
                        for area in [ 'continent' , 'country']: 
                            if list_other_area[area] is not None:
                                this_txt=""
                                print("Added list shuffle here")
                                random.shuffle(list_other_area[area])                                
                                for auth in list_other_area[area]:
                                    if auth[1] not in shown_list:
                                        shown_list.append(auth[1])
                                        if get_type == 'can_get':
                                            if jnf.can_referee_get_additional_paper(auth[1]):
                                                if len(suggested_reviewer)==0:
                                                    suggested_reviewer=str(auth[1])
                                                this_txt=this_txt+str(auth[1])+": "+str(auth[2])+"\n"
                                                this_txt=this_txt+"\t Can get papers? "+str(jnf.can_referee_get_additional_paper(auth[1]))+"\n"
                                                this_txt=this_txt+"\t"+str(jnf.referee_data_file_get_line(auth[1]))+"\n"
                                                for ref_paper in jnf.check_history_for_referee(auth[1]):
                                                    this_txt=this_txt+"\t\t"+str(ref_paper)+"\n"
                                                this_txt=this_txt+"\n"
                                        else:
                                            this_txt=this_txt+"(add) "+str(auth[1])+" : "+str(auth[2]['name'])+" / "+str(auth[2]['affiliation'])+" / "+str(auth[2]['country'])+"\n"
                                if (len(this_txt)>0):
                                    this_txt="--- "+ auth_type +"s - Area: "+ area + " \n"+this_txt+"\n"
                                    
                                    group_txt=this_txt+group_txt
                        if len(group_txt)>0:
                            group_txt="***** "+ txt_match +" *****\n"+group_txt
                            txt=group_txt+txt
    print("\n#####\n")
    print('Continent ', geodict['continent'])
    print('Countries ',geodict['countries'])
    if n_found==0:
        print("No matching referee found")
    else:
        print("Found ", n_found," possibilities")
        print(txt)
        print('Paper: ',args.paper[0],contrib['title'])
        print("Suggestion: ./assign_referee.py --paper ",args.paper[0]," --referee ",suggested_reviewer)
           
if args.map_subMC:
    jnf.load_contribs()
    the_sub_MC_list=[]
    all_referees_by_sub_MC=[]
    all_referees_by_sub_MC_coauthors=[]
    unavailable_referees=jnf.load_referees_unavailable()
    contribs=jnf.submitted_contribs()
    for contrib in jnf.data_json_contribs["results"][0]['contributions']:
        if (contrib['track'] is not None):
            if not contrib['track'][0:7] in the_sub_MC_list:
                print("Adding",contrib['track'][0:7])
                the_sub_MC_list.append(contrib['track'][0:7])
                all_referees_by_sub_MC.append([])
                all_referees_by_sub_MC_coauthors.append([])
                print(the_sub_MC_list)
            idx=the_sub_MC_list.index(contrib['track'][0:7])
            #print('Contrib id',contrib['id'],' db_id',contrib['db_id'])
            the_paper=jnf.get_paper_info(str(contrib['db_id']),use_cache=True)
            #print(the_paper)
            #print(the_paper['last_revision']['submitter'])
            if (the_paper is not None):
                submitter_name=the_paper['last_revision']['submitter']['full_name']
                submitter_email=the_paper['last_revision']['submitter']['email']            
                print('\tsubmitter_name',submitter_name)
                #print('submitter_email',submitter_email)
                referee_data=jnf.get_referee_dict_by_email(submitter_email)
                if referee_data is None:
                    participant=jnf.find_participant_by_name(submitter_name)
                    if participant is not None:
                        if participant['category']=='Student':
                            pass
                        else:
                            #print("\tMatching participant found: ",participant)
                            all_referees_by_sub_MC[idx].append(participant['email'])
                else:
                    if( int(referee_data['id']) in unavailable_referees):
                        #print("\tUnavailable")
                        pass
                    else:
                        all_referees_by_sub_MC[idx].append(referee_data['id'])
            for auth_type in ['speakers' , 'primaryauthors' ,'coauthors' ]:
                for speak in contrib[auth_type]:
                    speak_name=speak['first_name']+" "+speak['last_name']
                    print('\tSpeak name:',speak_name)
                    speak_ref=jnf.find_referee_by_name(speak_name)
                    if len(speak_ref)==0:
                        participant=jnf.find_participant_by_name(speak_name)
                        if participant is not None:                    
                            if participant['category']=='Student':
                                #print("\tMatching participant (student) found: ",participant)
                                pass
                            else:
                                print("\tMatching participant found: ",participant)
                                #participants_available_not_submitted.append(participant)
                                if auth_type == 'coauthors': 
                                    all_referees_by_sub_MC_coauthors[idx].append(participant['email'])
                                else:
                                    all_referees_by_sub_MC[idx].append(participant['email'])
                    else:
                        referee_data=jnf.get_referee_dict_by_id(speak_ref[0])
                        if( int(referee_data['id']) in unavailable_referees):
                            #print("\tUnavailable")
                            pass
                        else:                    
                            if auth_type == 'coauthors': 
                                all_referees_by_sub_MC_coauthors[idx].append(referee_data['id'])
                            else:
                                all_referees_by_sub_MC[idx].append(referee_data['id'])
    for subMC in the_sub_MC_list:
        idx=the_sub_MC_list.index(subMC)
        print(subMC,idx)
        #print(all_referees_by_sub_MC[idx])
        print(list(set(all_referees_by_sub_MC[idx])))
        print(list(set(all_referees_by_sub_MC_coauthors[idx])))
        all_referees_by_sub_MC[idx]=list(set(all_referees_by_sub_MC[idx]))
        all_referees_by_sub_MC_coauthors[idx]=list(set(all_referees_by_sub_MC_coauthors[idx]))
    print("**** MC map: *****")
    print('the_sub_MC_list')
    print(the_sub_MC_list)
    print('all_referees_by_sub_MC')
    print(all_referees_by_sub_MC)
    joblib.dump([the_sub_MC_list,all_referees_by_sub_MC,all_referees_by_sub_MC_coauthors],allrefdata_fname)


if args.all:
    all_refs=jnf.get_all_referees_from_file()
    refs_available=[]
    no_paper=[]
    for the_ref in all_refs:
        if jnf.can_referee_get_additional_paper(the_ref):
            refs_available.append(the_ref)
            papers_ref=jnf.check_papers_for_referee(the_ref)
            if (papers_ref['n_papers']==0):
                no_paper.append(the_ref)
    print("*** Referees who can get additional papers ***")
    for the_ref in reversed(refs_available):
        if the_ref < 200000:
            print('Checking ref id',the_ref)
            print('\tCan get more ', jnf.can_referee_get_additional_paper(the_ref))
            print("\t",jnf.get_referee_by_id(the_ref))
            print("\t",jnf.referee_data_file_get_line(the_ref))
            print("\t\t",jnf.check_history_for_referee(the_ref))
            papers_ref=jnf.check_papers_for_referee(the_ref)
            print("\t\t", papers_ref)
    print("*** Referees with no papers ***")
    for the_ref in reversed(no_paper):
        if the_ref < 200000:
            print('Ref id (no paper)',the_ref)
            print("\t",jnf.get_referee_by_id(the_ref))
            print("\t",jnf.referee_data_file_get_line(the_ref))
            print("\t\t",jnf.check_history_for_referee(the_ref))
            papers_ref=jnf.check_papers_for_referee(the_ref)
            print("\t", papers_ref)
    print('Total referees ',len(all_refs))
    print('N referees available',len(refs_available))
    print('N referees with no papers', len(no_paper))
    
