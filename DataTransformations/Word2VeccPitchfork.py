# -*- coding: utf-8 -*-
"""
Created on Mon May 23 15:34:48 2016

@author: dheepan.ramanan
"""

from nltk.tokenize import sent_tokenize
from nltk.tokenize import TreebankWordTokenizer as tbwToken
from gensim.models import Word2Vec
import string
import pandas as pd


reviews = pd.read_csv('/Users/dheepan.ramanan/Documents/PitchforkAnalysis/dataset/word2vecreviews.csv',sep="~",header=None,index_col=0)

def tokenize(text):
    tbw= tbwToken()
    sentences = text.replace("``","").replace("'","")
    sentences = sent_tokenize(text.encode("ascii","replace"))
    tokens = [tbw.tokenize(s.lower()) for s in sentences]
    tokens = reduce(lambda x,y: x+y,[stripPunc(t) for t in tokens])
    return tokens

def stripPunc(sent):
	tokens = []	
	for t in sent:
		if t not in string.punctuation:
			tokens.append(t)
	return tokens
	
sentences = [tokenize(s) for s in reviews[1]]
reducedFat = reduce(lambda x,y: x+y, sentences)

# Set values for various parameters

num_features = 300    # Word vector dimensionality                      
min_word_count = 10   # Minimum word count                        
num_workers = 4       # Number of threads to run in parallel
context = 10          # Context window size                                                                                    
downsampling = 1e-3   # Downsample setting for frequent words

print "Training model..."
model = Word2Vec(reducedFat, workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sample = downsampling)
											

model_name = "300features_10minwords_102context"
model.save(model_name)