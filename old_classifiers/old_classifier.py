from uclassify import uClassify
import requests

a = uclassify()
a.setWriteApiKey('****')
a.setReadApiKey('****')

a.create("AppSubject") #Creates Classifier named "ManorWoman"

a.addClass(["man","woman"],"AppSubject") #Adds two class named "man" and "woman" to the classifier "ManorWoman"

a.train(["Her hair is so nice!!","I wish I had more cosmetic.","I like those ice creams."],"woman","ManorWoman")
#The above function trains three sentences for the class "woman" on the classifier "ManorWoman"

d = a.classify(["sample text1","sample text2"],"ManorWoman")
#Now the list d will contain the following value [('sample text1', u'0', [(u'man', u'0.5'), (u'woman', u'0.5')]), ('sample text2', u'0', [(u'man', u'0.5'), (u'woman', u'0.5')])]