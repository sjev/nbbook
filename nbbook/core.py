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
    book = Book(Path(path)/config)
    return book.buildIndex()

       

    
#%% --------------Worker classes--------------------

class Reference():
    # parses "[ref]: # (A - b)" style referencs
    _regex = re.compile('.*\[ref\]:[\s#(]*(?P<category>[^-]+)-(?P<desc>[^)]+)') 
                   
    def __init__(self,category, description, target,parent=None):
        
        self.parent = parent # parent notebook or path
        self.category = category 
        self.description = description
        self.target = target # target header

    @classmethod
    def parse(cls, line):
        
        m = cls._regex.match(line)
        if m:
            return cls(m['category'].strip(),m['desc'].strip(),None)
        else:
            return None

    def linkTo(self):
        return self.target.linkTo(txt=self.description)
        

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
        
        
    def linkTo(self,txt=None, indent = 0):
        """ 
        markdown link to parent notebook 
        
        Parameters
        -------------
        txt :str
            text to display in link. If None is provided, header text will be used
        indent : int 
            amount of spaces to indent per level. Will also ad a * character
                
        """
        assert self.parent is not None, "Parent notebook is not set"
        if isinstance(self.parent, Notebook):
            target = self.parent.file.name
        elif  isinstance(self.parent, str):
            target = self.parent
          
        linkTxt = self.txt if txt is None else txt
            
        link = "[%s](%s#%s)" % (linkTxt,target,self.txt.replace(' ','-'))
        
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
        

class Book():
    """ class for bundling & indexing notebooks """
    def __init__(self,cfgFile):
        
        self._cfgFile = Path(cfgFile)
        self.path = self._cfgFile.parent # root folder
        self.config = yaml.load((self._cfgFile).open(mode='r'))
        
        # read notebooks
        self.notebooks = [Notebook(self.path/nb) for nb in self.config['notebooks'] ] 
        
        # init output notebook
        self.notebook = nbf.v4.new_notebook()
        self.notebook['cells'] = []
        
        # concat headers & references
        self.headers = []
        self.references = []
        for nb in self.notebooks:
            self.headers += nb.headers
            self.references += nb.references
            
        
        
        
    def buildIndex(self):
        """ create index (TOC) notebook """
        
        cfg = self.config
        
        lines = []
        links = []
        for h in self.headers:
            if h.level <= cfg['index']['max_depth']:
                links.append(h.linkTo(indent=cfg['index']['indent']))
                lines.append('#'*h.level+h.txt)
                
        md = '# Index\n' + '\n'.join(links)
        self.notebook['cells'].append(nbf.v4.new_markdown_cell(md))
        return md
    
    
    def buildReference(self):
        """ build reference notebook """
        
        
        index = {}
        for ref in self.references:
            if ref.category not in index:
                index[ref.category] = []
            index[ref.category].append(ref)
        
        lines = ['# Reference']
        for category in sorted(index.keys()):
            lines.append('\n## '+category)
            for ref in index[category]:
                lines.append(' * '+ref.linkTo())

        md = '\n'.join(lines) 

        self.notebook['cells'].append(nbf.v4.new_markdown_cell(md))

        return md           
    
    def write(self):
        """ write notebook """
        
        cfg = self.config
        
        # write notebook
        
        dest = (self.path/cfg['index']['name']).as_posix()
        print('Writing ',dest)
        nbf.write(self.notebook,dest)