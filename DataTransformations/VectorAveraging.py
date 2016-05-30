# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:34:45 2016

@author: dheepan.ramanan
"""
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer as tbwToken
from nltk.stem.porter import PorterStemmer
from gensim.models import Word2Vec
from IPython.core import display
import string
import numpy as np
import pandas as pd
from scipy import pearsonr

def lambda_vectoraverage(review,model,num_features):
    featureVec = np.zeros((num_features,),dtype="float32")
    nwords = 0.
    modelindex = set(model.index2word)
    #this is the list of words in our word2vec trained model
    sentences = tokenize(review)
    for word in sentences:
        if word not in stopwords.words('english'):
            if word in modelindex:
                nwords = nwords + 1.
                featureVec = np.add(featureVec,model[word])
    featureVec = np.divide(featureVec,nwords)
    return featureVec

def lambda_corr(vector,corr,df):
	correlations = []	
	for index,row in df.iterrows():
		correlation = corr(vector, row.vectorAverage)
		artist = row.artist
		album = row.album
		correlations.append([correlation[0],artist,album])
	return correlations