from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import HopForm
from .models import Hop


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


def updatehops(request, pk):

    hop_record = Hop.objects.filter(pk=pk)[0]
    edit_form = HopForm(request.POST or None, instance=hop_record)

    if request.method == 'POST':
        if edit_form.is_valid():
            edit_form.save()
            success_url = reverse('hops_list')
            return redirect(success_url)
    hop_form_url = reverse('updatehops', kwargs={'pk': hop_record.id})
    return render(request, 'homebrewdatabase/updatehops.html',
                  {'action': hop_form_url,
                   'form': edit_form
                   })
