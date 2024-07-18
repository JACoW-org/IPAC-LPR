#!/usr/local/bin/python3

# Check for consistency
# Nicolas Delerue, 4/2023


import jacow_nd_func as jnf
jnf.load_contribs()
jnf.submitted_contribs(force_online=True)
#jnf.submitted_contribs(force_online=False)
jnf.check_all_papers()
jnf.check_double_reviews_validated()

