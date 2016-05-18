# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 15:52:12 2016

@author: dheepan.ramanan
"""

from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd
import time
import re


def Depth(depth):
	urls = ['http://pitchfork.com/reviews/albums/?page='+str(i) for i in range(depth)]
	return urls
	
def AlbumUrls(urls):
	driver = webdriver.PhantomJS('/Users/dheepan.ramanan/Documents/Resources/phantomjs-2.1.1-macosx/bin/phantomjs')
	musicUrls = []
	for ix, url in enumerate(urls):
		driver.get(url)
		pageText = bs(driver.page_source, 'html.parser')
		grabReviewRels = pageText.findAll('div', attrs={'class':'review'})
		reviewRels = [rel.find('a')['href'] for rel in grabReviewRels]
		with open("urls3.txt","a") as f:
			for a in reviewRels:
				f.write(a+',')
		with open("log.txt","w+") as log:
			log.write(str(ix)+"\n")
		musicUrls.append(reviewRels)
		print reviewRels
	driver.quit()

	return musicUrls


def ReviewDetails(url, driver):
	
	data = {}	
	reviewData = 'empty'
	driver.get('http://pitchfork.com'+url)
	if driver.title == '502 Bad Gateway':
		time.sleep(40)
		newDriver = webdriver.Chrome('/Users/dheepan.ramanan/anaconda/chromedriver/chromedriver')
		newDriver.get('http://pitchfork.com'+url)
		reviewData = bs(newDriver.page_source, 'html.parser')
		newDriver.quit()
		
	if driver.title == '503 Backend fetch failed':
		time.sleep(40)
		newDriver = webdriver.Chrome('/Users/dheepan.ramanan/anaconda/chromedriver/chromedriver')
		newDriver.get('http://pitchfork.com'+url)
		reviewData = bs(newDriver.page_source, 'html.parser')
		newDriver.quit()
		
	

	
	
	if reviewData == 'empty':	
		reviewPageParse = bs(driver.page_source, 'html.parser')
	else:
		reviewPageParse= reviewData
	
	artist = reviewPageParse.find('h2', attrs={'class':'artists'}).text
	album = reviewPageParse.find('h1', attrs={'class':'review-title'}).text
	
	if reviewPageParse.find('div',attrs={'class':'score-box bnm'}):
		reviewScore = float(reviewPageParse.find('div',attrs={'class':'score-box bnm'}).find('span', attrs={'class':'score'}).text)
		bestNewText = reviewPageParse.find('div',attrs={'class':'score-box bnm'}).find('p').text
	else:
		reviewScore = float(reviewPageParse.find('span', attrs={'class':'score'}).text)
		bestNewText = 'Not Best New Music'
		
	metaAuthor = re.sub('by: ','',reviewPageParse.find('a', attrs={'class', 'display-name'}).text)
	
	if reviewPageParse.find('ul',attrs={"class":"genre-list before" }).findAll('li'):
		genres = reviewPageParse.find('ul',attrs={'class':"genre-list before"}).findAll('li')
		primaryGenre = genres[0].text
	else:
		primaryGenre = ''
		
	dateTime = re.search(r'(\w{3}\s\w{3}\s\d{2}\s\d{4})',reviewPageParse.find('span', attrs={'class':'pub-date'})['title']).group(0)
	
	abstract = reviewPageParse.find('div',  attrs={'class':'abstract'}).text
	try:
		reviewText = reviewPageParse.find('div',attrs={'class':'contents dropcap'}).text
	except Exception:
		reviewText = reviewPageParse.find('div',  attrs={'class':'contents'}).text
	fullReview = abstract+'\n'+reviewText
	
	data['album'] = album
	data['artist'] = artist
	data['date'] = dateTime
	data['author'] = metaAuthor
	data['reviewScore'] = reviewScore
	data['BestNewMusic'] = bestNewText
	data['fullReview'] = fullReview
	data['genre'] = primaryGenre
	
	return data
	
		
	
	
def PitchforkScraper(length):
	urls = Depth(length)
	albums = AlbumUrls(urls)
	albums = reduce(lambda x, y: x+y, albums)
	driver = webdriver.PhantomJS('/Users/dheepan.ramanan/Documents/Resources/phantomjs-1.9.7-macosx/bin/phantomjs')
	#getReviews = [pd.DataFrame.from_dict([ReviewDetails(url, driver)]) for url in albums]
	listOfDfs = []
	for url in albums:
		
		
	
		df = pd.DataFrame.from_dict([ReviewDetails(url,driver)])
		listOfDfs.append(df)
		print df[['artist','album']] 
		
			
		
		
	condensedDfs = pd.concat(listOfDfs)
	condensedDfs.to_excel(str(length)+'pitchfork.xlsx')
	return condensedDfs
		

		
		
	
	
	
	
		
		

