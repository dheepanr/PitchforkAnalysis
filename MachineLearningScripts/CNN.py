# -*- coding: utf-8 -*-
"""
Created on Thu May 26 14:04:57 2016

@author: dheepan.ramanan
"""

import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.preprocessing import sequence
from keras.layers.core import Dense, Dropout, Activation, Lambda
from keras.layers.embeddings import Embedding
from keras.layers.convolutional import Convolution1D
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras import backend as K
from nltk.tokenize import sent_tokenize
from sklearn.metrics import f1_score
import pandas as pd


max_features = 1000
maxlen = 400
batch_size = 32
embedding_dims = 50
nb_filter = 250
filter_length = 3
hidden_dims = 250
nb_epoch = 30

TrainData = pd.read_excel('/Users/dheepan.ramanan/Documents/PitchforkAnalysis/dataset/trainingData/upsampled3.xlsx').sample(frac=1)
encode = {"Best new music":1, "Not Best New Music":0}

BNM = TrainData.BestNewMusic.to_dict()
paragraphs = TrainData.fullReview.to_dict()

#this is to reduce reviews to sentences + label (very slow training)
def sentencePP(sentences,lookup):
	splitSents = []	
	ylabels =[]
	for key, val in sentences.items():	
		sents = sent_tokenize(val)
		ylabel = encode[lookup[key]]
		for x in range(len(sents)):
			ylabels.append(ylabel)
		splitSents.append(sents)
			
	splitSents = reduce(lambda x,y: x+y, splitSents)
	return splitSents,ylabels

xTrain = [x.encode("ascii","replace") for x in paragraphs.values()]
yTrain = [encode[val] for val in BNM.values()]

tk = Tokenizer(nb_words=max_features)
tk.fit_on_texts(xTrain)
xTrainSeq = sequence.pad_sequences(tk.texts_to_sequences(xTrain), maxlen=maxlen)


model = Sequential()
model.add(Embedding(max_features,
                    embedding_dims,
                    input_length=maxlen, dropout=.2))
																			
model.add(Convolution1D(nb_filter=nb_filter,
                        filter_length=filter_length,
                        border_mode='valid',
                        activation='relu',
                        subsample_length=1))

		
def max_1d(X):
    return K.max(X, axis=1)

model.add(Lambda(max_1d, output_shape=(nb_filter,)))

model.add(Dense(hidden_dims))
model.add(Dropout(0.2))
model.add(Activation('relu'))

model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',  metrics=["accuracy"],class_mode='binary')
              
														
model.fit(xTrainSeq, yTrain,
          batch_size=batch_size,
          nb_epoch=nb_epoch)       


TestData = pd.read_excel('/Users/dheepan.ramanan/Documents/PitchforkAnalysis/dataset/trainingData/upsampletest.xlsx')
xTest = TestData.fullReview.to_dict()
xTest = [x.encode("ascii","replace") for x in xTest.values()]
xTestSeq = sequence.pad_sequences(tk.texts_to_sequences(xTest), maxlen=maxlen)

yTest = TestData["BestNewMusic"].to_dict()
yTest = [encode[val] for val in yTest.values()]


f1_score(model.predict_classes(xTestSeq),yTest)