from unittest import skip

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase

from elasticsearch import Elasticsearch

from accounts.forms import LoginForm

from homebrewdatabase.models import Hop, Grain, Yeast


class TestLoginPage(TestCase):
    """Class for testing the login views."""

    def setUp(self):
        self.es_client = Elasticsearch()
        call_command('push_hop_to_index')
        call_command('push_grain_to_index')
        call_command('push_yeast_to_index')

        self.user = User.objects.create_user(username='testuser', email="antonio.alaniz@gmail.com",
                                             password='testpassword')

    def tearDown(self):
        self.es_client = Elasticsearch()
        call_command('push_hop_to_index')
        call_command('push_grain_to_index')
        call_command('push_yeast_to_index')

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

    def post_login_check(self, model):
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
        self.assertNotIn('Login', response.content.decode())
        self.assertIn('testuser', response.content.decode())
        self.assertIn(delete_match.format(model), response.content.decode())
        self.assertIn(update_match.format(model), response.content.decode())
        self.assertIn(add_match.format(model), response.content.decode())

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
        self.pre_login_check('grains')
        self.pre_login_check('yeasts')

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

    def test_add_item_after_login_adds_correctly(self):
        """`login` view should auth & redir to the next url if specified."""
        self.pre_login_check('hops')
        self.pre_login_check('grains')
        self.pre_login_check('yeasts')

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

        self.client.post(
            '/beerdb/add/hops/',
            data={
                'user': self.user,
                'name': 'Warrior',
                'min_alpha_acid': 24.00,
                'max_alpha_acid': 32.00,
                'country': 'USA',
                'comments': 'Very bitter, not good for aroma'
            })

        self.client.post(
            '/beerdb/add/grains/',
            data={
                'user': self.user,
                'name': 'Carared',
                'degrees_lovibond': 24.00,
                'specific_gravity': 32.00,
                'grain_type': 'GRN',
                'comments': 'Adds reddish brown color'
            })

        self.client.post(
            '/beerdb/add/yeasts/',
            data={'user': self.user,
                  'name': "WLP002 ENGLISH ALE YEAST",
                  'lab': "White Labs",
                  'yeast_type': "Ale",
                  'yeast_form': "Liquid",
                  'min_temp': "65",
                  'max_temp': "68",
                  'attenuation': "68",
                  'flocculation': "Very High",
                  'comments': "A classic ESB strain"})

        self.post_login_check('hops')
        self.post_login_check('grains')
        self.post_login_check('yeasts')

        hop = Hop.objects.filter(name='Warrior')
        grain = Grain.objects.filter(name='Carared')
        yeast = Yeast.objects.filter(name='WLP002 ENGLISH ALE YEAST')

        hop_user = hop[0].user
        grain_user = grain[0].user
        yeast_user = yeast[0].user

        self.assertEqual(len(hop), 1)
        self.assertEqual(len(grain), 1)
        self.assertEqual(len(yeast), 1)

        # TODO: Add a second user, make update, verify user 1 is user
        # def test_update_item_after_login_uses_same_user

        self.assertEqual(hop_user.username, 'testuser')
        self.assertEqual(grain_user.username, 'testuser')
        self.assertEqual(yeast_user.username, 'testuser')

    def test_anon_user_gets_redirect_on_add(self):
        response = self.client.get('/beerdb/add/hops/', follow=True)
        self.assertEqual(response.status_code, 200, msg="Status:{}\nResponse Text: {}".format(response.status_code,
                                                                                              response.content))
        self.assertIn('Login', response.content.decode())

        response = self.client.get('/beerdb/add/grains/', follow=True)
        self.assertEqual(response.status_code, 200, msg="Status:{}\nResponse Text: {}".format(response.status_code,
                                                                                              response.content))
        self.assertIn('Login', response.content.decode())

        response = self.client.get('/beerdb/add/yeasts/', follow=True)
        self.assertEqual(response.status_code, 200, msg="Status:{}\nResponse Text: {}".format(response.status_code,
                                                                                              response.content))
        self.assertIn('Login', response.content.decode())

    def test_user_can_logout(self):
        """User should login, add records, log out with no add or update visibility after logout."""
        """`login` view should auth & redir to the next url if specified."""
        self.pre_login_check('hops')
        self.pre_login_check('grains')
        self.pre_login_check('yeasts')

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

        self.client.post(
            '/beerdb/add/hops/',
            data={
                'user': self.user,
                'name': 'Warrior',
                'min_alpha_acid': 24.00,
                'max_alpha_acid': 32.00,
                'country': 'USA',
                'comments': 'Very bitter, not good for aroma'
            })

        self.post_login_check('hops')

        response = self.client.get('/accounts/logout/', follow=True)
        self.assertEqual(response.status_code, 200,
                         msg="Status:{}\nResponse Text: {}".format(response.status_code,
                                                                   response.content))
        self.assertIn('#Hashtag Brews', response.content.decode())
        self.assertIn('Login', response.content.decode())

        self.pre_login_check('hops')

        hop = Hop.objects.filter(name='Warrior')

        self.assertEqual(len(hop), 1)

    @skip('Need to log users out')
    def test_anon_user_gets_redirect_on_update(self):

        response = self.client.post(
            '/accounts/login/',
            data={
                'username': 'testuser',
                'password': 'testpassword',
                'next': reverse('index')
            }, follow=True)

        self.client.post(
            '/beerdb/add/hops/',
            data={
                'user': self.user,
                'name': 'Warrior',
                'min_alpha_acid': 24.00,
                'max_alpha_acid': 32.00,
                'country': 'USA',
                'comments': 'Very bitter, not good for aroma'
            })

        self.client.post(
            '/beerdb/add/grains/',
            data={
                'user': self.user,
                'name': 'Carared',
                'degrees_lovibond': 24.00,
                'specific_gravity': 32.00,
                'grain_type': 'GRN',
                'comments': 'Adds reddish brown color'
            })

        self.client.post(
            '/beerdb/add/yeasts/',
            data={'user': self.user,
                  'name': "WLP002 ENGLISH ALE YEAST",
                  'lab': "White Labs",
                  'yeast_type': "Ale",
                  'yeast_form': "Liquid",
                  'min_temp': "65",
                  'max_temp': "68",
                  'attenuation': "68",
                  'flocculation': "Very High",
                  'comments': "A classic ESB strain"})

        hop = Hop.objects.filter(name='Warrior')[0]
        grain = Grain.objects.filter(name='Carared')[0]
        yeast = Yeast.objects.filter(name='WLP002 ENGLISH ALE YEAST')[0]

        response = self.client.get('/beerdb/edit/%d/hops/' % hop.id, follow=True)
        self.assertEqual(response.status_code, 200, msg="Status:{}\nResponse Text: {}".format(response.status_code,
                                                                                              response.content))
        self.assertIn('Login', response.content.decode())

        response = self.client.get('/beerdb/edit/%d/grains/' % grain.id, follow=True)
        self.assertEqual(response.status_code, 200, msg="Status:{}\nResponse Text: {}".format(response.status_code,
                                                                                              response.content))
        self.assertIn('Login', response.content.decode())

        response = self.client.get('/beerdb/edit//%d/yeasts/' % yeast.id, follow=True)
        self.assertEqual(response.status_code, 200, msg="Status:{}\nResponse Text: {}".format(response.status_code,
                                                                                              response.content))
        self.assertIn('Login', response.content.decode())
        # self.assertTrue(False, 'Next, log the users out, then assign them as a foreign key to each model, finally,
        # remove dupes and deploy!')
