# -*- coding: utf-8 -*-
"""
Created on Sat May 14 13:17:50 2016

@author: dheepan.ramanan
"""

from ProtoScraper import ReviewDetails
from selenium import webdriver
import pandas as pd
import time

albums = open("urls3.txt").read().split(',')

#getReviews = [pd.DataFrame.from_dict([ReviewDetails(url, driver)]) for url in albums]
listOfDfs = []
driver = webdriver.Chrome('/Users/dheepan.ramanan/anaconda/chromedriver/chromedriver')
for url in albums:
	
	
	try:
		
		df = pd.DataFrame.from_dict([ReviewDetails(url,driver)])
		listOfDfs.append(df)
		print df[['artist','album']]

		
		
	except AttributeError:
		
		print "#########!!!Exception!!!########"
		time.sleep(25)
		try:
			newDriver = webdriver.Chrome('/Users/dheepan.ramanan/anaconda/chromedriver/chromedriver')
			df = pd.DataFrame.from_dict([ReviewDetails(url,newDriver)])
			listOfDfs.append(df)
			print df[['artist','album']]
			newDriver.quit()
			
		except AttributeError:
			pass
		
	except KeyboardInterrupt:
		with open("missinga.txt", "w+") as f: 
			f.write(url+",")
		condensedDfs = pd.concat(listOfDfs)
		condensedDfs.to_excel('breakpitchfork.xlsx')

			
	
condensedDfs = pd.concat(listOfDfs)
condensedDfs.to_excel('18000pitchfork.xlsx')
