#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 18:17:45 2017

@author: jev
"""
import pytest
from pathlib import Path
from testpath import assert_isfile

import nbbook as book


exampleDir = Path(__file__).parents[1] / 'example'

print(exampleDir)

#@pytest.mark.skip
def test_exampleDir():
    """ check that example dir is present """
    
    print( exampleDir.exists())
    assert_isfile(exampleDir / 'notebook_one.ipynb')

def test_re():
    
    import re
    
    line = " [ref]: # (Nulla sit amet - chapter 2)\n" 

    pattern = re.compile('.*\[ref\]:[\s#(]*(?P<category>[^-]+)-(?P<desc>[^)]+)')
    m = pattern.match(line)

    print(m)    
    if m is not None:
        print(m.groupdict())    

if __name__=="__main__":
    
    test_re()