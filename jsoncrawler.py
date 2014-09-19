from apps.models import Apps
from bs4 import BeautifulSoup
import requests
import re
# import datetime

try:
    import simplejson
except ImportError:
    import json as simplejson

acceptable_topics = ['Books', 'Reference', 'Education', 'Business', 'Productivity', 'Medical'] # 'Utilities'?

def get_json(topic):
	r = requests.get('http://itunes.apple.com/search?term='+topic+'&entity=software&limit=300')
	j = simplejson.loads(r.content)
	for i in j['results']:
		if not Apps.objects.filter(name=get_name(i)):
			if (i['primaryGenreName'] in ['Education', 'Reference']) or (('Education' in i['genres']) and (i['primaryGenreName'] in acceptable_topics)):
				try:
					m1 = Apps(name=get_name(i), description=get_description(i),
							creator=get_creator(i), subject=i['primaryGenreName'],
							price=get_price(i), rating=get_rating(i),
							artwork=get_artwork(i), link=get_link(i))
							# date_added=datetime.datetime.now()) <-- check if needed
					m1.save()
					print get_name(i) + " was added to the database! ", topic
				except:
					print get_name(i), get_link(i)
					raise
			else:
				print get_name(i) + " is not an Education app! " + str(i['genres'])
		
def classification(text):
	return classifier.classify(text)

# for model objects that allow nulls
def catch_key_errors_null(fn):
	def decorator(*args):
		try:
			return fn(*args)
		except KeyError:
			return None
	return decorator

# for model objects that do not allow nulls
def catch_key_errors_not_null(fn):
	def decorator(*args):
		try:
			return fn(*args)
		except KeyError:
			return ''
	return decorator

@catch_key_errors_not_null
def get_name(i):
	return i['trackName']

@catch_key_errors_not_null
def get_creator(i):
	return i['sellerName']

@catch_key_errors_null
def get_price(i):
	return i['price']

@catch_key_errors_null
def get_rating(i):
	return i['averageUserRating']

@catch_key_errors_null
def get_rating_count(i):
	return i['userRatingCount']

@catch_key_errors_not_null
def get_artwork(i):
	try:
		return i['artworkUrl100']
	except KeyError:
		return i['artworkUrl60']

@catch_key_errors_not_null
def get_link(i):
	try:
		return i['trackViewUrl']
	except:
		raise

@catch_key_errors_not_null
def get_description(i):
	return i['description']

def scrape_wikiversity():
	wiki_page = requests.get('http://en.wikiversity.org/wiki/Topic:Topics')
	soup = BeautifulSoup(wiki_page.text)
	links = soup.find_all('a', {'title': re.compile('Topic:')})
	titles = [link.get('title') for link in links]
	topics = [title[6:] for title in titles]
	return topics

def clean_topics(e):
	for topic in e:
		topic.replace('& ', '')
	return e

def main():
	topics = scrape_wikiversity()
	cleaned_topics = clean_topics(topics)
	for topic in cleaned_topics:
		get_json(topic)
	print "We're done!"

main()