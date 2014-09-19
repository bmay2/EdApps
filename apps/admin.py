from django.contrib import admin
from apps.models import Apps

class AppsAdmin(admin.ModelAdmin):
	list_display = ('name', 'platform', 'subject', 'price')
	search_fields = ('name', 'subject')

admin.site.register(Apps, AppsAdmin)


	