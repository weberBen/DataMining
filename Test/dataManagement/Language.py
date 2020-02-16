#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import unicodedata
from num2words import num2words
from nltk.corpus import stopwords
import re
from nltk.tokenize import TweetTokenizer


class Language:
    def __init__(self):
        self._stemmer = SnowballStemmer("english")
        self._stop_words = set(stopwords.words('english'))
        self.sentenceSeparator = "."
        self._tokenize = TweetTokenizer()
        
    def _removeAccent(self, text):
        #https://stackoverflow.com/questions/44431730/how-to-replace-accented-characters-in-python?rq=1
        try:
            text = unicode(text, 'utf-8')
        except NameError: # unicode is a default on python 3 
            pass
    
            text = unicodedata.normalize('NFD', text)\
               .encode('ascii', 'ignore')\
               .decode("utf-8")
    
        return str(text)
    
    def _numberToTextFunction(self, num):
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
        
        tmp = self._numberToTextFunction(word)
        if tmp is not None:
            word = tmp
        
        tmp = self._removeAccent(word)
        if word is not None:
            word = tmp
        
        word = self._stemmer.stem(word)
        
        return word
    
    def broom(self, txt):
        txt = txt.replace(self.sentenceSeparator, " ")
        token_txt = self._tokenize.tokenize(txt)
        
        clean_words = []
        for word in token_txt:
            word = self.normalize(word)
            if word is not None:
                clean_words.append(word)
        
        return clean_words
#%%