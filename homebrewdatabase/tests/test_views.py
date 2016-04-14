from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.html import escape

from homebrewdatabase.forms import HopForm
from homebrewdatabase.models import Hop, Grain
from homebrewdatabase.views import index, hops, addhops, grains, addgrains


class TestHomePageView(TestCase):

    def test_homepage_returns_correct_template(self):
        request = HttpRequest()
        response = index(request)
        expected_html = render_to_string('homebrewdatabase/index.html')
        self.assertEqual(response.content.decode(), expected_html)


class TestHopsPageView(TestCase):

    def test_can_add_new_hops_and_save_a_POST_request(self):
        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'Amarillo'
        request.POST['min_alpha_acid'] = 8.00
        request.POST['max_alpha_acid'] = 11.00
        request.POST['country'] = 'USA'
        request.POST['comments'] = 'Good over all aroma and bittering hops'

        addhops(request)

        self.assertEqual(Hop.objects.count(), 1)

        new_hop = Hop.objects.first()

        self.assertEqual(new_hop.name, 'Amarillo')
        self.assertAlmostEqual(new_hop.min_alpha_acid, 8.00)
        self.assertEqual(new_hop.max_alpha_acid, 11.00)
        self.assertEqual(new_hop.country, 'USA')
        self.assertEqual(new_hop.comments, 'Good over all aroma and bittering hops')

    def test_add_hops_redirects_after_POST(self):
        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'Amarillo'
        request.POST['min_alpha_acid'] = 8.00
        request.POST['max_alpha_acid'] = 11.00
        request.POST['country'] = 'USA'
        request.POST['comments'] = 'Good over all aroma and bittering hops'

        response = addhops(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/beerdb/hops/')

    def test_hop_page_only_saves_when_necessary(self):
        request = HttpRequest()
        hops(request)
        self.assertEqual(Hop.objects.count(), 0)

    def test_home_page_displays_all_hops_records(self):
        Hop.objects.create(name='Century',
                           min_alpha_acid=8.00,
                           max_alpha_acid=12.00,
                           country='USA',
                           comments='Pretty good, a little spicy')

        Hop.objects.create(name='Warrior',
                           min_alpha_acid=24.00,
                           max_alpha_acid=32.00,
                           country='USA',
                           comments='Very bitter, not good for aroma')

        request = HttpRequest()
        response = hops(request)

        self.assertIn('Century', response.content.decode())
        self.assertIn('Warrior', response.content.decode())

    def test_add_hops_view_saves_record(self):

        response = self.client.post(
            '/beerdb/add/hops/',
            data={
                'name': 'Warrior',
                'min_alpha_acid': 24.00,
                'max_alpha_acid': 32.00,
                'country': 'USA',
                'comments': 'Very bitter, not good for aroma'
            })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/beerdb/hops/')

        hop_record = Hop.objects.filter(name='Warrior')

        self.assertEqual(hop_record[0].name, 'Warrior')

    def test_can_update_hops(self):
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

        self.assertEqual(len(hop_list), 1)

        hop_list = Hop.objects.filter(name='Warrior')

        self.assertEqual(len(hop_list), 0)

    def test_delete_hop_record(self):
        self.client.post(
            '/beerdb/add/hops/',
            data={
                'name': 'Northern',
                'min_alpha_acid': 18.00,
                'max_alpha_acid': 12.00,
                'country': 'USA',
                'comments': 'Very bitter, not good for aroma'
            })

        hop_instance = Hop.objects.filter(name='Northern')[0]

        self.assertEqual(hop_instance.name, 'Northern')

        response = self.client.get('/beerdb/delete/%d/hops/' % hop_instance.id)

        self.assertEqual(response.status_code, 200)

        response = self.client.post('/beerdb/delete/%d/hops/' % hop_instance.id)

        self.assertEqual(response.status_code, 302)

        hop_list = Hop.objects.filter(name='Northern')

        self.assertEqual(len(hop_list), 0)

    def test_add_hop_uses_item_form(self):

        response = self.client.get('/beerdb/add/hops/')
        self.assertIsInstance(response.context['form'], HopForm)

    def test_blank_input_on_addhops_page_returns_hopslist_page_with_errors(self):
        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = ''
        request.POST['min_alpha_acid'] = ''
        request.POST['max_alpha_acid'] = ''
        request.POST['country'] = 'USA'
        request.POST['comments'] = ''

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

    def test_invalid_input_on_addhops_page_returns_hopslist_page_with_errors(self):
        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'test'
        request.POST['min_alpha_acid'] = 'bad value'
        request.POST['max_alpha_acid'] = 'another bad value'
        request.POST['country'] = 'USA'
        request.POST['comments'] = 'stuffs'

        response = addhops(request)

        self.assertEqual(response.status_code, 200)
        min_alpha_acid_error = escape("This field requires a decimal number")
        max_alpha_acid_error = escape("This field requires a decimal number")

        self.assertContains(response, min_alpha_acid_error)
        self.assertContains(response, max_alpha_acid_error)

    def test_blank_input_on_update_hops_page_returns_hopslist_page_with_errors(self):
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


class TestGrainsPageView(TestCase):

    def test_grains_page_returns_correct_template(self):
        response = self.client.get('/beerdb/grains/')
        self.assertTemplateUsed(response, 'homebrewdatabase/grains.html')

    def test_can_add_new_grain_and_save_a_POST_request(self):
        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'Carared'
        request.POST['degrees_lovibond'] = 1.5
        request.POST['specific_gravity'] = 120.00
        request.POST['grain_type'] = 'GRN'
        request.POST['comments'] = 'Amber red color'

        addgrains(request)

        new_grain = Grain.objects.first()

        self.assertEqual(new_grain.name, 'Carared')
        self.assertAlmostEqual(new_grain.degrees_lovibond, 1.50)
        self.assertEqual(new_grain.specific_gravity, 120.00)
        self.assertEqual(new_grain.grain_type, 'GRN')
        self.assertEqual(new_grain.comments, 'Amber red color')

    def test_add_grains_redirects_after_POST(self):
        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'Carared'
        request.POST['degrees_lovibond'] = 1.5
        request.POST['specific_gravity'] = 120.00
        request.POST['grain_type'] = 'GRN'
        request.POST['comments'] = 'Amber red color'

        response = addgrains(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/beerdb/grains/')

    def test_add_grain_page_only_saves_when_necessary(self):
        request = HttpRequest()
        addgrains(request)
        self.assertEqual(Grain.objects.count(), 0)

    def test_grains_page_displays_all_hops_records(self):
        Grain.objects.create(name='Carared',
                             degrees_lovibond=1.50,
                             specific_gravity=120.00,
                             grain_type='GRN',
                             comments='Amber red color'
                             )

        Grain.objects.create(name='Pale Chocolate',
                             degrees_lovibond='150.00',
                             specific_gravity='12.00',
                             grain_type='GRN',
                             comments='Dark malt that gives a rich red or brown color'
                             )

        request = HttpRequest()
        response = grains(request)

        self.assertIn('Carared', response.content.decode())
        self.assertIn('Pale Chocolate', response.content.decode())

    def test_add_grains_view_saves_record(self):
        response = self.client.post(
            '/beerdb/add/grains/',
            data={
                'name': 'Carared',
                'degrees_lovibond': 1.50,
                'specific_gravity': 120.00,
                'grain_type': 'GRN',
                'comments': 'Amber red color'
            })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/beerdb/grains/')

        grain_record = Grain.objects.filter(name='Carared')

        self.assertEqual(grain_record[0].name, 'Carared')

    def test_can_update_grain(self):
        self.client.post(
            '/beerdb/add/grains/',
            data={
                'name': 'Carared',
                'degrees_lovibond': 24.00,
                'specific_gravity': 32.00,
                'grain_type': 'GRN',
                'comments': 'Adds reddish brown color'
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
        self.client.post(
            '/beerdb/add/grains/',
            data={'name': 'Munich Malt',
                  'degrees_lovibond': 10.00,
                  'specific_gravity': 1.20,
                  'grain_type': 'LME',
                  'comments': 'Sweet, toasted flavor and aroma'
                  })

        grain_instance = Grain.objects.filter(name='Munich Malt')[0]

        self.assertEqual(grain_instance.name, 'Munich Malt')

        response = self.client.get('/beerdb/delete/%s/grains/' % grain_instance.id)

        self.assertEqual(response.status_code, 200)

        response = self.client.post('/beerdb/delete/%s/grains/' % grain_instance.id)

        self.assertEqual(response.status_code, 302)

        grains_list = Grain.objects.filter(name='Munich Malt')

        self.assertEqual(len(grains_list), 0)
