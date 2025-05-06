#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  6 11:16:04 2025

This script is used to try to send an email

@author: delerue
"""

import params
import email_func as ef 

recipients=[ params.email_from_address ]
string_txt="Test email for LPR\nHello,\n this is a test email.\nIf you receive this email  it means that you are correctly configured.\nBye"
ef.email_txt(recipients,string_txt,show_message=True,send_me_a_copy=True)
print("Sending email done")



