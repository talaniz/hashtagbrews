from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from .forms import HopForm, GrainForm
from .models import Hop, Grain


def index(request):

    return render(request, template_name='homebrewdatabase/index.html')


def homebrewmain(request):

    return render(request, template_name='homebrewdatabase/homebrewdatabase.html')


def hops(request):
    hops_list = Hop.objects.all()
    return render(request, 'homebrewdatabase/hops.html', {'hops': hops_list, 'form': HopForm()})


def addhops(request):

    add_form = HopForm(request.POST or None)

    if request.method == 'POST':
        if add_form.is_valid():
            Hop.objects.create(name=request.POST['name'],
                               min_alpha_acid=request.POST['min_alpha_acid'],
                               max_alpha_acid=request.POST['max_alpha_acid'],
                               country=request.POST['country'],
                               comments=request.POST['comments']
                               )
            return redirect('hops_list')
        else:
            hops_list = Hop.objects.all()
            return render(request, 'homebrewdatabase/hops.html', {'hops': hops_list, 'form': add_form})
    return render(request, 'homebrewdatabase/addhops.html', {'form': add_form})


def updatehops(request, pk):

    hop_record = Hop.objects.filter(pk=pk)[0]
    edit_form = HopForm(request.POST or None, instance=hop_record)

    if request.method == 'POST':
        if edit_form.is_valid():
            edit_form.save()
            success_url = reverse('hops_list')
            return redirect(success_url)
        else:
            hops_list = Hop.objects.all()
            return render(request, 'homebrewdatabase/hops.html', {'hops': hops_list,
                                                                  'form': HopForm(),
                                                                  'errors': edit_form.errors
                                                                  })
    hop_form_url = reverse('updatehops', kwargs={'pk': hop_record.id})
    return render(request, 'homebrewdatabase/updatehops.html',
                  {'action': hop_form_url,
                   'form': edit_form
                   })


def deletehops(request, pk):

    hop_record = Hop.objects.filter(pk=pk)[0]

    if request.method == 'POST':
        hop_record.delete()
        success_url = reverse('hops_list')
        return redirect(success_url)
    hop_form_url = reverse('deletehops', kwargs={'pk': hop_record.id})
    return render(request, 'homebrewdatabase/deletehops.html',
                  {'action': hop_form_url,
                   'hop': hop_record
                   })


def grains(request):
    grains_list = Grain.objects.all()
    return render(request, 'homebrewdatabase/grains.html', {'grains': grains_list, 'form': GrainForm()})


def addgrains(request):
    add_form = GrainForm(request.POST or None)

    if request.method == 'POST':
        Grain.objects.create(name=request.POST.get('name', ''),
                             degrees_lovibond=request.POST.get('degrees_lovibond', ''),
                             specific_gravity=request.POST.get('specific_gravity', ''),
                             grain_type=request.POST.get('grain_type', ''),
                             comments=request.POST.get('comments', '')
                             )
        success_url = reverse('grains_list')
        return redirect(success_url)
    return render(request, 'homebrewdatabase/addgrains.html', {'form': add_form})


def updategrains(request, pk):

    grain_record = Grain.objects.filter(pk=pk)[0]
    edit_form = GrainForm(request.POST or None, instance=grain_record)

    if request.method == 'POST':
        if edit_form.is_valid():
            edit_form.save()
            success_url = reverse('grains_list')
            return redirect(success_url)
    grain_form_url = reverse('updategrains', kwargs={'pk': grain_record.id})
    return render(request, 'homebrewdatabase/updategrains.html', {
                  'action': grain_form_url,
                  'form': edit_form
                  })


def deletegrains(request, pk):

    grain_record = Grain.objects.filter(pk=pk)[0]

    if request.method == 'POST':
        grain_record.delete()
        success_url = reverse('grains_list')
        return redirect(success_url)

    grain_form_url = reverse('deletegrains', kwargs={'pk': grain_record.id})
    return render(request, 'homebrewdatabase/deletegrains.html', {
                  'action': grain_form_url,
                  'grain': grain_record
                  })
