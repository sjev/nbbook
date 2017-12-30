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
    
    line = " [ref]: # (Nulla sit amet - chapter 2)   extra characters\n" 

    pattern = re.compile('.*\[ref\]:[\s#(]*(?P<category>[^-]+)-(?P<desc>[^)]+)')
    m = pattern.match(line)


    assert m['category'].strip() == 'Nulla sit amet'
    assert m['desc'].strip() == 'chapter 2'


def test_Header():
    
    with pytest.raises(AssertionError):
        book.Header(" Just some text")
    
    
    line = " ## Heading ABC"
    h = book.Header(line)
    
    
    assert h.level == 2
    assert h.txt == 'Heading ABC'
    
    link = h.linkTo('test.ipynb')
    assert link == '[Heading ABC](test.ipynb#Heading ABC)'
    
    link = h.linkTo('test.ipynb', indent=2)
    assert link == '  * [Heading ABC](test.ipynb#Heading ABC)'

if __name__=="__main__":
    
    test_exampleDir()