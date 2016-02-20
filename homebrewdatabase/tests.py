import unittest

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from .views import index, homebrewmain


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

    @unittest.skip('Not ready to test')
    def test_hops_page_returns_correct_template(self):
        request = HttpRequest()
        response = hops(request)
        expected_html = render_to_string('homebrewdatabase/hops.html')
        self.assertEqual(response.content.decode(), expected_html)

    @unittest.skip('Not ready to test')
    def test_can_add_new_hops_and_save(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['hops_name'] = 'Amarillo'

        response = HttpRequest(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Amarillo', response.content.decode())
