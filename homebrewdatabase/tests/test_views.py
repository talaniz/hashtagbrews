from django.http import HttpRequest
from django.core.management import call_command
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.html import escape

from elasticsearch import Elasticsearch

from homebrewdatabase.forms import HopForm, GrainForm, YeastForm
from homebrewdatabase.models import Hop, Grain, Yeast
from homebrewdatabase.views import index, hops, addhops, grains, addgrains, yeasts, addyeasts


class TestHomePageView(TestCase):
    """Class for testing the main homepage view."""

    def test_homepage_returns_correct_template(self):
        """Index view should return index.html.
                :return: pass or fail
        """
        request = HttpRequest()
        response = index(request)
        expected_html = render_to_string('homebrewdatabase/index.html')
        self.assertEqual(response.content.decode(), expected_html)


class TestHopsPageView(TestCase):
    """Class for testing hops related views."""

    def setUp(self):
        self.es_client = Elasticsearch()
        call_command('push_hop_to_index')

        self.user = User.objects.create_user(username='testuser', email="user@example.com",
                                     password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def tearDown(self):
        call_command('push_hop_to_index')

    def test_can_add_new_hops_and_save_a_POST_request(self):
        """
        Testing that the user can add and save a hop record using a POST request
                :return: pass or fail
        """

        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'Amarillo'
        request.POST['min_alpha_acid'] = 8.00
        request.POST['max_alpha_acid'] = 11.00
        request.POST['country'] = 'USA'
        request.POST['comments'] = 'Good over all aroma and bittering hops'
        request.user = self.user

        addhops(request)

        self.assertEqual(Hop.objects.count(), 1)

        new_hop = Hop.objects.first()

        self.assertEqual(new_hop.name, 'Amarillo')
        self.assertAlmostEqual(new_hop.min_alpha_acid, 8.00)
        self.assertEqual(new_hop.max_alpha_acid, 11.00)
        self.assertEqual(new_hop.country, 'USA')
        self.assertEqual(new_hop.comments, 'Good over all aroma and bittering hops')

        es_hop_record = self.es_client.get(index='hop', id=new_hop.id, doc_type='hop')['_source']

        self.assertEqual(es_hop_record['name'], 'Amarillo')
        self.assertAlmostEqual(es_hop_record['min_alpha_acid'], 8.00)
        self.assertEqual(es_hop_record['max_alpha_acid'], 11.00)
        self.assertEqual(es_hop_record['country'], 'USA')
        self.assertEqual(es_hop_record['comments'], 'Good over all aroma and bittering hops')

    def test_add_hops_redirects_after_POST(self):
        """
        Test to check that accessing the 'addhops' url redirects with 302 and a url of '/beerdb/hops'
                :return: pass or fail
        """

        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'Amarillo'
        request.POST['min_alpha_acid'] = 8.00
        request.POST['max_alpha_acid'] = 11.00
        request.POST['country'] = 'USA'
        request.POST['comments'] = 'Good over all aroma and bittering hops'
        request.user = self.user
        response = addhops(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/beerdb/hops/')

    def test_hop_page_only_saves_when_necessary(self):
        """
        Tests that a non-POST request does not save values to the database
                :return: pass or fail
        """

        request = HttpRequest()
        hops(request)
        self.assertEqual(Hop.objects.count(), 0)

        es_hits = self.es_client.search(index='hop')['hits']['total']
        self.assertEqual(es_hits, 0)

    def test_hops_page_displays_all_hops_records(self):
        """
        Checks that the hops page displays all available hop records. Will be changed to a limited view in the future.
                :return: pass or fail
        """

        first_hop = Hop(name='Century',
                        min_alpha_acid=8.00,
                        max_alpha_acid=12.00,
                        country='USA',
                        comments='Pretty good, a little spicy',
                        user=self.user)
        first_hop.save()

        second_hop = Hop(name='Warrior',
                         min_alpha_acid=24.00,
                         max_alpha_acid=32.00,
                         country='USA',
                         comments='Very bitter, not good for aroma',
                         user=self.user
                         )
        second_hop.save()

        request = HttpRequest()
        response = hops(request)

        self.assertIn('Century', response.content.decode())
        self.assertIn('Warrior', response.content.decode())

    def test_add_hops_view_saves_record(self):
        """
        Checks that the 'addhops' view can take a POST request and save to the database
                :return: pass or fail
        """

        response = self.client.login(username='testuser', password='testpassword')
        self.assertEqual(response, True)

        response = self.client.post(
            '/beerdb/add/hops/',
            data={
                'name': 'Warrior',
                'min_alpha_acid': 24.00,
                'max_alpha_acid': 32.00,
                'country': 'USA',
                'comments': 'Very bitter, not good for aroma',
                'user': self.user
            })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/beerdb/hops/')

        hop_record = Hop.objects.filter(name='Warrior')

        self.assertEqual(hop_record[0].name, 'Warrior')

        es_hop_record = self.es_client.search(index='hop', body={"query": {"match": {'name': 'Warrior'}}})['hits']
        self.assertEqual(es_hop_record['total'], 1)

    def test_can_update_hops(self):
        """
        Checks that the '/beerdb/edit/%d/hops/' url can update a hop record with creating an additional record
                 :return: pass or fail
        """

        response = self.client.login(username='testuser', password='testpassword')
        self.assertEqual(response, True)

        self.client.post(
            '/beerdb/add/hops/',
            data={
                'name': 'Warrior',
                'min_alpha_acid': 24.00,
                'max_alpha_acid': 32.00,
                'country': 'USA',
                'comments': 'Very bitter, not good for aroma'
            })

        hop_instance = Hop.objects.filter(name='Warrior')[0]

        response = self.client.get('/beerdb/edit/%d/hops/' % hop_instance.id)

        self.assertEqual(response.status_code, 200)

        edit_form = response.context['form']
        hop_record = edit_form.initial

        hop_record['name'] = 'Chinook'

        response = self.client.post('/beerdb/edit/%d/hops/' % hop_instance.id, data=hop_record)

        self.assertEqual(response.status_code, 302)

        hop_list = Hop.objects.filter(name='Chinook')
        es_hop_record = self.es_client.search(index='hop', body={"query": {"match": {'name': 'Chinook'}}})['hits']

        self.assertEqual(len(hop_list), 1)
        self.assertEqual(es_hop_record['total'], 1)

        hop_list = Hop.objects.filter(name='Warrior')
        es_hop_record2 = self.es_client.search(index='hop', body={"query": {"match": {'name': 'Warrior'}}})['hits']

        self.assertEqual(len(hop_list), 0)
        self.assertEqual(es_hop_record2['total'], 0)

    def test_delete_hop_record(self):
        """
        Checks that the '/beerdb/delete/%d/hops' url can delete a hop record
                :return: pass or fail
        """

        response = self.client.login(username='testuser', password='testpassword')
        self.assertEqual(response, True)

        self.client.post(
            '/beerdb/add/hops/',
            data={
                'name': 'Northern',
                'min_alpha_acid': 18.00,
                'max_alpha_acid': 12.00,
                'country': 'USA',
                'comments': 'Very bitter, not good for aroma',
                'user': self.user
            })

        hop_instance = Hop.objects.filter(name='Northern')[0]
        es_hop_record = self.es_client.get(index='hop', id=hop_instance.id, doc_type='hop')['_source']

        self.assertEqual(hop_instance.name, 'Northern')
        self.assertEqual(es_hop_record['name'], 'Northern')

        response = self.client.get('/beerdb/delete/%d/hops/' % hop_instance.id)

        self.assertEqual(response.status_code, 200)

        response = self.client.post('/beerdb/delete/%d/hops/' % hop_instance.id)

        self.assertEqual(response.status_code, 302)

        hop_list = Hop.objects.filter(name='Northern')
        es_hop_record2 = self.es_client.search(index='hop', body={"query": {"match": {'name': 'Northern'}}})['hits']

        self.assertEqual(len(hop_list), 0)
        self.assertEqual(es_hop_record2['total'], 0)

    def test_add_hop_uses_item_form(self):
        """`addhops` should use a `HopForm` instance.
                :return: pass or fail
        """
        response = self.client.login(username='testuser', password='testpassword')
        self.assertEqual(response, True)

        response = self.client.get('/beerdb/add/hops/')
        self.assertIsInstance(response.context['form'], HopForm)

    def test_blank_input_on_addhops_page_returns_hops_list_page_with_errors(self):
        """
        Validation testing, user should not be able to save a hop record with blank information
                :return: pass or fail

                * 'country' field is excluded as it is a multiselect field with a valid default option
        """

        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = ''
        request.POST['min_alpha_acid'] = ''
        request.POST['max_alpha_acid'] = ''
        request.POST['country'] = 'USA'
        request.POST['comments'] = ''
        request.user = self.user

        response = addhops(request)

        self.assertEqual(response.status_code, 200)
        name_validation_error = escape("A hop name is required")
        min_alpha_acid_error = escape("You must enter a min alpha acid")
        max_alpha_acid_error = escape("You must enter a max alpha acid")
        comments_error = escape("You must enter a comment")

        self.assertContains(response, name_validation_error)
        self.assertContains(response, min_alpha_acid_error)
        self.assertContains(response, max_alpha_acid_error)
        self.assertContains(response, comments_error)

    def test_invalid_input_on_addhops_page_returns_hops_list_page_with_errors(self):
        """
        Validation test to check that strings will not be saved in Integer or Decimal fields
                :return: pass or fail
        """

        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'test'
        request.POST['min_alpha_acid'] = 'bad value'
        request.POST['max_alpha_acid'] = 'another bad value'
        request.POST['country'] = 'USA'
        request.POST['comments'] = 'stuffs'
        request.user = self.user

        response = addhops(request)

        self.assertEqual(response.status_code, 200)
        min_alpha_acid_error = escape("Min alpha acid must be a decimal number")
        max_alpha_acid_error = escape("Max alpha acid must be a decimal number")

        self.assertContains(response, min_alpha_acid_error)
        self.assertContains(response, max_alpha_acid_error)

    def test_blank_input_on_update_hops_page_returns_hops_list_page_with_errors(self):
        """
        Checks that validation error messages appear on the 'hops_list' page when blank input is saved
                :return: pass or fail
        """

        self.client.post(
            '/beerdb/add/hops/',
            data={
                'name': 'Warrior',
                'min_alpha_acid': 24.00,
                'max_alpha_acid': 32.00,
                'country': 'USA',
                'comments': 'Very bitter, not good for aroma',
                'user': self.user
            })

        hop_instance = Hop.objects.filter(name='Warrior')[0]

        response = self.client.get('/beerdb/edit/%d/hops/' % hop_instance.id)

        self.assertEqual(response.status_code, 200)

        edit_form = response.context['form']
        hop_record = edit_form.initial

        hop_record['name'] = ''
        hop_record['min_alpha_acid'] = ''
        hop_record['max_alpha_acid'] = ''
        hop_record['comments'] = ''

        response = self.client.post('/beerdb/edit/%d/hops/' % hop_instance.id, data=hop_record)

        self.assertEqual(response.status_code, 200)
        name_validation_error = escape("A hop name is required")
        min_alpha_acid_error = escape("You must enter a min alpha acid")
        max_alpha_acid_error = escape("You must enter a max alpha acid")
        comments_error = escape("You must enter a comment")

        self.assertContains(response, name_validation_error)
        self.assertContains(response, min_alpha_acid_error)
        self.assertContains(response, max_alpha_acid_error)
        self.assertContains(response, comments_error)

    def test_search_GET_request_returns_matching_results(self):

        self.client.post(
            '/beerdb/add/hops/',
            data={
                'name': 'Cascade',
                'min_alpha_acid': 19.00,
                'max_alpha_acid': 21.00,
                'country': 'USA',
                'comments': 'Very bitter, not good for aroma',
                'user': self.user
            })

        self.client.post(
            '/beerdb/add/hops/',
            data={
                'name': 'Chinook',
                'min_alpha_acid': 25.00,
                'max_alpha_acid': 31.00,
                'country': 'USA',
                'comments': 'High bitterness, similar to Cascade',
                'user': self.user
            })

        self.client.post(
            '/beerdb/add/hops/',
            data={
                'name': 'Amarillo',
                'min_alpha_acid': 24.00,
                'max_alpha_acid': 32.00,
                'country': 'USA',
                'comments': 'Very bitter, not good for aroma',
                'user': self.user
            })

        request = HttpRequest()

        request.method = 'GET'
        request.GET['query'] = 'Cascade'

        response = hops(request)

        self.assertIn('Cascade', response.content.decode())
        self.assertIn('High bitterness,', response.content.decode())
        self.assertNotIn('Amarillo', response.content.decode())


class TestGrainsPageView(TestCase):
    """
    Class for testing grain related views
    """

    def setUp(self):
        self.es_client = Elasticsearch()
        call_command('push_hop_to_index')

        self.user = User.objects.create_user(username='testuser',
                                             email="user@example.com",
                                             password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def tearDown(self):
        call_command('push_hop_to_index')

    def test_grains_page_returns_correct_template(self):
        """
        Test to check that '/beerdb/grains/' returns the grains.html template
                :return: pass or fail
        """

        response = self.client.get('/beerdb/grains/')
        self.assertTemplateUsed(response, 'homebrewdatabase/grains.html')

    def test_can_add_new_grain_and_save_a_POST_request(self):
        """
        Checks that a user can save a new post request using the Grain model
                :return: pass or fail
        """

        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'Carared'
        request.POST['degrees_lovibond'] = 1.5
        request.POST['specific_gravity'] = 120.00
        request.POST['grain_type'] = 'GRN'
        request.POST['comments'] = 'Amber red color'
        request.user = self.user

        addgrains(request)

        new_grain = Grain.objects.first()

        self.assertEqual(new_grain.name, 'Carared')
        self.assertAlmostEqual(new_grain.degrees_lovibond, 1.50)
        self.assertEqual(new_grain.specific_gravity, 120.00)
        self.assertEqual(new_grain.grain_type, 'GRN')
        self.assertEqual(new_grain.comments, 'Amber red color')

    def test_add_grains_redirects_after_POST(self):
        """
        Checks that the 'addgrains' url redirects to 'grains_list' after a POST request
                :return: pass or fail
        """

        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'Carared'
        request.POST['degrees_lovibond'] = 1.5
        request.POST['specific_gravity'] = 120.00
        request.POST['grain_type'] = 'GRN'
        request.POST['comments'] = 'Amber red color'
        request.user = self.user

        response = addgrains(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/beerdb/grains/')

    def test_add_grain_page_only_saves_when_necessary(self):
        """
        Test to check that the 'addgrains' page does not save additional records for non-POST requests
                :return: pass or fail
        """

        request = HttpRequest()
        request.user = self.user
        addgrains(request)
        self.assertEqual(Grain.objects.count(), 0)

    def test_grains_page_displays_all_grains_records(self):
        """
        Test to check that the 'grains_list' page displays all grain records
                :return: pass or fail
        """

        Grain.objects.create(name='Carared',
                             degrees_lovibond=1.50,
                             specific_gravity=120.00,
                             grain_type='GRN',
                             comments='Amber red color',
                             user=self.user
                             )

        Grain.objects.create(name='Pale Chocolate',
                             degrees_lovibond='150.00',
                             specific_gravity='12.00',
                             grain_type='GRN',
                             comments='Dark malt that gives a rich red or brown color',
                             user=self.user
                             )

        request = HttpRequest()
        response = grains(request)

        self.assertIn('Carared', response.content.decode())
        self.assertIn('Pale Chocolate', response.content.decode())

    def test_add_grains_view_saves_record(self):
        """
        Test to check that the 'addgrains' view saves records using the Grain model
                :return: pass or fail
        """

        response = self.client.post(
            '/beerdb/add/grains/',
            data={
                'name': 'Carared',
                'degrees_lovibond': 1.50,
                'specific_gravity': 120.00,
                'grain_type': 'GRN',
                'comments': 'Amber red color',
                'user': self.user
            })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/beerdb/grains/')

        grain_record = Grain.objects.filter(name='Carared')

        self.assertEqual(grain_record[0].name, 'Carared')

    def test_can_update_grain(self):
        """
        Tests that the user is able to use the '/beerdb/edit/%d/grains/' url to update a grain record
                :return: pass or fail
        """

        self.client.post(
            '/beerdb/add/grains/',
            data={
                'name': 'Carared',
                'degrees_lovibond': 24.00,
                'specific_gravity': 32.00,
                'grain_type': 'GRN',
                'comments': 'Adds reddish brown color',
                'user': self.user
            })

        grain_instance = Grain.objects.filter(name='Carared')[0]

        response = self.client.get('/beerdb/edit/%d/grains/' % grain_instance.id)

        self.assertEqual(response.status_code, 200)

        edit_form = response.context['form']
        grain_record = edit_form.initial

        grain_record['name'] = 'Chocolate Pale'

        response = self.client.post('/beerdb/edit/%d/grains/' % grain_instance.id, data=grain_record)

        self.assertEqual(response.status_code, 302)

        grain_list = Grain.objects.filter(name='Chocolate Pale')

        self.assertEqual(len(grain_list), 1)

        hop_list = Hop.objects.filter(name='Carared')

        self.assertEqual(len(hop_list), 0)

    def test_can_delete_grain(self):
        """
        Test to check that '/beerdb/delete/%d/grains/' allows users to successfully delete records
                :return: pass or fail
        """

        self.client.post(
            '/beerdb/add/grains/',
            data={'name': 'Munich Malt',
                  'degrees_lovibond': 10.00,
                  'specific_gravity': 1.20,
                  'grain_type': 'LME',
                  'comments': 'Sweet, toasted flavor and aroma',
                  'user': self.user
                  })

        grain_instance = Grain.objects.filter(name='Munich Malt')[0]

        self.assertEqual(grain_instance.name, 'Munich Malt')

        response = self.client.get('/beerdb/delete/%s/grains/' % grain_instance.id)

        self.assertEqual(response.status_code, 200)

        response = self.client.post('/beerdb/delete/%s/grains/' % grain_instance.id)

        self.assertEqual(response.status_code, 302)

        grains_list = Grain.objects.filter(name='Munich Malt')

        self.assertEqual(len(grains_list), 0)

    def test_add_grain_uses_grain_form(self):
        """
        Asserts that the 'addgrains' view is using a Grain form
                :return: pass or fail
        """

        response = self.client.get('/beerdb/add/grains/')

        self.assertIsInstance(response.context['form'], GrainForm)

    def test_blank_input_on_add_grains_page_returns_grains_list_page_with_errors(self):
        """
        Testing for blank input on 'addgrains' redirects to 'grains_list' with validation errors
                :return: pass or fail
        """

        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = ''
        request.POST['degrees_lovibond'] = ''
        request.POST['specific_gravity'] = ''
        request.POST['grain_type'] = 'GRN'
        request.POST['comments'] = ''
        request.user = self.user

        response = addgrains(request)

        self.assertEqual(response.status_code, 200)
        name_validation_error = escape('A grain name is required')
        degrees_lovibond_validation_error = escape('You must specify degrees lovibond')
        specific_gravity_validation_error = escape('You must enter a specific gravity')
        comments_validation_error = escape('You must leave a comment')

        self.assertContains(response, name_validation_error)
        self.assertContains(response, degrees_lovibond_validation_error)
        self.assertContains(response, specific_gravity_validation_error)
        self.assertContains(response, comments_validation_error)

    def test_invalid_input_on_add_grains_page_returns_grains_list_page_with_errors(self):
        """
        Checks that invalid input on the 'addgrains' view redirects to 'grains_list' with validation errors
                :return: pass or fail
        """

        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'Amber'
        request.POST['degrees_lovibond'] = 'number'
        request.POST['specific_gravity'] = 'another number'
        request.POST['grain_type'] = 'GRN'
        request.POST['comments'] = 'Amber color'
        request.user = self.user

        response = addgrains(request)

        self.assertEqual(response.status_code, 200)
        degrees_lovibond_validation_error = escape('Degrees lovibond must be a decimal number')
        specific_gravity_validation_error = escape('Specific gravity must be a decimal number')

        self.assertContains(response, degrees_lovibond_validation_error)
        self.assertContains(response, specific_gravity_validation_error)

    def test_blank_input_on_update_grains_page_returns_grains_list_with_errors(self):
        """
        Checks that blank input saved on the 'updategrain' view redirects to the 'grains_list' page with errors
                :return: pass or fail
        """

        self.client.post(
            '/beerdb/add/grains/',
            data={
                'name': 'Amber Dry',
                'degrees_lovibond': 23.00,
                'specific_gravity': 15.00,
                'grain_type': 'GRN',
                'comments': 'Dry grain, amber color',
                'user': self.user
             })

        grain_instance = Grain.objects.filter(name='Amber Dry')[0]

        response = self.client.get('/beerdb/edit/%d/grains/' % grain_instance.id)

        self.assertEqual(response.status_code, 200)

        edit_form = response.context['form']
        grain_record = edit_form.initial

        grain_record['name'] = ''
        grain_record['degrees_lovibond'] = ''
        grain_record['specific_gravity'] = ''
        grain_record['grain_type'] = 'GRN'
        grain_record['comments'] = ''

        response = self.client.post('/beerdb/edit/%d/grains/' % grain_instance.id, data=grain_record)

        self.assertEqual(response.status_code, 200)
        name_validation_error = escape("A grain name is required")
        degrees_lovibond_validation_error = escape('You must specify degrees lovibond')
        specific_gravity_validation_error = escape('You must enter a specific gravity')
        comments_validation_error = escape('You must leave a comment')

        self.assertContains(response, name_validation_error)
        self.assertContains(response, degrees_lovibond_validation_error)
        self.assertContains(response, specific_gravity_validation_error)
        self.assertContains(response, comments_validation_error)

    def test_search_GET_request_returns_matching_results(self):

        self.client.post(
            '/beerdb/add/grains/',
            data={
                'name': 'Amber Dry',
                'degrees_lovibond': 23.00,
                'specific_gravity': 15.00,
                'grain_type': 'GRN',
                'comments': 'Dry grain, amber color',
                'user': self.user
             })

        self.client.post(
            '/beerdb/add/grains/',
            data={'name': 'Munich Malt',
                  'degrees_lovibond': 10.00,
                  'specific_gravity': 1.20,
                  'grain_type': 'LME',
                  'comments': 'Sweet, toasted flavor and aroma',
                  'user': self.user
            })

        request = HttpRequest()

        request.method = 'GET'
        request.GET['query'] = 'Amber Dry'

        response = grains(request)

        self.assertIn('Amber Dry', response.content.decode())
        self.assertIn('Dry grain, ', response.content.decode())
        self.assertNotIn('Munich Malt', response.content.decode())


class TestYeastPageView(TestCase):
    """
    Class for testing yeast related views
    """

    def setUp(self):
        self.es_client = Elasticsearch()
        call_command('push_yeast_to_index')

        self.user = User.objects.create_user(username='testuser',
                                     email="user@example.com",
                                     password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def tearDown(self):
        call_command('push_yeast_to_index')

    def test_yeast_page_returns_correct_template(self):
        """
        Checks that the 'yeasts_list' page returns the 'yeasts.html' template
                :return: pass or fail
        """

        response = self.client.get('/beerdb/yeasts/')
        self.assertTemplateUsed(response, 'homebrewdatabase/yeasts.html')

    def test_can_add_new_yeast_and_save_a_POST_request(self):
        """
        Checks that the user is able to save a yeast record using the Yeast model with a POST request
                :return: pass or fail
        """

        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'Amarillo'
        request.POST['lab'] = 'Wyeast'
        request.POST['yeast_type'] = 'Ale'
        request.POST['yeast_form'] = 'Liquid'
        request.POST['min_temp'] = 60
        request.POST['max_temp'] = 72
        request.POST['attenuation'] = 75
        request.POST['flocculation'] = 'Medium'
        request.POST['comments'] = 'Well balanced.'
        request.user = self.user

        addyeasts(request)

        self.assertEqual(Yeast.objects.count(), 1)

        new_yeast = Yeast.objects.first()

        self.assertEqual(new_yeast.name, 'Amarillo')
        self.assertEqual(new_yeast.lab, 'Wyeast')
        self.assertEqual(new_yeast.yeast_type, 'Ale')
        self.assertEqual(new_yeast.yeast_form, 'Liquid')
        self.assertEqual(new_yeast.min_temp, 60)
        self.assertEqual(new_yeast.max_temp, 72)
        self.assertEqual(new_yeast.attenuation, 75)
        self.assertEqual(new_yeast.flocculation, 'Medium')
        self.assertEqual(new_yeast.comments, 'Well balanced.')

        es_yeast_record = self.es_client.get(index='yeast', id=new_yeast.id, doc_type='yeast')['_source']

        self.assertEqual(es_yeast_record['name'], 'Amarillo')
        self.assertEqual(es_yeast_record['lab'], 'Wyeast')
        self.assertEqual(es_yeast_record['yeast_type'], 'Ale')
        self.assertEqual(es_yeast_record['yeast_form'], 'Liquid')
        self.assertEqual(es_yeast_record['min_temp'], 60)
        self.assertEqual(es_yeast_record['max_temp'], 72)
        self.assertEqual(es_yeast_record['attenuation'], 75)
        self.assertEqual(es_yeast_record['flocculation'], 'Medium')
        self.assertEqual(es_yeast_record['comments'], 'Well balanced.')

    def test_add_yeasts_redirects_after_POST(self):
        """
        Test to check that accessing the 'addyeasts' url redirects with 302 and a url of '/beerdb/yeasts'
                :return: pass or fail
        """

        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'Alpine'
        request.POST['lab'] = 'Wyeast'
        request.POST['yeast_type'] = 'Ale'
        request.POST['yeast_form'] = 'Liquid'
        request.POST['min_temp'] = 60
        request.POST['max_temp'] = 72
        request.POST['attenuation'] = 75
        request.POST['flocculation'] = 'Medium'
        request.POST['comments'] = 'Well balanced.'
        request.user = self.user
        response = addyeasts(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/beerdb/yeasts/')

    def test_yeast_page_only_saves_when_necessary(self):
        """
        Tests that a non-POST request does not save values to the database
                :return: pass or fail
        """

        request = HttpRequest()
        request.user = self.user
        addyeasts(request)
        self.assertEqual(Yeast.objects.count(), 0)

        es_hits = self.es_client.search(index='yeast')['hits']['total']
        self.assertEqual(es_hits, 0)

    def test_yeast_page_displays_all_yeast_records(self):
        """
        Test to check that the yeasts page displays all saved yeast records
                :return: pass or fail
        """

        Yeast.objects.create(name="WLP002 ENGLISH ALE YEAST",
                             lab="White Labs",
                             yeast_type="Ale",
                             yeast_form="Liquid",
                             min_temp="65",
                             max_temp="68",
                             attenuation="68",
                             flocculation="Very High",
                             comments="A classic ESB strain from one of England's largest independent breweries.",
                             user=self.user)

        Yeast.objects.create(name='WLP566 BELGIAN SAISON II YEAST',
                             lab='White Labs',
                             yeast_type='Saison',
                             yeast_form='Liquid',
                             min_temp='68',
                             max_temp='78',
                             attenuation='82',
                             flocculation='Medium',
                             comments='Saison strain with more fruity ester production than with WLP565',
                             user=self.user)

        request = HttpRequest()
        response = yeasts(request)

        self.assertIn('WLP002 ENGLISH ALE YEAST', response.content.decode())
        self.assertIn('WLP566 BELGIAN SAISON II YEAST', response.content.decode())

    def test_add_yeast_view_saves_record(self):
        """
        Checks that 'addyeasts' vew can take a POT request and save to the database
                :return: pass or fail

        * Note: location check is redundant. Could be refactored to check more of the yeast model
        """

        response = self.client.post(
            '/beerdb/add/yeasts/',
            data={
                'name': "WLP002 ENGLISH ALE YEAST",
                'lab': "White Labs",
                'yeast_type': "Ale",
                'yeast_form': "Liquid",
                'min_temp': "65",
                'max_temp': "68",
                'attenuation': "68",
                'flocculation': "Very High",
                'comments': "A classic ESB strain from one of England's largest independent breweries.",
                'user': self.user
            })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/beerdb/yeasts/')

        yeast_record = Yeast.objects.filter(name='WLP002 ENGLISH ALE YEAST')

        self.assertEqual(yeast_record[0].name, 'WLP002 ENGLISH ALE YEAST')

        es_yeast_record = self.es_client.search(index='yeast',
                                                body={"query": {
                                                            "match": {
                                                                "name": "WLP002 ENGLISH ALE YEAST"}}})['hits']
        self.assertEqual(es_yeast_record['total'], 1)

    def test_add_yeasts_view_uses_yeast_form(self):
        """
        Checks that the 'addyeasts' form is using the YeastForm() in forms.py
                :return: pass or fails
        """

        response = self.client.get('/beerdb/add/yeasts/')
        self.assertIsInstance(response.context['form'], YeastForm)

    def test_can_update_yeasts(self):
        """
        Checks that the '/beerdb/edit/%d/yeasts/' url can update a yeast record with creating an additional record
                 :return: pass or fail
        """

        self.client.post('/beerdb/add/yeasts/',
                         data={'name': "WLP002 ENGLISH ALE YEAST",
                               'lab': "White Labs",
                               'yeast_type': "Ale",
                               'yeast_form': "Liquid",
                               'min_temp': "65",
                               'max_temp': "68",
                               'attenuation': "68",
                               'flocculation': "Very High",
                               'comments': "A classic ESB strain",
                               'user': self.user})

        yeast_instance = Yeast.objects.filter(name='WLP002 ENGLISH ALE YEAST')[0]

        response = self.client.get('/beerdb/edit/%d/yeasts/' % yeast_instance.id)

        self.assertEqual(response.status_code, 200)

        edit_form = response.context['form']
        yeast_record = edit_form.initial

        yeast_record['name'] = 'WLP004 IRISH ALE YEAST'

        response = self.client.post('/beerdb/edit/%s/yeasts/' % yeast_instance.id, data=yeast_record)

        self.assertEqual(response.status_code, 302)

        yeast_list = Yeast.objects.filter(name='WLP004 IRISH ALE YEAST')
        es_yeast_record = self.es_client.search(index='yeast',
                                                body={"query": {
                                                        "match": {
                                                            "name": 'WLP004 IRISH ALE YEAST'
                                                        }}})['hits']

        self.assertEqual(len(yeast_list), 1)
        self.assertEqual(es_yeast_record['total'], 1)

        yeast_list = Yeast.objects.filter(name='WLP002 ENGLISH ALE YEAST')
        es_yeast_record2 = self.es_client.search(index='yeast',
                                                 body={"query": {
                                                        "match": {
                                                            "name": 'ENGLISH'
                                                        }}})['hits']
        self.assertEqual(len(yeast_list), 0)
        self.assertEqual(es_yeast_record2['total'], 0)

    def test_can_delete_yeasts(self):
        """
        Checks that the '/beerdb/delete/%d/yeasts' urls can delete a hop record
                :return: pass or fail
        """

        self.client.post('/beerdb/add/yeasts/',
                         data={
                             'name': "WLP002 ENGLISH ALE YEAST",
                             'lab': "White Labs",
                             'yeast_type': "Ale",
                             'yeast_form': "Liquid",
                             'min_temp': "65",
                             'max_temp': "68",
                             'attenuation': "68",
                             'flocculation': "Very High",
                             'comments': "A classic ESB strain from one of England's largest independent breweries.",
                             'user': self.user
                         })

        yeast_instance = Yeast.objects.filter(name='WLP002 ENGLISH ALE YEAST')[0]
        es_yeast_record = self.es_client.get(index='yeast', id=yeast_instance.id, doc_type='yeast')['_source']

        self.assertEqual(yeast_instance.name, 'WLP002 ENGLISH ALE YEAST')
        self.assertEqual(es_yeast_record['name'], 'WLP002 ENGLISH ALE YEAST')

        response = self.client.get('/beerdb/delete/%d/yeasts/' % yeast_instance.id)

        self.assertEqual(response.status_code, 200)

        self.client.post('/beerdb/delete/%d/yeasts/' % yeast_instance.id)

        yeast_list = Yeast.objects.filter(name="WLP002 ENGLISH ALE YEAST")
        es_yeast_record2 = self.es_client.search(index='yeast',
                                                 body={"query": {"match": {"name": "ENGLISH"}}})['hits']

        self.assertEqual(len(yeast_list), 0)
        self.assertEqual(es_yeast_record2['total'], 0)

    def test_blank_input_on_add_yeasts_page_returns_yeasts_list_page_with_errors(self):
        """
        Checks that blanks input on the 'addyeasts' view redirects to 'yeasts_list' with validation errors
                :return: pass or fail
        """

        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = ''
        request.POST['lab'] = 'Brewferm'
        request.POST['yeast_type'] = 'Ale'
        request.POST['yeast_form'] = 'Liquid'
        request.POST['min_temp'] = ''
        request.POST['max_temp'] = ''
        request.POST['attenuation'] = ''
        request.POST['flocculation'] = 'Medium'
        request.POST['comments'] = ''
        request.user = self.user

        response = addyeasts(request)

        self.assertEqual(response.status_code, 200)
        name_validation_error = escape("A yeast name is required")
        min_temp_validation_error = escape("You must enter a min temp")
        max_temp_validation_error = escape("You must enter a max temp")
        attenuation_validation_error = escape("You must enter an attenuation")
        comment_validation_error = escape("You must enter a comment")

        self.assertContains(response, name_validation_error)
        self.assertContains(response, min_temp_validation_error)
        self.assertContains(response, max_temp_validation_error)
        self.assertContains(response, attenuation_validation_error)
        self.assertContains(response, comment_validation_error)

    def test_invalid_input_on_add_yeasts_page_returns_yeasts_list_page_with_errors(self):
        """
        Checks that invalid input on the 'addyeasts' view redirects to the 'yeasts_list' with custom validation errors
                :return: pass or fail
        """

        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'WLP0065 Ale Yeast'
        request.POST['lab'] = 'Brewferm'
        request.POST['yeast_type'] = 'Ale'
        request.POST['yeast_form'] = 'Liquid'
        request.POST['min_temp'] = 'eighty eight'
        request.POST['max_temp'] = 'ninety two'
        request.POST['attenuation'] = 'thirty'
        request.POST['flocculation'] = 'Medium'
        request.user = self.user

        response = addyeasts(request)

        self.assertEqual(response.status_code, 200)
        min_temp_validation_error = "Min temp must be a number"
        max_temp_validation_error = "Max temp must be a number"
        attenuation_validation_error = "Attenuation must be a number"

        self.assertContains(response, min_temp_validation_error)
        self.assertContains(response, max_temp_validation_error)
        self.assertContains(response, attenuation_validation_error)

    def test_search_GET_request_returns_matching_results(self):

        self.client.post(
            '/beerdb/add/yeasts/',
            data={
                'name': 'American Ale II 1272',
                'lab': 'Wyeast',
                'yeast_type': 'Ale',
                'yeast_form': 'Liquid',
                'min_temp': 60,
                'max_temp': 72,
                'attenuation': 75,
                'flocculation': 'Low',
                'comments': 'Well balanced.',
                'user': self.user
                })

        self.client.post(
            '/beerdb/add/yeasts/',
            data={'name': 'American Ale 1056',
                  'lab': 'Brewtek',
                  'yeast_type': 'Saison',
                  'yeast_form': 'Dry',
                  'min_temp': 61,
                  'max_temp': 73,
                  'attenuation': 76,
                  'flocculation': 'Medium',
                  'comments': 'Sweet, toasted flavor and aroma',
                  'user': self.user
                  })

        request = HttpRequest()

        request.method = 'GET'
        request.GET['query'] = 'American'

        response = yeasts(request)

        # Yeast 1
        self.assertIn('American Ale II 1272' , response.content.decode())
        self.assertIn('Wyeast' , response.content.decode())
        self.assertIn('Ale', response.content.decode())
        self.assertIn('Liquid', response.content.decode())
        self.assertIn('60', response.content.decode())
        self.assertIn('72', response.content.decode())
        self.assertIn('75', response.content.decode())
        self.assertIn('Low', response.content.decode())
        self.assertIn('Well balanced.', response.content.decode())

        # Yeast 2
        self.assertIn('American Ale 1056', response.content.decode())
        self.assertIn('Brewtek', response.content.decode())
        self.assertIn('Saison', response.content.decode())
        self.assertIn('Dry', response.content.decode())
        self.assertIn('61', response.content.decode())
        self.assertIn('73', response.content.decode())
        self.assertIn('76', response.content.decode())
        self.assertIn('Medium', response.content.decode())
        self.assertIn('Sweet, toasted flavor and aroma', response.content.decode())
