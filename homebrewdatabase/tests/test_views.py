from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from homebrewdatabase.models import Hop
from homebrewdatabase.views import index, hops, addhops, updatehops


class TestHomePage(TestCase):

    def test_homepage_returns_correct_template(self):
        request = HttpRequest()
        response = index(request)
        expected_html = render_to_string('homebrewdatabase/index.html')
        self.assertEqual(response.content.decode(), expected_html)


class TestHopsPage(TestCase):

    def test_can_add_new_hops_and_save_a_POST_request(self):
        request = HttpRequest()

        request.method = 'POST'
        request.POST['name'] = 'Amarillo'
        request.POST['min_alpha_acid'] = 8.00
        request.POST['max_alpha_acid'] = 11.00
        request.POST['country'] = 'USA'
        request.POST['comments'] = 'Good over all aroma and bittering hops'

        response = addhops(request)

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