from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import Client, TestCase

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


class HopModelTest(TestCase):

    def test_saving_items_and_retrieving_later(self):
        first_hop = Hop()
        first_hop.name = 'Amarillo'
        first_hop.min_alpha_acid = '8.00'
        first_hop.max_alpha_acid = '11.00'
        first_hop.country = 'USA'
        first_hop.comments = 'Pretty good, all around'
        first_hop.save()

        second_hop = Hop()
        second_hop.name = 'Chinook'
        second_hop.min_alpha_acid = '12.00'
        second_hop.max_alpha_acid = '14.00'
        second_hop.country = 'USA'
        second_hop.comments = 'Good for bittering, not great for aroma'
        second_hop.save()

        saved_hops = Hop.objects.all()
        self.assertEqual(saved_hops.count(), 2)

        first_saved_hop = saved_hops[0]
        second_saved_hop = saved_hops[1]
        self.assertEqual(first_saved_hop.name, 'Amarillo')
        self.assertEqual(first_saved_hop.min_alpha_acid, 8.00)
        self.assertEqual(first_saved_hop.max_alpha_acid, 11.00)
        self.assertEqual(first_saved_hop.country, 'USA')
        self.assertEqual(first_saved_hop.comments, 'Pretty good, all around')

        self.assertEqual(second_saved_hop.name, 'Chinook')
        self.assertEqual(second_saved_hop.min_alpha_acid, 12.00)
        self.assertEqual(second_saved_hop.max_alpha_acid, 14.00)
        self.assertEqual(second_saved_hop.country, 'USA')
        self.assertEqual(second_saved_hop.comments, 'Good for bittering, not great for aroma')
