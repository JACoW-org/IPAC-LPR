# IPAC-LPR

This code manages the Light Peer Review at IPAC (or other jacow based conferences). It is meant to interface with indico.

##To get started:

1) Read the LPR.md file with generic advices about LPR.
2) Identify your conference ID in Jacow. It will look like https://indico.jacow.org/event/41/ with the 41 corresponding to IPAC'23 replaced by another value corresponding to your conference.
3) Create a file called "mailpwd.txt" in the directory above the directory wher you have downloaded this code. This file should contain the email password that will be used to send emails. It is used by email_func Do not save your email password in the git.
4) Populate the MC_coordinators.txt and MC_coordinators_emails.txt files with the relevant data


##History of this code:

This code was initially written in a rush for IPAC'23. Some of the coding was done quickly to address problems as the arose and might need to be rewritten/adapted to future needs.

As the code evolved, I tried to keep all the functionalities but some functionnalities needed at the begginning of the conference may have been lost or broken later.


##About the scripts in the repository

* The directory **tests** contains samples of codes that I find useful to test features.
* check_new_submission.py Checks if new papers or reviews have been submitted
* find_paper.py gives the status of a paper
* find_referee.py gives the status of a referee (including expertise)
* ask_for_author_form.py is a simple code that sends an email to ask the submission of the IoP author_form
* check_poster_police_status_accepted_papers.py checks the status of the paper with respect to the poster police checks.
* notify_all_authors_paper_published.py and notify_all_referees_who_have_reviewed_a_paper.py were used to inform the authors and the referees when the volum was published.

##To do list:
- The replacement of https://indico.jacow.org/event/41/ by {event_url}  has not been tested as it was done after the conference.
- As data access was slow, some data have been stored locally in excel files. On should look at what is necessary and if another data format would not be more appropriate. However, one should remember that excels files are easy to browse when something goes wrong with a paper.