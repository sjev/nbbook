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

def test_yaml():
    """ check that config file can be parsed correctly """
    import yaml
    cfg = yaml.load((exampleDir/'book.yml').open(mode='r'))

    assert 'notebook_one.ipynb' in cfg['notebooks']
    assert 'max_depth' in cfg['index']
    assert cfg['index']['name'] == '_index.ipynb'

#@pytest.mark.skip
def test_exampleDir():
    """ check that example dir is present """
    
    testNb = exampleDir / 'notebook_one.ipynb'
    assert_isfile(testNb)
    

def test_Reference():
    
    line = " # No reference here ..."
    r = book.Reference.parse(line)
    assert r is None
    
    
    line = " [ref]: # (Nulla sit amet - chapter 2)   extra characters\n" 

    r = book.Reference.parse(line)


    assert r.category == 'Nulla sit amet'
    assert r.description == 'chapter 2'


def test_Header():
    
    # this is not a heading
    line = " [ref]: # (Nulla sit amet - chapter 2)   \n" 
    h = book.Header.parse(line)
    assert h is None
   
    # this is a heading
    line = " ## Heading ABC"
    h = book.Header.parse(line)
    
    assert isinstance(h, book.Header)
    assert h.level == 2
    assert h.txt == 'Heading ABC'
    
    link = h.linkTo('test.ipynb')
    assert link == '[Heading ABC](test.ipynb#Heading-ABC)'
    
    link = h.linkTo('test.ipynb', indent=2)
    assert link == '  * [Heading ABC](test.ipynb#Heading-ABC)'
    
    
def test_Notebook():
    
    nbFile =  exampleDir / 'notebook_one.ipynb'# get example filename
    n = book.Notebook(nbFile)
    
    headers = [h.txt for h in n.headers]
    
    assert len(headers) == 5
    assert 'Part One' in headers
    assert 'Chapter Two' in headers
    
#@pytest.mark.skip   
def test_buildIndex():

    outFile = exampleDir / '_index.ipynb'
    if outFile.exists(): outFile.unlink()
 
    path = exampleDir.as_posix()    
    
    nrHeaders = book.buildIndex(path)
    
    assert nrHeaders == 9
    
    assert outFile.exists()

if __name__=="__main__":
    
    test_exampleDir()