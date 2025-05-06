### How to?

### How to find help on a script?
Most script accept the "--help" argument to give their syntax.

#### How to create the Authors' subtrack map?
Use the script ./map_authors_to_MC.py with the indico conference identifiers as arguments.
Example:
    ./map_authors_to_MC.py --confid 41,63,81
    
### How to find all authors who have published in a given subtrack
After creating the authors map, use the script ./read_authors_map.py with the subtrack as argument 
Example:
    ./read_authors_map.py --subMC MC8.U01
    
### How to find all reviewers who have published in a given subtrack
After creating the authors map, use the script ./read_authors_map.py with the subtrack as argument and --only_reviewers as extra argument
Example:
    ./read_authors_map.py --subMC MC8.U01 --only_reviewers

### How to find an author?
After creating the authors map, use the script ./find_user.py you can search by last name, first name or database id.
Examples:
    ./find_user.py --last_name delerue
    ./find_user.py --first_name nicolas
    ./find_user.py --db_id 877
    
### How to check the subtracks (subMC) of all reviewers?
After creating the authors map, use the script ./read_authors_map.py with  --check_reviewers as argument
Example:
    ./read_authors_map.py --check_reviewers

### How to test that email is properly setup?
Execute:
    python test_send_email.py
This should send an email to yourself.

### How to assign a paper to a reviewer?
Find the paper id and the referee id (using find_user) and then:
    ./assign_referee.py --paper 149 --referee 877
Note that for IPAC'25, paper ID are 4-digit number mostly starting with 8. This is not a 3-digit number.
For IPAC 26 and beyong it will be 5-digits numbers.

### How to unassign a paper to a reviewer?
If a reviewer is unavailable, you can unassign him from a paper with the command:
    ./assign_referee.py --paper 149 --referee 877 --unassign


