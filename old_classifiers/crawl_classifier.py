from bs4 import BeautifulSoup
from xml.sax.saxutils import escape
import elementtree.ElementTree as ET
import requests

writeKey = '****'
readKey = '****'

# def create_classifier(classifier, class_id):
# 	writeCalls = ET.SubElement(root, 'writeCalls', writeApiKey=writeKey, classifierName=classifier)
# 	create = ET.SubElement(writeCalls, 'create', id=class_id)
# 	return root

# def create_class(classifier, class_id, className):
# 	writeCalls = ET.SubElement(root, 'writeCalls', writeApiKey=writeKey, classifierName=classifier)	
# 	addClass = ET.SubElement(writeCalls, 'addClass', id=class_id, className=className)
# 	return root

def train(text, className, new=0):
	print "Safely made it to the train() method!"
	root = ET.Element('uclassify', xmlns='http://api.uclassify.com/1/RequestSchema', version='1.01')	
	texts = ET.SubElement(root, 'texts')
	textBase64 = ET.SubElement(texts, 'textBase64', id='text1')
	textBase64.text = escape(text)
	writeCalls = ET.SubElement(root, 'writeCalls', writeApiKey=writeKey, classifierName='subjects')	
	if new == 1:
		addClass = ET.SubElement(writeCalls, 'addClass', id='add1', className=className)
	train = ET.SubElement(writeCalls, 'train', id='train1', className=className, textId='text1')
	print ET.tostring(root, encoding='UTF-8')
	return root

def read(text):
	print "Safely made it into the read() method!"
	root = ET.Element('uclassify', xmlns='http://api.uclassify.com/1/RequestSchema', version='1.01')
	texts = ET.SubElement(root, 'texts')
	textBase64 = ET.SubElement(texts, 'textBase64', id='text1')
	textBase64.text = escape(text)
	readCalls = ET.SubElement(root, 'readCalls', readApiKey=readKey)
	classify = ET.SubElement(readCalls, 'classify', id='classify1', classifierName='subjects', textId='text1')
	print ET.tostring(root, encoding='UTF-8')
	print "End of read() method."
	return root

def post(root):
	# print "Safely entered the post() method!"
	r = requests.post('http://api.uclassify.com', ET.tostring(root, encoding='UTF-8'), headers={'Content-Type': 'text/xml'})
	return r.content

def classify(text):
	print "Safely made it into the classifier module!"
	root = read(text)
	soup = BeautifulSoup(post(root))
	print soup
	results = soup.find_all('class') # find all probabilities in xml

	probs = [(result.get('classname'), float(result.get('p'))) for result in results] # make a list of tuples
	print probs
	top = max(probs, key=lambda x: x[1]) # get (subject, probability) tuple with highest probability

	if top[1] >= 0.7:
		post(train(text, top[0]))
		return top[0]
	else: # pick subject or add a new class
		print "Do any of these subjects match that of the app?"
		for i, (subject, probability) in enumerate(probs, 1):
			print "%d. Subject: %s; Probability of match: %f." % (i, subject, probability)
		
		try:
			input_choice = int(raw_input("Type the number you choose. If you want to create a new class, enter 0; '-1' if you don't know/want to exit."))
			if input_choice < -1:
				print "Not a valid choice."
			elif input_choice == -1:
				return ''
			elif input_choice == 0:
				return '' # create new class here
			else:
				try:
					post(train(text, probs[input_choice-1][0]))
					return probs[input_choice-1][0]
				except IndexError:
					print "Try another number."
		except ValueError:
			print "That is not a valid number. Try again."
		return ''

def choice(probs):
	pass

# def process():
# 	# pseudocode
# 	do:
# 		readCalls()
# 		if p < 0.7:
# 			pick a subject or add a new one
# 		else:
# 			return the subject

# 	if thing[1] >= 0.7:
# 		return thing[0]
# 	else:
# 		return ''
# 	train(thing[0])

# if "Couldn't find any classifier with the name" in q:
# if "Trying to classify a text before any classes have been added!" in q:

# # head = ET.tostring(head, encoding='UTF-8')
# # action = ET.tostring(action, encoding='UTF-8')

# from xml.sax.saxutils import escape
# import requests
# import elementtree.ElementTree as ET
# url = 'http://api.uclassify.com'
# root = ET.Element("uclassify", xmlns="http://api.uclassify.com/1/RequestSchema", version="1.01")
# head = ET.SubElement(root, "writeCalls", writeApiKey="****", classifierName="test2")
# action = ET.SubElement(head, "create", id="CreateTest2")
# headers = {'Content-Type': 'text/xml'}

# root = ET.tostring(root, encoding='UTF-8')
# r = requests.post(url, root, headers=headers)
# r.content
# '<?xml version="1.0" encoding="UTF-8" ?>\n<uclassify xmlns="http://api.uclassify.com/1/ResponseSchema" version="1.01">\n\t<status success="true" statusCode="2000"/>\n\t<writeCalls>\n\t\t<create id="CreateTest"/>\n\t</writeCalls>\n</uclassify>'