# -*- coding: utf-8 -*-

import nbformat as nbf
import re
from pathlib import Path

#foo
def lineIsHeader(line):      
    
    if not line.strip(): # empty line
        return False 
    
    if line.strip()[0] != "#": # not a header
        return False
    
    return True

def headerToLink(line, srcNotebook):
    """ 
    transform line to markdown link in a notebook 
    returns 
        link : markdown link to a notebook
        header : indented header text
        level : 
    
    """
    
    p = re.compile('[^#]*(?P<hash>[#]+)[\s]+(?P<header>[^\n]+)')
    m = p.match(line)
    
    level = len(m['hash'])
    header = m['header']
            
    dest = Path(srcNotebook)
    
    txt = line.strip('#').strip() # stripped text
    link = 4*(level-1)*" "+"* [%s](%s#%s)" % (txt,dest.name,txt) #
    #header = 3*(level-1)*" "+txt
    
    return link, header, level

class Header():
    """ header parser """
    p = re.compile('[^#]*(?P<hash>[#]+)[\s]+(?P<txt>[^\n]+)')    

    def __init__(self,line):
        
        assert lineIsHeader(line), "Not a valid header string"
        m = self.p.match(line)
        self.level = len(m['hash'])
        self.txt = m['txt']
        
        
    def linkTo(self,dest, indent = 0):
        """ 
        markdown link to existing notebook 
        
        Parameters
        -------------
        dest :str
            path to a notebook
        indent : int 
            amount of spaces to indent per level. Will also ad a * character
                
        """
        if indent > 0:
            return indent*(self.level-1)*" "+"* [%s](%s#%s)" % (self.txt,dest,self.txt)
        else:
            return "[%s](%s#%s)" % (self.txt,dest,self.txt)    
        
        

class Notebook():
    """ notebook parsing class """
    p = re.compile('[^#]*(?P<hash>[#]+)[\s]+(?P<header>[^\n]+)')
    
    def __init__(self,fName):
        
        self.file = Path(fName)
        
        # parse
        self.data = nbf.read(self.file.as_posix(),as_version=4)
        
        