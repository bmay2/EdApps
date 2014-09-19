from django.db import models
from django.utils.timezone import utc
import datetime
import os

os.environ['DJANGO_SETTINGS_MODULE'] = "newproject.settings"

class Apps(models.Model):
	
	# AGES = (
	# 	('E', 'Elementary School'),
	# 	('M', 'Middle School'),
	# 	('H', 'High School'),
	# 	('C', 'College'),
	# 	('G', 'Graduate School'),
	# 	('O', 'Other'),
	# )

 	name = models.CharField(max_length=150)
	platform = models.CharField(max_length=30, blank=True)
	subject = models.CharField(max_length=30, blank=True)
 	creator = models.CharField(max_length=100, blank=True)
	price = models.FloatField(max_length=10, null=True, blank=True)
 	downloads = models.IntegerField(null=True, blank=True)
	rating = models.FloatField(max_length=10, null=True, blank=True)
	age = models.CharField(max_length=30, null=True, blank=True)
 	description = models.TextField(blank=True)
 	artwork = models.CharField(max_length=500, blank=True)
 	link = models.CharField(max_length=250, blank=True)
 	crawl_binary = models.IntegerField(default=0)
	date_added = models.DateTimeField(auto_now_add=True, blank=True)

	def __unicode__(self):
	 	return u'%s' % self.name

	def _get_name(self):
		return '%s' % self.name

	# def _crawled_status(self):
	# 	return self.crawl_binary

# 	class Meta:
# 		ordering = ['name']