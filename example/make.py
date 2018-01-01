#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build book script

"""



import sys
import nbbook # this is where the magic happens 

book = nbbook.Book('book.yml')

ACTIONS = {}

def action(func):
    """ decorator to collect actionable functions """
    ACTIONS[func.__name__]=func
    return func
    

#%% action functions
     
@action 
def reference():
    """ show structure """
    book.buildReference()
    
@action 
def index():
    """ make index notebook """
    book.buildIndex()

#%%    
if __name__=="__main__":

    if len(sys.argv) == 1 :
        print('please provide action')
        print('available actions:',list(ACTIONS.keys()))
        
    else:
        func = ACTIONS[sys.argv[1]]
        func()
