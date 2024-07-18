#Reads the referees file
#Nicolas Delerue, 3/2023

import sys
sys.path.insert(0, '')

import openpyxl
import jacow_nd_func as jnf

def printv(txt):
    print(txt," : ",eval(txt))

printv('jnf.max_referees')
#jnf.get_referee_by_id('666')
#jnf.get_referee_by_id(666)

jnf.assign_referees_to_MC()
jnf.stats_for_all_MC()

