# -*- coding: utf-8 -*-
"""
Created on Mon May 23 11:46:06 2016

@author: dheepan.ramanan
"""

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import TreebankWordTokenizer as tbwToken
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim.models import Word2Vec
import string
import pandas as pd

stemmer = PorterStemmer()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tbw= tbwToken()
    sentences = sent_tokenize(text)
    tokens = reduce(lambda x,y : x+y, [tbw.tokenize(s) for s in sentences])
    tokens = [i.encode("ascii","ignore") for i in tokens if i not in string.punctuation]
    stems = stem_tokens(tokens, stemmer)
    return stems

pfdata = pd.read_excel('FinalPFDataset.xlsx')
BNM = pfdata.date.dt.year > 2002
pfdataBNM = pfdata[BNM == True]
reviews = pfdata.fullReview
vect = CountVectorizer(tokenizer=tokenize, stop_words=stopwords.words('english'),min_df=2,max_features=5000)


