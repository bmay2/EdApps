from django.db import models

class Apps(models.Model):

# 	SUBJECTS = (
# 		(u'B', u'Biology'),
# 		(u'F', u'French'),
# 	)
# 		
	PRICES = (
		('F', 'Free'),
		('1', 'Up to $1'),
		('3', 'Up to $3'),
		('5', 'Up to $5'),
		('10', 'Up to $10'),
		('25', 'Up to $25'),
		('50', 'Up to $50'),
		('50m', '$50 or more'),
	)

 	name = models.CharField(max_length=30)
	platform = models.CharField(max_length=30)
	subject = models.CharField(max_length=30)
# 	creator = models.CharField(max_length=30, blank=True)
	price = models.CharField('price', max_length=30, choices=PRICES) #, verbose_name='price')
# 	downloads = models.IntegerField(blank=True, null=True)
	rating = models.FloatField(blank=True, null=True)
# 	comment = models.CharField(max_length=7500, blank=True)
	
	def __unicode__(self):
		return u'%s %s' % (self.name, self.platform)

# 	class Meta:
# 		ordering = ['name']