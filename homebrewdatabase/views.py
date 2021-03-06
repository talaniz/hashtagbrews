from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render

from .forms import HopForm, GrainForm, YeastForm
from .models import Hop, Grain, Yeast

from elasticsearch import Elasticsearch

es_client = Elasticsearch()


def index(request):
    """HashtagBrews main site page view.
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

    # hops_list = Hop.objects.all()
    hops_list = []
    es = Elasticsearch()
    if request.GET.get('query'):
        entries = es.search(index='hop', body={"query": {
                                                    "query_string": {
                                                        "fields": ["name", "country", "comments"],
                                                        "query": request.GET['query']
                                                                    }
                                                        }})['hits']['hits']
    else:
        entries = es_client.search(index='hop')['hits']['hits']

    # Add the id to the source field and build the list of entries
    # Should this be a helper function to use in all 3 views?
    for entry in entries:
        entry['_source']['id'] = entry['_id']
        entry = entry['_source']
        hops_list.append(entry)
    return render(request, 'homebrewdatabase/hops.html', {'hops': hops_list, 'form': HopForm()})

@login_required()
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
            hop = add_form.save(commit=False)
            hop.user = request.user
            hop.save()
            return redirect('hops_list')
        else:
            # FIXME: This should use Elasticsearch
            hops_list = Hop.objects.all()
            return render(request, 'homebrewdatabase/hops.html', {'hops': hops_list, 'form': HopForm(),
                                                                  'error_form': add_form})
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
    grains_list = []
    es = Elasticsearch()
    if request.GET.get('query'):
        entries = es.search(index='grain', body={"query": {
                                                      "query_string": {
                                                           "fields": ["name", "grain_type", "comments"],
                                                           "query": request.GET['query']
                                                                      }
                                                      }})['hits']['hits']
    else:
        entries = es_client.search(index='grain')['hits']['hits']
    for entry in entries:
        entry['_source']['id'] = entry['_id']
        entry = entry['_source']
        grains_list.append(entry)
    return render(request, 'homebrewdatabase/grains.html', {'grains': grains_list, 'form': GrainForm()})

@login_required()
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
            grain = add_form.save(commit=False)
            grain.user = request.user
            grain.save()
            return redirect('grains_list')
        else:
            grains_list = Grain.objects.all()
            return render(request, 'homebrewdatabase/grains.html', {'grains': grains_list, 'form': GrainForm(),
                                                                    'error_form': add_form})
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

    yeasts_list = []
    es = Elasticsearch()
    if request.GET.get('query'):
        entries = es.search(index='yeast',
                            body={"query": {
                                    "query_string": {
                                            "fields": ["name", "lab", "yeast_type",
                                                       "yeast_form", "comments"],
                                            "query": request.GET['query']
                                                      }
                                             }})['hits']['hits']
    else:
        entries = es_client.search(index='yeast')['hits']['hits']

    for entry in entries:
        entry['_source']['id'] = entry['_id']
        entry = entry['_source']
        yeasts_list.append(entry)
    return render(request, 'homebrewdatabase/yeasts.html', {'yeasts': yeasts_list, 'form': YeastForm()})


@login_required()
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

    add_form = YeastForm(request.POST or None)

    if request.method == 'POST':
        if add_form.is_valid():
            yeast = add_form.save(commit=False)
            yeast.user = request.user
            yeast.save()
            return redirect('yeasts_list')
        else:
            yeasts_list = Yeast.objects.all()
            return render(request, 'homebrewdatabase/yeasts.html', {'yeasts': yeasts_list, 'form': YeastForm(),
                                                                    'error_form': add_form})
    return render(request, 'homebrewdatabase/addyeasts.html', {'form': add_form})


def updateyeasts(request, pk):
    """
    Modal form to update a yeast record. Shows all form fields.
            :param request: Django HttpRequest object
            :param pk: primary key of the yeast record to be updated
            :return: renders 'hombrewdatabase/updateyeasts.html' by default, otherwise 'hombrewdatabase/yeasts.html'

            * context
                - 'yeasts'
                - 'form'
                - 'errors'

            * success_url: 'yeasts_list'
    """

    yeast_record = Yeast.objects.filter(pk=pk)[0]
    edit_form = YeastForm(request.POST or None, instance=yeast_record)

    if request.method == 'POST':
        if edit_form.is_valid():
            edit_form.save()
            success_url = reverse('yeasts_list')
            return redirect(success_url)
        else:
            yeasts_list = Yeast.objects.all()
            return render(request, 'homebrewdatabase/yeasts.html', {'yeasts': yeasts_list,
                                                                   'form': YeastForm(),
                                                                   'errors': edit_form.errors})
    yeast_form_url = reverse('updateyeasts', kwargs={'pk': yeast_record.id})
    return render(request, 'homebrewdatabase/updateyeasts.html',
                  {'action': yeast_form_url,
                   'form': edit_form
                   })


def deleteyeasts(request, pk):
    """
    Modal form to delete yeast record. Shows yeast record name
            :param request: Django HttpRequest object
            :param pk: primary key of the yeast record to be deleted
            :return: renders 'hombrewdatabase/deleteyeasts.html'

            * success_url: 'yeasts_list'
    """

    yeast_record = Yeast.objects.filter(pk=pk)[0]

    if request.method == 'POST':
        yeast_record.delete()
        success_url = reverse('yeasts_list')
        return redirect(success_url)
    yeast_form_url = reverse('deleteyeasts', kwargs={'pk': yeast_record.id})
    return render(request, 'homebrewdatabase/deleteyeasts.html',
                  {'action': yeast_form_url,
                   'yeast': yeast_record
                   })
