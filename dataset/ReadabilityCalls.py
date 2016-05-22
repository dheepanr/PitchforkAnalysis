# -*- coding: utf-8 -*-
"""
Created on Fri May 20 17:53:45 2016

@author: dheepan.ramanan
"""
import pandas as pd
import requests as rq
import json 

pfdata = pd.read_excel("dataset/pitchforkdataset.xlsx")
headers={
    "X-Mashape-Key": "MD9aq7OnCsmsha5IDtO2dbJ1G64Ep1rfQ5TjsnroFgVE00nVFO",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"}
url = "https://ipeirotis-readability-metrics.p.mashape.com/getReadabilityMetrics"

for review in pfdata.fullReview.values[7670:]:
    payload = {"text":review[:3000].encode("ascii","ignore")}
    response = rq.post(url,headers=headers, params=payload)    
    with open("readability.txt","a") as f:
					f.write(response.text+"~")
					
callresponses = open('/Users/dheepan.ramanan/Documents/PitchforkAnalysis/readability.txt').read().split("~")

callDicts= {}
for i in enumerate(callresponses):
	try:
		callDicts[i[0]] = json.loads(i[1])
	except ValueError:
		callDicts[i[0]] = {u'ARI': 0,
		 u'CHARACTERS': 0,
		 u'COLEMAN_LIAU': 0,
		 u'COMPLEXWORDS': 0,
		 u'FLESCH_KINCAID': 0,
		 u'FLESCH_READING': 0,
		 u'GUNNING_FOG': 0,
		 u'SENTENCES': 0,
		 u'SMOG': 0,
		 u'SMOG_INDEX': 0,
		 u'SYLLABLES': 0,
		 u'WORDS': 0,
		 u'etag': u'"to4mFGVXeFl3UYs8Sp68GrRZqEw/QTVqcaa2RbNAyR-d3amVlby6x78"',
		 u'kind': u'readability#resourcesItem'}
		