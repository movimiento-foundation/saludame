#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by: Pablo Astigarraga (poteland@gmail.com)**
# License: GPLv3
# 
# Description: Base for Saludame, a health-awareness teaching game for children intended for Plan Ceibal OLPC laptops implemented in Uruguay. 
# 
# URL: http://ceibaljam.org/

"""
This module will read all html documents and subdirectories on a given directory and create a tree based on the directory disposition of the files in the following manner:

root directory
    DirectoryLevel1
        htmldocument1
        htmldocument2
    DirectoryLevel1
        DirectoryLevel2
            htmldocument1
            htmldocument2
            Directorylevel3
                htmldocument1
        htmldocument1
        htmldocument2
        htmldocument3
    DirectoryLevel1
        htmldocument1
        
        
Usage involves initializing an instance of the ContentTree object, this object will attempt to parse the root directory and create a hierarchy of topics consisting only of directories and .html files.

The default location will be a /content/ folder located on the same directory as the script calling the function. 
"""

import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

class ComplexContentTree(object):
    """A ComplexContentTree object will search for its contents recursively down a directory
    tree, creating one topic with each subdirectory that contains one or more html files. 
    Its intended use is to instanciate it, load contents and be able to reference each of its
    topics and files. Aiming at a graphical display the application will be able create a 
    representation of all topics and subtopics available and to pull the html content for each
    topic and present it as a help page."""  

    def __init__(self,root="content",load_content=True):     
        self.root = os.path.join(PROJECT_ROOT,root)
        if load_content:
            self.load_content()
        
        
    def load_content(self):
    	"""Will parse the root directory of the content tree for html files and create
    	the information tree.
     	"""
        if not self.root:
            raise Exception("No root directory has been assigned")
        
        if not os.path.exists(self.root):
            raise Exception("Invalid root directory - does not exist")
            
        all_topics = []
        for root, dirs, files in os.walk(self.root):
            if os.path.exists(root):
                new_topic = Topic(root)
                if (new_topic not in all_topics) and (new_topic.files != []):
                    all_topics.append(new_topic)  
  
        self.topics = all_topics    


             
class SimpleContentTree(object):
    """A SimpleContentTree object contains just one topic and and is intended for 
    lightweight implementations where only one level will be used (no additional 
    subdirectories other than the root dir)"""

    def __init__(self,root="content",load_content=True):     
         self.root = os.path.join(PROJECT_ROOT,root)
         if load_content:
             self.load_content()
             
             
    def load_content(self):        
        if not self.root:
            raise Exception("No root directory has been assigned")

        if not os.path.exists(self.root):
            raise Exception("Invalid root directory - does not exist")

        self.topic = Topic(self.root)
        self.topic.parent = None
                    
                    
                    
class Topic(object):
    """Minimum object - it will usually know its parent, title and files
    so that an application can easily create and display the content tree 
    by showing the html content of each of the topic's files """
 
    def __init__(self,path,parent=None):
        self.subdirectories,self.files = [],[]
        
        for thing in os.listdir(path):
            if os.path.isdir(os.path.join(path,thing)):
                self.subdirectories.append(os.path.join(path,thing))
            if (os.path.isfile(os.path.join(path,thing))) and (os.path.splitext(thing)[1] == '.html'):
                self.files.append(os.path.join(path,thing))

        self.parent = os.path.basename(os.path.dirname(path))
        self.title = os.path.basename(path)
        self.parent = parent      
        self.path = path
        
