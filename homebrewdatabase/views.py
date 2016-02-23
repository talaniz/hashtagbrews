from django.http import HttpResponse
from django.shortcuts import render


def index(request):

    return render(request, template_name='homebrewdatabase/index.html')


def homebrewmain(request):

    return render(request, template_name='homebrewdatabase/homebrewdatabase.html')


def hops(request):
    return render(request, 'homebrewdatabase/hops.html',
                  {'new_hops_name': request.POST.get('hops_name', ''),
                   })
