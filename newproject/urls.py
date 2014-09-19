from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'newproject.views.home', name='home'),
    # url(r'^newproject/', include('newproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r"^meta/", views.display_meta),
    url(r"^anything/?$", views.anything),
    url(r"^anything/goes/", views.what),
    url(r"^home/", views.home),
    url(r"^search-form/$", views.search_form),
    url(r"^search/", views.search),
    url(r"^login/", views.login),
    url(r"^minimax/", views.minimax),
    url(r"^about/", views.about),
    url(r"^contact/", views.contact),
    url(r'^(?P<page_alias>.+?)/$', views.static_page)
)
