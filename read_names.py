#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 00:36:37 2022

@author: mihalis
"""



def read_name_file(filename):
    """Read a file containing a list of names
        Args:
            filename: a file containing a name for each row
        Returns:
            An array of names from the input file
    """
    names = []
    with open(filename, "r") as f:
        for line in f:
            if not line.startswith("#") and line.strip() != "":  # remove comments and empty lines
                names.append(line.strip().lower())
    return names      


female_list = read_name_file('female.txt')

male_list = read_name_file('male.txt')
