from django.shortcuts import redirect, render

from .models import Hop


def index(request):

    return render(request, template_name='homebrewdatabase/index.html')


def homebrewmain(request):

    return render(request, template_name='homebrewdatabase/homebrewdatabase.html')


def hops(request):
    if request.method == 'POST':
        Hop.objects.create(name=request.POST['hops_name'],
                           min_alpha_acid=request.POST['min_alpha_acid'],
                           max_alpha_acid=request.POST['max_alpha_acid'],
                           country=request.POST['countries'],
                           comments=request.POST['comments']
                           )
        return redirect('/beerdb/hops')
    hops = Hop.objects.all()
    return render(request, 'homebrewdatabase/hops.html', {'hops': hops}Hop)
