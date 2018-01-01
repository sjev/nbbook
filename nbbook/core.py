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
        
    Returns
    --------
    int : number of elements in index
    """
    path = Path(path)
    cfg = yaml.load((path/config).open(mode='r'))

    notebooks = [Notebook(path/nb) for nb in cfg['notebooks'] ]    

    headers = []
    for nb in notebooks:
        for h in nb.headers:
            if h.level <= cfg['index']['max_depth']:
                headers.append(h.linkTo(indent=cfg['index']['indent']))
            
    md = '\n'.join(headers)
    
    
    
    # write notebook
    nb = nbf.v4.new_notebook()
    nb['cells'] = [nbf.v4.new_markdown_cell(md)]
    dest = (path/cfg['index']['name']).as_posix()
    nbf.write(nb,dest)

    return len(headers)
#%% --------------Worker classes--------------------

class Reference():
    # parses "[ref]: # (A - b)" style referencs
    _regex = re.compile('.*\[ref\]:[\s#(]*(?P<category>[^-]+)-(?P<desc>[^)]+)') 
                   
    def __init__(self,category, description, target,parent=None):
        
        self.parent = parent
        self.category = category
        self.description = description
        self.target = target

    @classmethod
    def parse(cls, line):
        
        m = cls._regex.match(line)
        if m:
            return cls(m['category'].strip(),m['desc'].strip(),None)
        else:
            return None
            
        

class Header():
    """ header parser """
    _regex = re.compile('[\s]*(?P<hash>[#]+)[\s]+(?P<txt>[^\n]+)')    

    def __init__(self,txt,level,parent=None):
        
        self.parent = parent # parent notebook
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
        
        
    def linkTo(self, indent = 0):
        """ 
        markdown link to parent notebook 
        
        Parameters
        -------------
        dest :str
            path to a notebook
        indent : int 
            amount of spaces to indent per level. Will also ad a * character
                
        """
        assert self.parent is not None, "Parent notebook is not set"
        if isinstance(self.parent, Notebook):
            target = self.parent.file.name
        elif  isinstance(self.parent, str):
            target = self.parent
            
        link = "[%s](%s#%s)" % (self.txt,target,self.txt.replace(' ','-'))
        
        if indent > 0:
            return indent*(self.level-1)*" "+"* "+link
        else:
            return link    
        
    def __repr__(self):
         return 'Header("%s")'% self.txt

class Notebook():
    """ notebook parsing class """
    p = re.compile('[^#]*(?P<hash>[#]+)[\s]+(?P<header>[^\n]+)')
    
    def __init__(self,fName):
        
        self.file = Path(fName)
        
        # parse
        self._data = nbf.read(self.file.as_posix(),as_version=4)
    
        self.headers = []
        self.references = []
        
        cells = self._data['cells']
        for cell in cells:
            if cell['cell_type'] == 'markdown':
                for line in cell['source'].splitlines():
                    h = Header.parse(line)
                    if h:
                        h.parent = self
                        self.headers.append(h) 
                    
                    r = Reference.parse(line)
                    if r: 
                        r.parent = self
                        r.target = self.headers[-1] # link to last known header
                        self.references.append(r)
        
    
   
