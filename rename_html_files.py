#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 16:17:54 2022

@author: mihalis
"""


import os
import codecs
import re


directory = '/Users/mihalis/PycharmProjects/Bechdel_Test/scripts_html'
for filename in os.listdir(directory):
    filename_new = filename.replace(' ', "")
    filename_new = filename_new.replace('-', '_')
    
    os.rename(directory + '/'+ filename,directory + '/'+filename_new)