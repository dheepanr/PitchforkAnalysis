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
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score


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

pfdata = pd.read_excel('../dataset/trainingData/pfdataTrain.xlsx')
reviews = pfdata.fullReview
vect = CountVectorizer(tokenizer=tokenize, stop_words=stopwords.words('english'),min_df=5,max_features=5000)

xdata = pfdata.drop(["artist","fullReview","date","album","author","genre","reviewScore","index"],axis=1).reset_index().drop("index",axis=1)
vecBow = vect.fit_transform(reviews)
BoW = pd.DataFrame(vecBow.todense(),columns=[vect.get_feature_names()])
xtrain = xdata.join(BoW,rsuffix="_bow").dropna()
ytrain = xtrain["BestNewMusic"]
xtrain = pd.DataFrame(StandardScaler().fit_transform(xtrain.drop("BestNewMusic",axis=1)),columns=xtrain.columns[1:])

modelStats= {}
classifiers = [LogisticRegression(penalty="l1"), LinearSVC(penalty="l1",dual=False),RandomForestClassifier()]
for c in classifiers:
	c.fit(xtrain,ytrain)
	score = cross_val_score(c, xtrain.values, ytrain, cv=5, scoring="f1_weighted")
	modelStats[c] = score

xtest = pd.read_excel('/Users/dheepan.ramanan/Documents/PitchforkAnalysis/dataset/trainingData/pfdataTest.xlsx').drop(["artist","date","album","author","genre","reviewScore"],axis=1).reset_index().drop("index",axis=1)
testBow = vect.transform(xtest.fullReview)
testBoW = pd.DataFrame(vecBow.todense(),columns=[vect.get_feature_names()])
xtestjoin = xtest.join(testBoW,rsuffix="_bow").dropna().drop("fullReview",axis=1)
ytest = xtest["BestNewMusic"]
xtestjoin = pd.DataFrame(StandardScaler().fit_transform(xtestjoin.drop("BestNewMusic",axis=1)),columns=xtestjoin.columns[1:])

fscoresTest = {}
for c in classifiers:
	c.fit(xtestjoin,ytest)
	ypred = c.predict(xtestjoin)
	fscore = f1_score(ytest,ypred,pos_label='Best new music')
	fscoresTest[c] = fscore
	