from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from .views import index, homebrewmain, hops

from .models import Hop


class TestViewHomePage(TestCase):

    def test_homepage_returns_correct_template(self):
        request = HttpRequest()
        response = index(request)
        expected_html = render_to_string('homebrewdatabase/index.html')
        self.assertEqual(response.content.decode(), expected_html)


class TestOpenSourceBeerDataBase(TestCase):

    def test_main_page_returns_correct_template(self):
        request = HttpRequest()
        response = homebrewmain(request)
        expected_html = render_to_string('homebrewdatabase/homebrewdatabase.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_can_add_new_hops_and_save_a_POST_request(self):
        request = HttpRequest()

        request.method = 'POST'
        request.POST['hops_name'] = 'Amarillo'
        request.POST['min_alpha_acid'] = 8.00
        request.POST['max_alpha_acid'] = 11.00
        request.POST['countries'] = 'USA'
        request.POST['comments'] = 'Good over all aroma and bittering hops'

        response = hops(request)

        self.assertEqual(Hop.objects.count(), 1)

        new_hop = Hop.objects.first()

        self.assertEqual(new_hop.name, 'Amarillo')
        self.assertAlmostEqual(new_hop.min_alpha_acid, 8.00)
        self.assertEqual(new_hop.max_alpha_acid, 11.00)
        self.assertEqual(new_hop.country, 'USA')
        self.assertEqual(new_hop.comments, 'Good over all aroma and bittering hops')

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()

        request.method = 'POST'
        request.POST['hops_name'] = 'Amarillo'
        request.POST['min_alpha_acid'] = 8.00
        request.POST['max_alpha_acid'] = 11.00
        request.POST['countries'] = 'USA'
        request.POST['comments'] = 'Good over all aroma and bittering hops'

        response = hops(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/beerdb/hops')

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

    def test_can_update_hops(self):
        request = HttpRequest()
        response = updatehops(request, '1')

        hop_record = response.context['hop']

        self.assertEqual(hop_record.name, 'Amarillo')

        hop_record.comments = 'This has been changed'

        request.method = 'POST'
        request.POST['hops_name'] = hop_record.name
        request.POST['min_alpha_acid'] = hop.min_alpha_acid
        request.POST['max_alpha_acid'] = hop.max_alpha_acid
        request.POST['countries'] = 'USA'
        request.POST['comments'] = hop_record.comments

        response = updatehops(request, 1)

        self.assertEqual(response.status_code, 302)
        self.assertIn('This has been changed' , response.content.decode())