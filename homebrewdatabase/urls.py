from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.homebrewmain, name='beerdb_main'),
    url(r'^hops/$', views.hops, name='hops_list'),
    url(r'^add/hops/$', views.addhops, name='addhops'),
]