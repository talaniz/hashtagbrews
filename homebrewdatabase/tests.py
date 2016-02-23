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

    def test_hops_url_returns_correct_template(self):
        test_client = Client()
        response = test_client.get('http://localhost:8000/beerdb/hops/')
        self.assertTemplateUsed('hops.html')

    def test_can_add_new_hops_and_save(self):
        request = HttpRequest()

        request.method = 'POST'
        request.POST['hops_name'] = 'Amarillo'
        request.POST['min_alpha_acid'] = '8.00'
        request.POST['max_alpha_acid'] = '11.00'
        request.POST['countries'] = 'USA'
        request.POST['comments'] = 'Good over all aroma and bittering hops'

        response = hops(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Amarillo', response.content.decode())
        self.assertIn('8.00', response.content.decode())
        self.assertIn('11.00', response.content.decode())
        self.assertIn('USA', response.content.decode())
        self.assertIn('Good over all aroma and bittering hops', response.content.decode())

        expected_html = render_to_string(
            'homebrewdatabase/hops.html',
            {'new_hops_name': 'Amarillo',
             'min_alpha_acid': '8.00',
             'max_alpha_acid': '11.00',
             'countries': 'USA',
             'comments': 'Good over all aroma and bittering hops'},
            request=request
        )

        self.assertIn(response.content.decode(), expected_html)

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

        '''Class representing a hops profile.

       Contains the following attributes:
       x -name: name of the hop strain
       x -min_alpha_acid: lowest alpha acid for hop range
       x -max_alpha_acid: highest alpha acid for hop range
       x -origin: country of origin, DEFAULT = USA
           x -country codes: [AUS, CAN, CHN, CZE, FRA, DEU, NZL, POL, GBR, USA]
       -comments: final notes about the hop profile
    '''