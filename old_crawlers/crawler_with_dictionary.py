#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import feedparser
import os
import re
import requests
from bs4 import BeautifulSoup
from apps.models import Apps

# from sys import argv
# script, d = argv

os.environ['DJANGO_SETTINGS_MODULE'] = "newproject.settings"

def gather_applinks(rss_feed):
	d = feedparser.parse(rss_feed)
	e = []
	
	for i in xrange(0,len(d.entries)):
		link = d.entries[i].link
		e.append(link)
	return e
	
def scrape_app_page(app_links, dictionary):
	# downloads, age, comment
	# also_bought
	
	for link in app_links:
		if not Apps.objects.filter(link=link):
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
				elif 'for iP' in full_name:
					name = full_name[:full_name.index('for iP')]
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
			
			dictionary[name] = {}
			dictionary[name]['platform'] = platform
			dictionary[name]['creator'] = creator
			dictionary[name]['subject'] = subject
			dictionary[name]['price'] = price
			dictionary[name]['rating'] = rating
			dictionary[name]['artwork'] = artwork
			dictionary[name]['link'] = link
			
	return dictionary
	
def main(dictionary):
	link = "http://itunes.apple.com/us/rss/topgrossingapplications/limit=25/genre=6017/xml" # % int(limit)
	app_links = gather_applinks(link)
	dictionary = scrape_app_page(app_links, dictionary)
	
def prettify(dictionary):
	for entry in dictionary:
		print entry
		for key in ['platform','creator','subject','price','rating','artwork','link']:
			print "\t%s: %s" % (key, dictionary[entry][key])

def duplicate_check(d):
	pass

def add_to_db(d):
	for entry in d:
		if not Apps.objects.filter(name=entry):
			m1 = Apps(name=entry, platform=d[entry]['platform'], 
				creator=d[entry]['creator'], subject=d[entry]['subject'], 
				price=d[entry]['price'], rating=d[entry]['rating'],
				artwork=d[entry]['artwork'], link=d[entry]['link'])
			m1.save()
		else:
			print "The app '%s' is already in the database!" % entry