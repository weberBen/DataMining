#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
from anytree import AnyNode, RenderTree, PreOrderIter
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter
import json
import os
import sys
import datetime

if __name__ == "__main__":
    from Language import Language
else:
    from dataManagement.Language import Language
    

'''
import nltk
nltk.download()
nltk.download('stopwords')
nltk.download('punkt')
'''


#%%
class AlphabeticTree:
    def __init__(self, tree_filename=None, erease=False):
        
        res = self._loadTree(tree_filename, erease)
        if res is None:
            logging.info("new alphabetical tree has been created")
            self._index = 0
            self._tree = self._createEmptytree()
        else :
            logging.info("alphabetical tree has been loaded from file")
            self._index, self._tree = res[0], res[1]
        
    
    #-------------------------------------------------------
    #
    #-------------------------------------------------------
    def _loadTree(self, filename, erease):
        str_tree = None
        index = 0
        
        if filename is None or not os.path.exists(filename):
            return None
        
        if erease:
            with open(filename, 'w') as file:
                file.write("")
        
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
    
        
    def _createNode(self, parent, letter):
        return AnyNode(id=None, label=letter, end=False, parent=parent)
    
    def _createEmptytree(self):
        root = AnyNode(id="root")      
        return root
        
    def toFile(self, filename):
        exporter = JsonExporter(indent=0, sort_keys=False)
        with open(filename, 'w') as file:
            file.write(str(self._index))
            file.write("\n")
            file.write(exporter.export(self._tree))
    
    def toString(self):
        return RenderTree(self._tree)
    
    def _getNodeId(self):
        val = self._index
        self._index+=1
        
        return val
        
    #-------------------------------------------------------
    #
    #-------------------------------------------------------
    def _getNode(self, node, letter):
        for elm in node.children:
            if elm.label == letter:
                return elm
        
        return None
    
    def _isEmpty(self):
        return len(self._tree.children)==0
    
    def _isRootNode(self, node):
        return node==self._tree
    
    def addWord(self, word_str):
        if word_str is None:
            return None
        
        node = self._tree
        for letter in word_str:
            
            child = self._getNode(node, letter)
            if child is None:
                child = self._createNode(node, letter)
            node = child
        
        if node == self._tree:
            return None
        
        if not node.end :
            node.end = True
            node.id = self._getNodeId()
    
    def isIn(self, word):
        return self.getId(word) is not None
    
    def getId(self, word_str):
        
        if word_str is None:
            return None
        
        node = self._tree
        
        for letter in word_str:
            child = self._getNode(node, letter)
            if child is None:
                return None
            node = child
        
        if node.end:
            return node.id
        else:
            return None
    
    def _getWordPath(self, leaf_node):
        word = ""
        node = leaf_node
        
        while node!=self._tree:
            word = node.label + word
            node = node.parent
        
        return word
    
    def size(self):
        return self._index
    #%%
    
    def iterator(self):
        return self._Iterator(self)
    
    class _Iterator():
        def __init__(self, Tree):
            self._obj = Tree
            self._iterator = PreOrderIter(self._obj._tree, filter_=lambda node: node.is_leaf)
            
            if self._obj._isEmpty():
                self._hasNext = False
            else :
                self._next_word = self._getNext()
                if self._next_word is None:
                    self._hasNext = False
                else:
                    self._hasNext = True
        
        def hasNext(self):
            return self._hasNext
        
        def _getNext(self):
            
            try:
                node = next(self._iterator)
                return self._obj._getWordPath(node)
                
            except StopIteration:
                self._hasNext = False
            
            return None
        
        def getNext(self):
            
            tmp = self._next_word
            self._next_word = self._getNext()
            return tmp
            

#%%

class WordsBag:
    def __init__(self, filename, erease=False, Language=Language()):
        if filename is  None :
            logging.warning("Fichier de sauvegarde du dictionnaire invalide")
            sys.exit()
        
        self._filename = filename
        logging.info("loading dictionnary")
        self._dico = AlphabeticTree(filename, erease)
        logging.info("dictionnary loaded")
        self._Language = Language
    
    def populateFromTxt(self, txt):
        clean_txt = self._Language.broom(txt)

        for word in clean_txt:
            self._dico.addWord(word)
    
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
    
    def initialize(self, database_obj, count_item=100):
        logging.info("initialize dictionnary from database...")
        it = database_obj.iterator()
        
        cpt=1
        
        while it.hasNext():
            movie = it.getNext()
            self.populateFromTxt(movie.summary)
            
            if cpt%count_item==0:
                logging.info("{0} items has been browse since the begining ({1})".format(cpt, datetime.datetime.now()))
                
            cpt+=1
        
        logging.info("dictionnary has been initialized from database")
    
    def getIds(self, txt):
        clean_txt = self._Language.broom(txt)
        output = []
        
        for word in clean_txt:
            id_word = self.getId(word)
            if id_word is not None:
                output.append((word, id_word))
        
        return output
    
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
