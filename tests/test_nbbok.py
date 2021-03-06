#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 18:17:45 2017

@author: jev
"""
#import pytest
from pathlib import Path
from testpath import assert_isfile

import nbbook as book

EXAMPLE_REF = " [ref]: # (Nulla sit amet - chapter 2)   \n" 

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
    



def test_Header():
    
    # this is not a heading
    line = EXAMPLE_REF
    h = book.Header.parse(line)
    assert h is None
   
    # this is a heading
    line = " ## Heading ABC##"
    h = book.Header.parse(line)
    h.parent = 'test.ipynb'
    
    assert isinstance(h, book.Header)
    assert h.level == 2
    assert h.txt == 'Heading ABC'
    
    link = h.linkTo()
    assert link == '[Heading ABC](test.ipynb#Heading-ABC)'
    
    link = h.linkTo('Foo')
    assert link == '[Foo](test.ipynb#Heading-ABC)'
    
    link = h.linkTo(indent=2)
    assert link == '  * [Heading ABC](test.ipynb#Heading-ABC)'
    
    
    return h

def test_Reference():
    
    line = " # No reference here ..."
    r = book.Reference.parse(line)
    assert r is None
    
    
    line = EXAMPLE_REF
    r = book.Reference.parse(line)

    assert r.category == 'Nulla sit amet'
    assert r.description == 'chapter 2'

    h = test_Header()
    r.target = h
    
    link = r.linkTo()
    assert link == '[chapter 2](test.ipynb#Heading-ABC)'

    
def test_Notebook():
    
    nbFile =  exampleDir / 'notebook_one.ipynb'# get example filename
    n = book.Notebook(nbFile)
    
    link = n.headers[0].linkTo()
    assert link == '[Part One](notebook_one.ipynb#Part-One)'
    
    
    headers = [h.txt for h in n.headers]
    assert len(headers) == 5
    assert 'Part One' in headers
    assert 'Chapter Two' in headers
    

def test_Book():
    
    b = book.Book(exampleDir / 'book.yml')
    
    assert len(b.headers) == 10
    assert len(b.references) == 4
    
    #--- index
    outFile = exampleDir / '_index.ipynb'
    if outFile.exists(): outFile.unlink()
    md = b.buildIndex()
    
    lines = md.splitlines()
    assert len(lines) == 10
    
    
    #---reference
    md = b.buildReference()
    b.write()
    
    
    lines = md.splitlines()
    
    
    assert lines[0] == '# Reference'
    assert outFile.exists()

if __name__=="__main__":
    
    test_exampleDir()