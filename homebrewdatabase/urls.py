from django.conf.urls import url

from . import views

# TODO: organize urls to make them more readable. Sort by name, ingredient

urlpatterns = [
    url(r'^delete/(?P<pk>[0-9]+)/hops/$', views.deletehops, name='deletehops'),
    url(r'^edit/(?P<pk>[0-9]+)/hops/$', views.updatehops, name='updatehops'),
    url(r'^edit/(?P<pk>[0-9]+)/grains/$', views.updategrains, name='updategrains'),
    url(r'^edit/(?P<pk>[0-9]+)/yeasts/$', views.updateyeasts, name='updateyeasts'),
    url(r'^delete/(?P<pk>[0-9]+)/grains/$', views.deletegrains, name='deletegrains'),
    url(r'^delete/(?P<pk>[0-9]+)/yeasts/$', views.deleteyeasts, name='deleteyeasts'),
    url(r'^$', views.homebrewmain, name='beerdb_main'),
    url(r'^hops/$', views.hops, name='hops_list'),
    url(r'^add/hops/$', views.addhops, name='addhops'),
    url(r'^grains/$', views.grains, name='grains_list'),
    url(r'^add/grains/$', views.addgrains, name='addgrains'),
    url(r'^yeasts/$', views.yeasts, name='yeasts_list'),
    url(r'^add/yeasts/$', views.addyeasts, name='addyeasts'),
]
