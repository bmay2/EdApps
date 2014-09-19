"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from apps.models import Apps
from crawler import add_update


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class ScrapeTestCase(TestCase):
	
	def test_app_scrape(self):
		link = 'http://itunes.apple.com/us/app/mathwise/id455686352?mt=8'
		val = 0
		add_update(link, val)
		test = Apps.objects.get(link=link)

		self.assertEqual(test.name, 'MathWise')
		self.assertEqual(test.creator, 'Touch Adventures LLC')
		self.assertEqual(test.price, 0.0)
		self.assertEqual(test.rating, 3.0)
		self.assertEqual(test.artwork, 'http://a2.mzstatic.com/us/r1000/063/Purple/16/10/b0/mzm.sjyrfqta.175x175-75.jpg')
		self.assertEqual(test.link, link)
