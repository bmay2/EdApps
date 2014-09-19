#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import feedparser
import datetime
import os
import re
import requests
from bs4 import BeautifulSoup
from apps.models import Apps

# from sys import argv
# script, d = argv

os.environ['DJANGO_SETTINGS_MODULE'] = "newproject.settings"

def breadth_first_search(start_link=''):
	to_crawl = Apps.objects.filter(crawl_binary=0).order_by('date_added')
	while to_crawl:
		app_to_crawl = to_crawl[0]
		print to_crawl
		link_to_crawl = app_to_crawl.link
		print link_to_crawl
		foobar = requests.get(link_to_crawl).text
		soup = BeautifulSoup(foobar)

		try:
			also_bought_apps = soup.find_all('div', {'class': 'content', 'num-items': re.compile('[0-9]+')})[1].find_all('div', {'class': 'lockup small application'})
		
			for app in also_bought_apps:
				name = app.find('a', {'class': 'name'}).get_text().encode('utf8')
				link = app.find('a', {'class': 'name'}).get('href').encode('utf8')

				if not (Apps.objects.filter(name=name) or Apps.objects.filter(link=link)):
					page_to_db(link)
				else:
					print "The app '%s' is already in the database!" % (Apps.objects.get(link=link)._get_name())
		except IndexError:
			print "There was an IndexError for the app '%s'." % app_to_crawl
			pass
		except:
			raise

		app_to_crawl.crawl_binary = 1
		app_to_crawl.save()

		print "The app '%s' was successfully crawled!" % a

		to_crawl = Apps.objects.filter(crawl_binary=0).order_by('date_added')
	print "There are no more pages to crawl!"
	
def page_to_db(link):
	# downloads, age, comment
	
	foobar = requests.get(link).text
	soup = BeautifulSoup(foobar)

	# get_name
	try:
		a = re.compile('<title>.+</title>').findall(str(soup))
		title = a[0]
		begin, end = title.index('>')+1, title.index('<',1)
		full_name = title[begin:end]
		if 'App Store - ' in full_name:
			name = full_name[full_name.index('Store - ')+8:]
		elif ' for iP' in full_name:
			name = full_name[:full_name.index(' for iP')]
		else:
			name = full_name
	except (AttributeError, ValueError, TypeError):
		name = link
		print "Error retrieving name from %s." % link

	# get_creator
	try:
		a = soup.find('div', {'class':'lockup product application'})
		b = str(a.find('li', {'class':'copyright'}).previous_sibling.get_text())
		creator = b[8:]
	except (AttributeError, ValueError, TypeError):
		creator = ''
		print "Error retrieving creator for %s." % name
		
	# get_platform
	try:
		platform = list(soup.find_all('a', {'metrics-loc' : 'Pill_'})) # list
		for key, value in enumerate(platform):
			platform[key] = re.compile('>[^<]*<').findall(str(value))[0].lstrip('>').rstrip('<')
		platform = '/'.join(platform[:])
	except (AttributeError, ValueError, TypeError):
		platform = ''
		print "Error retrieving platform for %s." % name
	
	# get_subject
	try:
		a = soup.find('div', {'class':'lockup product application'})
		subject = str(a.find('span', {'class':'label'}).next_sibling.get_text())
	except (AttributeError, ValueError, TypeError):
		subject = ''
		print "Error retrieving subject for %s." % name
		
	# get_price
	try:
		price_text = soup.find('div', {'class':'price'}).get_text()
		try:
			price = float(price_text[1:]) # get rid of $ in front
		except ValueError:
			if price_text == ("Free" or "free"):
				price = float(0)
			else:
				price = None
				print "Error retrieving float-type price for %s." % name
	except (AttributeError, TypeError):
		price = None
		print "Error retrieving price for %s." % name
		
	# get_rating
	try:
		rating_text = soup.find('div', {'class': 'rating'}).get('aria-label')
		rating_num = re.compile('[0-5]\.?[0-9]*').findall(rating_text)
		rating = float(rating_num[0])
	except AttributeError:
		try:
			rating_text = soup.find('div', {'class': 'app-rating'}).a.get_text()
			rating_num = re.compile('[0-5]\.?[0-9]*').findall(rating_text)
			rating = float(rating_num[0])
		except (AttributeError, IndexError, TypeError, ValueError):
			rating = None
	except (IndexError, ValueError, TypeError):
		rating = None
		print "Error retrieving rating for %s." % name
	
	# get_artwork
	try:
		artwork = str(soup.find('img', {'class': 'artwork'}).get('src'))
	except (AttributeError, ValueError, TypeError):
		artwork = ''
		print "Error retrieving artwork for %s." % name

	m1 = Apps(name=name, platform=platform, 
		creator=creator, subject=subject, 
		price=price, rating=rating,
		artwork=artwork, link=link,
		crawl_binary=0, date_added=datetime.datetime.now())
	m1.save()

	print "The app '%s' was successfully added to the database!" % name
	
if __name__ == '__main__':
	breadth_first_search()

# def prettify(dictionary):
# 	for entry in dictionary:
# 		print entry
# 		for key in ['platform','creator','subject','price','rating','artwork','link']:
# 			print "\t%s: %s" % (key, dictionary[entry][key])