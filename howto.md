### How tos

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