### Setting up the LPR scripts

1. Check that the LPR module in indico is setup. See instructions at [here](./module.md).

1. Download the code at https://github.com/JACoW-org/IPAC-LPR 

1. The scripts have been written to work with python3

1. In indico (after login in), click on your name on the top-right corner, then click on "My preferences", go to API tokens, create a new API token with all permissions and save it carefully.

1. In the directory above the directory where you have downloaded the scripts, 
create a file "api_token.txt" with the indico API token create at the previous 
step and a "mailpwd.txt" with the password to send emails (do not put these information on a publicly visible location).

1. Identify the indico code of the previous conferences from the same series (example: IPAC 23 was at https://indico.jacow.org/event/41/ so its code is 41;  IPAC24=63; IPAC25=81)

1. Create the map of referees by running:
    ./map_authors_to_MC.py --confid 41,63 
This will create a map of all contributors to IPAC (based on their Jacow database ID) for the selected conferences.