from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

from .models import Hop

from .forms import HopForm

def index(request):

    return render(request, template_name='homebrewdatabase/index.html')


def homebrewmain(request):

    return render(request, template_name='homebrewdatabase/homebrewdatabase.html')


def hops(request):
    hops_list = Hop.objects.all()
    return render(request, 'homebrewdatabase/hops.html', {'hops': hops_list, 'form': HopForm()})


def addhops(request):
    if request.method == 'POST':
        Hop.objects.create(name=request.POST['name'],
                           min_alpha_acid=request.POST['min_alpha_acid'],
                           max_alpha_acid=request.POST['max_alpha_acid'],
                           country=request.POST['country'],
                           comments=request.POST['comments']
                           )
        return redirect('/beerdb/hops')
    return render(request, 'homebrewdatabase/addhops.html', {'form': HopForm()})
