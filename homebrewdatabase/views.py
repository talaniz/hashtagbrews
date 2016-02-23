from django.shortcuts import render


def index(request):

    return render(request, template_name='homebrewdatabase/index.html')


def homebrewmain(request):

    return render(request, template_name='homebrewdatabase/homebrewdatabase.html')


def hops(request):

    return render(request, template_name='homebrewdatabase/hops.html')