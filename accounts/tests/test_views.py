from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from accounts.forms import LoginForm
from accounts.views import login


class TestLoginPage(TestCase):
    """Class for testing the login views."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email="antonio.alaniz@gmail.com",
                                             password='testpassword')

    def test_login_returns_correct_template(self):
        """Login view should return login.html.
                :return: pass or fail
        """
        response = self.client.get('/accounts/login/')
        self.assertTemplateUsed(response, template_name='accounts/login.html')

    def test_login_page_uses_login_form(self):
        """`accounts/login` should use an instance of `LoginForm`"""
        response = self.client.get('/accounts/login/')
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_login_page_auths_on_POST(self):
        """`login` view should auth & redir to the homebrew db page."""
        response = self.client.get('/beerdb/hops/')
        self.assertIn('Login', response.content.decode())
        self.assertNotIn('testuser', response.content.decode())

        response = self.client.login(username='testuser', password='testpassword')
        self.assertEqual(response, True)

        response = self.client.post(
            '/accounts/login/',
            data={
                'username': 'testuser',
                'password': 'testpassword',
                'next': ''
            }, follow=True)

        self.assertEqual(response.status_code, 200, msg="Status:{}\nResponse Text: {}".format(response.status_code,
                                                                                              response.content))
        self.assertIn('Homebrew Materials Database', response.content.decode())
        self.assertIn('testuser', response.content.decode())

    def test_login_page_redirects_to_next(self):
        """`login` view should auth & redir to the next url if specified."""
        response = self.client.get('/beerdb/hops/')
        self.assertIn('Login', response.content.decode())
        self.assertNotIn('testuser', response.content.decode())

        response = self.client.post(
            '/accounts/login/',
            data={
                'username': 'testuser',
                'password': 'testpassword',
                'next': reverse('index')
            }, follow=True)

        self.assertEqual(response.status_code, 200, msg="Status:{}\nResponse Text: {}".format(response.status_code,
                                                                                              response.content))
        self.assertIn('#Hashtag Brews', response.content.decode())
        self.assertIn('testuser', response.content.decode())
