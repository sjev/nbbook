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
    testNb = exampleDir / 'notebook_one.ipynb'
    assert_isfile(testNb)
    return testNb
    

def test_Reference():
    
    line = " No reference here ..."
    r = book.Reference.parse(line)
    assert r is None
    
    
    line = " [ref]: # (Nulla sit amet - chapter 2)   extra characters\n" 

    r = book.Reference.parse(line)


    assert r.category == 'Nulla sit amet'
    assert r.description == 'chapter 2'


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
    
    
def test_Notebook():
    
    nbFile = test_exampleDir() # get example filename
    n = book.Notebook(nbFile)
    
    print('Headers:', n.headers)
    
    headers = [h.txt for h in n.headers]
    assert 'Part One' in headers
    assert 'Chapter Two' in headers

if __name__=="__main__":
    
    test_exampleDir()