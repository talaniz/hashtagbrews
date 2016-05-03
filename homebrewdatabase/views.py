from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from .forms import HopForm, GrainForm
from .models import Hop, Grain, Yeast


def index(request):
    """
    HashtagBrews main site page view
            :param request: Django HttpRequest object
            :return: renders 'homebrewdatabase/index.html'
    """

    return render(request, template_name='homebrewdatabase/index.html')


def homebrewmain(request):
    """
    Main page for the Homebrew Database
            :param request: Django HttpRequest object
            :return: renders
    """

    return render(request, template_name='homebrewdatabase/homebrewdatabase.html')


def hops(request):
    """
    Main hops page list
             :param request: Django HttpRequest object
             :return: renders 'homebrewdatabase/hops.html';

             * context
                 - 'hops'
                 - 'form'
    """

    hops_list = Hop.objects.all()
    return render(request, 'homebrewdatabase/hops.html', {'hops': hops_list, 'form': HopForm()})


def addhops(request):
    """
    Modal form for adding a hop record. Shows all form fields.
            :param request: Django HttpRequest object
            :return: renders 'homebrewdatabase/addhops.html' by default, otherwise 'homebrewdatabase/hops.html'

        * context
            - 'hops'
            - 'form'

        * success_url: 'hops_list'
    """

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
    """
    Modal form to update a hop record. Shows all form fields.
            :param request: Django HttpRequest object
            :param pk: primary key of the hop record to be updated
            :return: renders 'hombrewdatabase/updatehops.html' by default, otherwise 'hombrewdatabase'hops.html'

        * context
                - 'hops'
                - 'form'
                - 'errors'

        * success_url: 'hops_list'
    """

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
    """
    Modal form to delete hop record. Shows hop record name
            :param request: Django HttpRequest object
            :param pk: primary key of the hop record to be deleted
            :return: renders 'homebrewdatabase/deletehops.html'

            * success_url: 'hops_list'
    """

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
    """
    Main grains page list
            :param request: Django HttpRequest object
            :return: renders 'homebrewdatabase/grains.html'

            * context
                - 'hops'
                - 'form'
    """

    grains_list = Grain.objects.all()
    return render(request, 'homebrewdatabase/grains.html', {'grains': grains_list, 'form': GrainForm()})


def addgrains(request):
    """
    Modal form for adding a grain record. Shows all form fields.
            :param request: Django HttpRequest object
            :return: renders 'homebrewdatabase/addgrains.html' by default, otherwise 'homebrewdatabase/grains.html'

            * context
                - 'grains'
                - 'form'

            * success_url: 'grains_list'
    """

    add_form = GrainForm(request.POST or None)

    if request.method == 'POST':
        if add_form.is_valid():
            Grain.objects.create(name=request.POST['name'],
                                 degrees_lovibond=request.POST['degrees_lovibond'],
                                 specific_gravity=request.POST['specific_gravity'],
                                 grain_type=request.POST['grain_type'],
                                 comments=request.POST['comments']
                                 )
            return redirect('grains_list')
        else:
            grains_list = Grain.objects.all()
            return render(request, 'homebrewdatabase/grains.html', {'grains': grains_list, 'form': add_form})
    return render(request, 'homebrewdatabase/addgrains.html', {'form': add_form})


def updategrains(request, pk):
    """
    Modal form to update a grain record. Shows all form fields.
            :param request: Django HttpRequest object
            :param pk: primary key of the grain record to be updated
            :return: renders 'hombrewdatabase/updategrains.html' by default, otherwise 'hombrewdatabase/grains.html'

            * context
                - 'grains'
                - 'form'
                - 'errors'

            * success_url: 'grains_list'
    """

    grain_record = Grain.objects.filter(pk=pk)[0]
    edit_form = GrainForm(request.POST or None, instance=grain_record)

    if request.method == 'POST':
        if edit_form.is_valid():
            edit_form.save()
            success_url = reverse('grains_list')
            return redirect(success_url)
        else:
            grains_list = Grain.objects.all()
            return render(request, 'homebrewdatabase/grains.html', {'grains': grains_list,
                                                                    'form': GrainForm(),
                                                                    'errors': edit_form.errors})
    grain_form_url = reverse('updategrains', kwargs={'pk': grain_record.id})
    return render(request, 'homebrewdatabase/updategrains.html', {
                  'action': grain_form_url,
                  'form': edit_form
                  })


def deletegrains(request, pk):
    """
    Modal form to delete grain record. Shows grain record name
            :param request: Django HttpRequest object
            :param pk: primary key of the grain record to be deleted
            :return: renders 'homebrewdatabase/deletegrains.html' by default

            * success_url: 'grains_list'
    """

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


def yeasts(request):
    """
    Main homepage for viewing yeast records
            :param request: Django HttpRequest object
            :return: renders 'homebrewdatabase/yeasts.html'

            * context
                - 'yeasts'
                - 'form'
    """
    yeasts_list = Yeast.objects.all()
    return render(request, 'homebrewdatabase/yeasts.html', {'yeasts': yeasts_list})


def addyeasts(request):
    """
    Modal form for adding a yeast record. Shows all form fields.
            :param request: Django HttpRequest object
            :return: renders 'homebrewdatabase/addyeasts.html' by default, otherwise 'homebrewdatabase/yeasts.html'

            * context
                - 'yeasts'
                - 'form'

            * success_url: 'yeasts_list'
    """

    if request.method == 'POST':
        Yeast.objects.create(name=request.POST.get('name', ''),
                             lab=request.POST.get('lab', ''),
                             yeast_type=request.POST.get('yeast_type', ''),
                             yeast_form=request.POST.get('yeast_form', ''),
                             min_temp=request.POST.get('min_temp', ''),
                             max_temp=request.POST.get('max_temp', ''),
                             attenuation=request.POST.get('attenuation', ''),
                             flocculation=request.POST.get('flocculation'),
                             comments=request.POST.get('comments', '')
                             )
        return redirect('yeasts_list')
    return render(request, 'homebrewdatabase/addyeasts.html')