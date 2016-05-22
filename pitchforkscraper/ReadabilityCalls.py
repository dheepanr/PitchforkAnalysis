# -*- coding: utf-8 -*-
"""
Created on Fri May 20 17:50:47 2016

@author: dheepan.ramanan
"""

import requests as rq
import json 

headers={
    "X-Mashape-Key": "MD9aq7OnCsmsha5IDtO2dbJ1G64Ep1rfQ5TjsnroFgVE00nVFO",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"}
url = "https://ipeirotis-readability-metrics.p.mashape.com/getReadabilityMetrics"

data = []
for review in pfdata.fullReview.values:
    payload = {"text":review[:3000].encode("ascii","ignore")}
    response = rq.post(url,headers=headers, params=payload)
    data.append(response.text)