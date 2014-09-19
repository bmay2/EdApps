from bs4 import BeautifulSoup
from apps.models import Apps
from xml.sax.saxutils import escape
import elementtree.ElementTree as ET
import requests
import base64

writeKey = '****'
readKey = '****'

# def create_classifier(classifier, class_id):
# 	writeCalls = ET.SubElement(root, 'writeCalls', writeApiKey=writeKey, classifierName=classifier)
# 	create = ET.SubElement(writeCalls, 'create', id=class_id)
# 	return root

def getInfo():
	root = ET.Element('uclassify', xmlns='http://api.uclassify.com/1/RequestSchema', version='1.01')
	readCalls = ET.SubElement(root, 'readCalls', readApiKey=readKey)
	getInformation = ET.SubElement(readCalls, 'getInformation', id='GetInformation', classifierName='subjects')
	return root

def train(text, className, new=0):
	root = ET.Element('uclassify', xmlns='http://api.uclassify.com/1/RequestSchema', version='1.01')	
	texts = ET.SubElement(root, 'texts')
	textBase64 = ET.SubElement(texts, 'textBase64', id='text1')
	textBase64.text = base64.b64encode(text.encode('UTF-8'))
	writeCalls = ET.SubElement(root, 'writeCalls', writeApiKey=writeKey, classifierName='subjects')	
	if new == 1:
		addClass = ET.SubElement(writeCalls, 'addClass', id='add1', className=className)
	train = ET.SubElement(writeCalls, 'train', id='train1', className=className, textId='text1')
	return root

def read(text):
	root = ET.Element('uclassify', xmlns='http://api.uclassify.com/1/RequestSchema', version='1.01')
	texts = ET.SubElement(root, 'texts')
	textBase64 = ET.SubElement(texts, 'textBase64', id='text1')
	textBase64.text = base64.b64encode(text.encode('UTF-8'))
	readCalls = ET.SubElement(root, 'readCalls', readApiKey=readKey)
	classify = ET.SubElement(readCalls, 'classify', id='classify1', classifierName='subjects', textId='text1')
	return root

def post(root):
	r = requests.post('http://api.uclassify.com', ET.tostring(root, encoding='UTF-8'), headers={'Content-Type': 'text/xml'})
	return r.content

def classify_subject(text):
	root = read(text)
	soup = BeautifulSoup(post(root))
	results = soup.find_all('class') # find all probabilities in xml

	probs = [(result.get('classname'), float(result.get('p'))) for result in results] # make a list of tuples (subject, probability)
	top = max(probs, key=lambda x: x[1]) # get (subject, probability) tuple with highest probability

	# if top[1] >= 0.7:
	# 	post(train(text, top[0]))
	# 	return top[0]
	if True: # pick subject or add a new class
		print "Do any of these subjects match that of the app?"
		for i, (subject, probability) in enumerate(probs, 1):
			print "%d. Subject: %s; Probability of match: %f." % (i, subject, probability)
		
		try:
			input_choice = int(raw_input("Type the number you choose. If you want to create a new class, enter 0; '-1' if you don't know/want to exit: "))
			if input_choice < -1:
				print "Not a valid choice."
			elif input_choice == -1:
				return ''
			elif input_choice == 0:
				input_subject = raw_input("Type the name of the subject this app falls under: ")
				post(train(text, input_subject, new=1)) # create new className
				return input_subject # create new class here
			else:
				try:
					post(train(text, probs[input_choice-1][0])) # train from list of possible subjects
					print probs[input_choice-1][0]
					return probs[input_choice-1][0]
				except IndexError:
					print "Try another number."
		except ValueError:
			print "That is not a valid number. Try again."
		return ''

def choice(probs):
	pass

def main():
	generic_subjects = ['Books', 'Reference', 'Education', 'Business', 'Productivity', 'Medical', '']
	a = Apps.objects.filter(subject__in=generic_subjects)
	for app in a:
		if app.description:
			m1 = Apps.objects.filter(link=app.link)
			print app.name
			print app.description
			subject = classify_subject(app.description)
			m1.update(subject=subject)
			print "The app '%s' was successfully classified as '%s'!" % (app.name, subject)

#main()

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