import unittest

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import Client, TestCase

from .views import index, homebrewmain, hops


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

        request.method == 'POST'
        request.POST['hops_name'] = 'Amarillo'

        response = hops(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Amarillo', response.content.decode())
        expected_html = render_to_string(
            'homebrewdatabase/hops.html',
            {'new_hops_name': 'Amarillo'},
            request=request
        )

        self.assertIn(response.content.decode(), expected_html)
