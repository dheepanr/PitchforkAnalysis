# -*- coding: utf-8 -*-
"""
Created on Fri May 27 12:17:40 2016

@author: dheepan.ramanan
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.preprocessing import StandardScaler
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer as tbwToken
from nltk.stem.porter import PorterStemmer
from gensim.models import Word2Vec
from IPython.core import display
from sklearn.metrics import f1_score
import string
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.svm import SVC

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

encode = {"Best new music":1, "Not Best New Music":0}

pfdata = pd.read_excel('/Users/dheepan.ramanan/Documents/PitchforkAnalysis/dataset/trainingData/upsampled2.xlsx')
reviews = pfdata.fullReview
vect = CountVectorizer(tokenizer=tokenize, stop_words=stopwords.words('english'),min_df=5,max_features=1000,ngram_range=(1,2))
transformer = TfidfTransformer( smooth_idf=True, sublinear_tf=False, use_idf=True)


xdata = pfdata.drop(["artist","fullReview","date","album","author","genre","reviewScore"],axis=1).drop("level_0","index").sample(frac=1)
vecBow = vect.fit_transform(reviews)
vecBowT = transformer.fit_transform(vecBow)

BoW = pd.DataFrame(vecBow.todense(),columns=[vect.get_feature_names()])
xtrain = xdata.join(BoW,rsuffix="_bow").dropna()
ytrain = xtrain["BestNewMusic"].apply(lambda x: encode[x])
xtrain = pd.DataFrame(StandardScaler().fit_transform(xtrain.drop("BestNewMusic",axis=1)),columns=xtrain.columns[1:])

modelStats= {}
classifiers = [LogisticRegression(penalty="l1"), LinearSVC(penalty="l1",dual=False)]
for c in classifiers:
	c.fit(xtrain,ytrain)
	score = cross_val_score(c, xtrain.values, ytrain, cv=2, scoring="f1",n_jobs=1)
	modelStats[c] = score