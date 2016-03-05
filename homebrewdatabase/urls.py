from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^edit/(?P<pk>[0-9]+)/hops/$', views.updatehops, name='updatehops'),
    url(r'^$', views.homebrewmain, name='beerdb_main'),
    url(r'^hops/$', views.hops, name='hops_list'),
    url(r'^add/hops/$', views.addhops, name='addhops'),
]