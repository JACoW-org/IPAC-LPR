# Requestion date abut one contribution
# Nicolas Delerue, 3/2023

def printv(txt):
    print(txt," : ",eval(txt))

import jacow_nd_func as jnf

contribs=jnf.submitted_contribs()
printv('contribs')
for the_contrib_id in contribs:
    print('###')
    printv('the_contrib_id')
    contrib=jnf.find_contrib(the_db_id=the_contrib_id)
    #print(contrib)
    #print('---')
    #print(contrib.keys())
    print('---')
    print(contrib['title'])
    #print(contrib['id'])
    #print(contrib['db_id'])
    print(contrib['speakers'])
    print(contrib['speakers'][0]['first_name'],contrib['speakers'][0]['last_name'])
    print(contrib['speakers'][0]['affiliation'])
    jnf.load_affiliations_countries_file()
    country=jnf.get_country_from_affiliation(contrib['speakers'][0]['affiliation'])
    continent=jnf.get_continent(country)
    #print('Continent ',continent)
    print('---') 
    print(contrib['track'])

    referees=jnf.randomly_suggest_two_referees(contrib['track'],continent)
    #exit()
print(jnf.no_country_affiliation)
