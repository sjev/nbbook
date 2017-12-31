# -*- coding: utf-8 -*-

import nbformat as nbf
import re
from pathlib import Path
import yaml

#%% -------------Action functions-------------------

def buildIndex(path, config='book.yml'):
    """
    Build index notebook. 
    
    Parameters
    ------------
    path : str
        location of the notebooks folder
    config : str
        configuration yaml file.
    """
    path = Path(path)
    cfg = yaml.load((path/config).open(mode='r'))
    print(cfg)

    notebooks = [Notebook(path/nb) for nb in cfg['notebooks'] ]    
    print(notebooks)

#%% --------------Worker classes--------------------

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

class Reference():
    # parses "[ref]: # (A - b)" style referencs
    _regex = re.compile('.*\[ref\]:[\s#(]*(?P<category>[^-]+)-(?P<desc>[^)]+)') 
                   
    def __init__(self,category, description):
        
        self.category = category
        self.description = description

    @classmethod
    def parse(cls, line):
        
        m = cls._regex.match(line)
        if m:
            return cls(m['category'].strip(),m['desc'].strip())
        else:
            return None
            
        

class Header():
    """ header parser """
    _regex = re.compile('[^#]*(?P<hash>[#]+)[\s]+(?P<txt>[^\n]+)')    

    def __init__(self,txt,level):
        
        self.level = level
        self.txt = txt
        
    @classmethod
    def parse(cls, line):
        """ parse line, return None if not a header """
        
        m = cls._regex.match(line)
        if m:
            return cls(m['txt'].strip(),len(m['hash']))
        else:
            return None 
        
        
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
        
    def __repr__(self):
         return 'Header("%s")'% self.txt

class Notebook():
    """ notebook parsing class """
    p = re.compile('[^#]*(?P<hash>[#]+)[\s]+(?P<header>[^\n]+)')
    
    def __init__(self,fName):
        
        self.file = Path(fName)
        
        # parse
        self._data = nbf.read(self.file.as_posix(),as_version=4)
    
    @property
    def headers(self):
        """ list of headers """
        
        headers = []
        cells = self._data['cells']
        for cell in cells:
            if cell['cell_type'] == 'markdown':
                for line in cell['source'].splitlines():
                    h = Header.parse(line)
                    if h:  headers.append(h) 
        return headers
    
