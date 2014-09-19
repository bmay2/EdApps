from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from apps.models import Apps
	
def anything(request):
	print request
	return HttpResponse("Here's your page with anything you want!")
	
def what(request):
	print request
	return HttpResponse("Why doesn't this work?")

def home(request):
	return render_to_response('base_home.html', locals(), RequestContext(request))
	
def search_form(request):
	return render_to_response('base_search_new.html',
			{'subjects': Apps.objects.values_list('subject', flat=True).distinct().exclude(subject=''),
			 'ratings': Apps.objects.values_list('rating', flat=True).distinct().exclude(rating=None),
			 'prices': Apps.objects.values_list('price', flat=True).distinct().exclude(price=None),
			 'platforms': Apps.objects.values_list('platform', flat=True).distinct().exclude(platform='')},
			 RequestContext(request))
	
def display_meta(request): # implemented after tutorial
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))
	
def search(request): 
	subject = request.GET.getlist('subject')
	if not subject:
		subject = Apps.objects.values_list('subject').distinct()
	
	rating = request.GET.getlist('rating')
	if not rating:
		rating = Apps.objects.values_list('rating').distinct()

	price = request.GET.getlist('price')
	price = price[0].split(';')
	price = [float(i) for i in range(int(price[0]), int(price[1])+1)]
	lower, upper = price[0]-.50, price[len(price)-1]+.50
	results = Apps.objects.filter(subject__in=subject, rating__in=rating, price__gte=lower, price__lte=upper)

	# paginator = Paginator(result_list, 25)

	# try:
	# 	results = paginator.page(page)
	# except PageNotAnInteger:
	# 	results = paginator.page(1)
	# except EmptyPage:
	# 	results = paginator.page(paginator.num_pages)

	return render_to_response('base_results.html', {'results': results}, RequestContext(request))
	
def static_page(request, page_alias):
	try:
		active = Apps.objects.get(name=page_alias)
	except App.DoesNotExist:
		raise Http404("Page does not exist")
    
def login(request):
	return render_to_response('base_login.html', RequestContext(request))
	
def about(request):
	return render_to_response('base_about.html', RequestContext(request))

def contact(request):
	return render_to_response('base_contact.html', RequestContext(request))

def minimax(request):
	return render_to_response('base_minimax.html', RequestContext(request))
