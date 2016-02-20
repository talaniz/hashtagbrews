from django.conf.urls import url


urlpatterns = [
    url(r'$', 'homebrewdatabase.views.homebrewmain', name='beerdb_main')
]