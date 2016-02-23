from django.http import HttpResponse
from django.shortcuts import render


def index(request):

    return render(request, template_name='homebrewdatabase/index.html')


def homebrewmain(request):

    return render(request, template_name='homebrewdatabase/homebrewdatabase.html')


def hops(request):
    return render(request, 'homebrewdatabase/hops.html',
                  {'new_hops_name':  request.POST.get('hops_name', ''),
                   'min_alpha_acid': request.POST.get('min_alpha_acid', ''),
                   'max_alpha_acid': request.POST.get('max_alpha_acid', ''),
                   'countries':      request.POST.get('countries', ''),
                   'comments':       request.POST.get('comments', ''),
                   })
