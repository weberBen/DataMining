#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
from anytree import AnyNode, RenderTree, PreOrderIter
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter
import string
import json
import os
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import unicodedata
from num2words import num2words
from nltk.corpus import stopwords
import re

'''
import nltk
nltk.download()
nltk.download('stopwords')
nltk.download('punkt')
'''

#%%
class AlphabeticTree:
    def __init__(self, tree_filename=None):
        
        res = self.__loadTree__(tree_filename)
        if res is None:
            self.index = 0
            self.tree = self.__createEmptytree__()
        else :
            self.index, self.tree = res[0], res[1]
        
    
    #-------------------------------------------------------
    #
    #-------------------------------------------------------
    def __loadTree__(self, filename):
        str_tree = None
        index = 0
        
        if not os.path.exists(filename):
            return None
        
        with open(filename, 'r') as file:
            try :
                index = int(file.readline())
            except ValueError:
                return None
            str_tree = file.read()
        
        importer = JsonImporter()
        try :
            tree = importer.import_(str_tree)
        except json.JSONDecodeError:
            return None
        
        return index, tree
    
        
    def __createNode__(self, parent, letter):
        return AnyNode(id=None, label=letter, end=False, parent=parent)
    
    def __createEmptytree__(self):
        root = AnyNode(id="root")
        #self.__initializeNode__(root)
       
        return root
        
    def toFile(self, filename):
        exporter = JsonExporter(indent=0, sort_keys=False)
        with open(filename, 'w') as file:
            file.write(str(self.index))
            file.write("\n")
            file.write(exporter.export(self.tree))
    
    def toString(self):
        return RenderTree(self.tree)
    
    def __getNodeId__(self):
        val = self.index
        self.index+=1
        
        return val
        
    #-------------------------------------------------------
    #
    #-------------------------------------------------------
    def __getNode__(self, node, letter):
        for elm in node.children:
            if elm.label == letter:
                return elm
        
        return None
            
    def addWord(self, word_str):
        if word_str is None:
            return None
        
        node = self.tree
        for letter in word_str:
            
            child = self.__getNode__(node, letter)
            if child is None:
                child = self.__createNode__(node, letter)
            node = child
        
        if node == self.tree:
            return None
        
        if not node.end :
            node.end = True
            node.id = self.__getNodeId__()
        
    def getId(self, word_str):
        node = self.tree
        print("-----------------------------------")
        print("word=", word_str)
        for letter in word_str:
            child = self.__getNode__(node, letter)
            if child is None:
                return None
            node = child
        
        if node.end:
            return node.id
        else:
            return None
    
    def __getWordPath__(self, leaf_node):
        word = ""
        node = leaf_node
        
        while node!=self.tree:
            word = node.label + word
            node = node.parent
        
        return word
    
    def size(self):
        return self.index
    #%%
    
    def iterator(self):
        return self.__Iterator__(self)
    
    class __Iterator__():
        def __init__(self, Tree):
            self._obj = Tree
            self._iterator = PreOrderIter(self._obj.tree, filter_=lambda node: node.is_leaf)
            
            self._next_word = self.__getNext__()
            if self._next_word is None:
                self._hasNext = False
            else:
                self._hasNext = True
        
        def hasNext(self):
            return self._hasNext
        
        def __getNext__(self):
            
            try:
                node = next(self._iterator)
                return self._obj.__getWordPath__(node)
                
            except StopIteration:
                self._hasNext = False
            
            return None
        
        def getNext(self):
            
            tmp = self._next_word
            self._next_word = self.__getNext__()
            return tmp
            
#%%
#SnowballStemmer(language)
class Language:
    def __init__(self):
        self._stemmer = SnowballStemmer("english")
        self._stop_words = set(stopwords.words('english')) 
        
    def __removeAccent__(self, text):
        #https://stackoverflow.com/questions/44431730/how-to-replace-accented-characters-in-python?rq=1
        try:
            text = unicode(text, 'utf-8')
        except NameError: # unicode is a default on python 3 
            pass
    
            text = unicodedata.normalize('NFD', text)\
               .encode('ascii', 'ignore')\
               .decode("utf-8")
    
        return str(text)
    
    def __numberToTextFunction__(self, num):
        try :
            num = int(num)
        except ValueError :
            return None
        
        return num2words(num, lang='en')
    
    def normalize(self, word):
        word = word.lower()
        
        regex = re.compile('[%s]' % re.escape(string.punctuation))
        word = regex.sub(' ', word)
        #word = word.translate(str.maketrans('', '', string.punctuation))
        word = word.strip()
        
        
        if len(word)==0:
            return None
        
        if word in self._stop_words:
            return None
        
        tmp = self.__numberToTextFunction__(word)
        if tmp is not None:
            word = tmp
        
        tmp = self.__removeAccent__(word)
        if word is not None:
            word = tmp
        
        word = self._stemmer.stem(word)
        
        return word
#%%

class WordsBag:
    def __init__(self, filename):
        self._filename = filename
        logging.info("loading dictionnary")
        self._dico = AlphabeticTree(filename)
        logging.info("dictionnary loaded")
        self._Language = Language()
    
    def __addWord__(self, word_str):
        word = self._Language.normalize(word_str)
        if word is not None:
            self._dico.addWord(word)
    
    def populateFromTxt(self, text):
        token_txt = word_tokenize(text)
        for word in token_txt:
            self.__addWord__(word)
    
    def update(self):
        self._dico.toFile(self._filename)
    
    def getId(self, word):
        word = self._Language.normalize(word)
        return self._dico.getId(word)
    
    def iterator(self):
        return self._dico.iterator()
    
    def toString(self):
        return self._dico.toString()
    
    def size(self):
        return self._dico.size()
    
    def initialize(self, database_obj):
        it = database_obj.iterator()
        
        while it.hasNext():
            movie = it.getNext()
            print(movie.title)
            self.populateFromTxt(movie.summary)
        
        
    
#%%

'''
import DataParser
db = DataParser.Database('/home/benjamin/Documents/UPMC/L3/Projet_Math/DataMining/Dataset/CleanMovieData')

dico = WordsBag('/home/benjamin/Documents/UPMC/L3/Projet_Math/DataMining/Dataset/dictionnary')
#dico.initialize(db)

print(dico.size())
'''

'''
l = Language()
print("|",l.normalize("hello ?"),"|")

token_txt = word_tokenize("salut Mr.Henry est là ?")
for word in token_txt:
    print(l.normalize(word))
'''

'''
print(RenderTree(root))
print(s0.children[0].bar)

y = io.StringIO('there is a lot of blah blah in this so-called file')
print(y.read(1))

'''

'''
tree = AlphabeticTree('/home/benjamin/Documents/UPMC/L3/Projet_Math/DataMining/Test/dataManagement/Dictionnary.py')
tree.addWord("bonjour")

tree.addWord("bonsoir")
tree.addWord("bon")
tree.addWord("bonne")
tree.addWord("bonneap")
print(tree.toString())
print(tree.getId('bon'))
tree.toFile("./test")
#print(tree.tree.leaves)

it = tree.iterator()

while it.hasNext():
    print(it.getNext())
'''

'''
it = PreOrderIter(tree.tree, filter_=lambda node: node.is_leaf)

while True:
    try:
        node = next(it)
        #print(node.parent)
        print(__getWordPath__(tree.tree, node))
    except StopIteration:
        break


tree2 = AlphabeticTree("./test")
print(tree2.toString())
print(tree2.index)'''