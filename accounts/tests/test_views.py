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

    def pre_login_check(self, model):
        """Check that modal links aren't showing in each list view."""

        # FIXME: Grains model needs to be updated to use plural
        # otherwise it has to check for which model and provide the match string
        if model == 'grains':
            add_match = '#deletegrain'
            update_match = '#updategrain'
            delete_match = '#addgrain'
        else:
            add_match = '#delete{}'
            update_match = '#update{}'
            delete_match = '#add{}'

        response = self.client.get('/beerdb/{}/'.format(model))
        self.assertIn('Login', response.content.decode())
        self.assertNotIn('testuser', response.content.decode())
        self.assertNotIn(delete_match.format(model), response.content.decode())
        self.assertNotIn(update_match.format(model), response.content.decode())
        self.assertNotIn(add_match.format(model), response.content.decode())

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
        self.pre_login_check('hops')
        self.pre_login_check('grains')
        self.pre_login_check('yeasts')

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

        response = self.client.get('/beerdb/hops/')
        self.assertIn('#addhops', response.content.decode())

    def test_login_page_redirects_to_next(self):
        """`login` view should auth & redir to the next url if specified."""
        self.pre_login_check('hops')

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
