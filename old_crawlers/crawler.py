#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import feedparser
import datetime
import os
import re
import requests
import classifier
from bs4 import BeautifulSoup
from apps.models import Apps

# from sys import argv
# script, d = argv

os.environ['DJANGO_SETTINGS_MODULE'] = "newproject.settings"

# def classify():

def update_all():
	for app in Apps.objects.all():
		link = app.link
		page_to_db(link, crawl_binary=1)

def search(start_link=''):
	to_crawl = Apps.objects.filter(crawl_binary=0).order_by('date_added')
	while to_crawl:
		app_to_crawl = to_crawl[0]
		print to_crawl
		link_to_crawl = app_to_crawl.link
		print link_to_crawl
		soup = get_soup(link_to_crawl)

		try:
			also_bought_apps = get_also_bought_apps(soup)
		
			for app in also_bought_apps:
				name = app.find('a', {'class': 'name'}).get_text().encode('utf8')
				link = app.find('a', {'class': 'name'}).get('href').encode('utf8')

				if not (Apps.objects.filter(name=name) or Apps.objects.filter(link=link)):
					add_update(link, 0)
				else:
					try:
						print "The app '%s' is already in the database!" % (Apps.objects.get(link=link)._get_name())
					except Apps.DoesNotExist:
						print "The app '%s' is already in the database!" % (Apps.objects.get(name=name)._get_name())

		except IndexError:
			print "There was an IndexError for the app '%s'." % app_to_crawl
			pass
		except:
			raise

		app_to_crawl.crawl_binary = 1
		app_to_crawl.save()

		print "The app '%s' was successfully crawled!" % app_to_crawl

		to_crawl = Apps.objects.filter(crawl_binary=0).order_by('date_added')
	print "There are no more pages to crawl!"

def add_update(link, val):
	# future: find downloads, age, comment
	soup = get_soup(link)

	name = get_name(soup)
	creator = get_creator(soup)
	platform = get_platform(soup)
	subject = get_subject(soup)
	if subject == 'NotEducation': # change to "creator == 'NotEducation', set in classifier"
		print "The app '%s' is not Education-related and was not added to the database!" % name
	else:
		price = get_price(soup)
		rating = get_rating(soup)
		artwork = get_artwork(soup)

		if val == 0:
			m1 = Apps(name=name, platform=platform, 
				creator=creator, subject=subject, 
				price=price, rating=rating,
				artwork=artwork, link=link,
				date_added=datetime.datetime.now())
			m1.save()
			print "The app '%s' was successfully added to the database!" % name
		elif val == 1:
			m1 = Apps.objects.get(link=link)
			m1.update(name=name, platform=platform, 
				creator=creator, subject=subject, 
				price=price, rating=rating,
				artwork=artwork, link=link)
			print "The app '%s' was successfully updated!" % name
		else:
			print "What the hell are you doing with your code!?"

def update_all():
	for app in Apps.objects.all():
		add_update(app.link, val=1)
	print "There are no more objects to update!"

def get_soup(link):
	request = requests.get(link)
	return BeautifulSoup(request.text)

def get_also_bought_apps(soup):
	return soup.find_all('div', {'class': 'content', 'num-items': re.compile('[0-9]+')})[1].find_all('div', {'class': 'lockup small application'})

def get_name(soup):
	# get_name
	try:
		a = re.compile('<title>.+</title>').findall(str(soup))
		title = a[0]
		begin, end = title.index('>')+1, title.index('<',1)
		full_name = title[begin:end]
		if 'App Store - ' in full_name:
			return full_name[full_name.index('Store - ')+8:]
		elif ' for iP' in full_name:
			return full_name[:full_name.index(' for iP')]
		else:
			return full_name
	except (AttributeError, ValueError, TypeError):
		print "Error retrieving name from %s." % link
		return link

def get_creator(soup):
	# get_creator
	try:
		a = soup.find('div', {'class':'lockup product application'})
		b = a.find('li', {'class':'copyright'}).previous_sibling.get_text()
		return b[8:]
	except (AttributeError, ValueError, TypeError):
		print "Error retrieving creator for %s." % name
		return ''

def get_platform(soup):		
	# get_platform
	try:
		platform = list(soup.find_all('a', {'metrics-loc' : 'Pill_'})) # list
		for key, value in enumerate(platform):
			platform[key] = re.compile('>[^<]*<').findall(str(value))[0].lstrip('>').rstrip('<')
		return '/'.join(platform[:])
	except (AttributeError, ValueError, TypeError):
		print "Error retrieving platform for %s." % name
		return ''

def get_subject(soup):
	# get_subject
	try:
		a = soup.find('div', {'class':'lockup product application'})
		subject = a.find('span', {'class':'label'}).next_sibling.get_text()
		if subject == ('Education' or 'Reference'):
			subject = classifier.classify(get_description(soup))
			print "This app was classified as '%s'!" % subject
			return subject
		else:
			return "NotEducation"
	except (AttributeError, ValueError, TypeError):
		print "Error retrieving subject for %s." % name
		return ''

def get_price(soup):
	# get_price
	try:
		price_text = soup.find('div', {'class':'price'}).get_text()
		try:
			return float(price_text[1:]) # get rid of $ in front
		except ValueError:
			if price_text == ("Free" or "free"):
				return float(0)
			else:
				print "Error retrieving float-type price for %s." % name
				return None
	except (AttributeError, TypeError):
		print "Error retrieving price for %s." % name
		return None
		
def get_rating(soup):		
	# get_rating
	try:
		rating_text = soup.find('div', {'class': 'rating'}).get('aria-label')
		rating_num = re.compile('[0-5]\.?[0-9]*').findall(rating_text)
		return float(rating_num[0])
	except AttributeError:
		try:
			rating_text = soup.find('div', {'class': 'app-rating'}).a.get_text()
			rating_num = re.compile('[0-5]\.?[0-9]*').findall(rating_text)
			return float(rating_num[0])
		except (AttributeError, IndexError, TypeError, ValueError):
			return None
	except (IndexError, ValueError, TypeError):
		print "Error retrieving rating for %s." % name
		return None
	
def get_artwork(soup):
	# get_artwork
	try:
		return soup.find('div', {'class': 'lockup product application'}).find('img', {'class': 'artwork'}).get('src')
	except (AttributeError, ValueError, TypeError):
		print "Error retrieving artwork for %s." % name
		return ''

def get_description(soup):
	comment = soup.find('div', {'class': 'product-review'}).find('p').get_text()
	# strip unicode characters and do some additional formatting
	return comment

def main():
	print """
	1) Crawl
	2) Add apps to the database
	3) Update apps in the database
	4) Exit"""
	a = raw_input("Enter a number: ")
	while a != "4":
		if a == "1":
			pass
		elif a == "2":
			pass
		elif a == "3":
			pass
		else:
			print "Not a valid choice"
		a = raw_input("Enter a number: ")

def crawl_menu():
	print "Would you like to crawl from a link"

def db_menu():
	pass

# def prettify(dictionary):
# 	for entry in dictionary:
# 		print entry
# 		for key in ['platform','creator','subject','price','rating','artwork','link']:
# 			print "\t%s: %s" % (key, dictionary[entry][key])