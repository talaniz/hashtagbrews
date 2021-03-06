from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from elasticsearch import Elasticsearch

from homebrewdatabase.models import Hop, Grain, Yeast


class HopModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email="antonio.alaniz@gmail.com",
                                             password='testpassword')
        self.es_client = Elasticsearch()
        call_command('push_hop_to_index')

    def tearDown(self):
        call_command('push_hop_to_index')

    def test_saving_items_and_retrieving_later(self):
        """
        Asserts that a user can successfully enter and retrieve a hop record using the Hop model
                :return: pass or fail
        """

        first_hop = Hop()
        first_hop.user = self.user
        first_hop.name = 'Amarillo'
        first_hop.min_alpha_acid = '8.00'
        first_hop.max_alpha_acid = '11.00'
        first_hop.country = 'USA'
        first_hop.comments = 'Pretty good, all around'
        first_hop.save()

        second_hop = Hop()
        second_hop.user = self.user
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

        self.assertEqual(first_saved_hop.user.username, 'testuser')
        self.assertEqual(first_saved_hop.name, 'Amarillo')
        self.assertEqual(first_saved_hop.min_alpha_acid, 8.00)
        self.assertEqual(first_saved_hop.max_alpha_acid, 11.00)
        self.assertEqual(first_saved_hop.country, 'USA')
        self.assertEqual(first_saved_hop.comments, 'Pretty good, all around')

        self.assertEqual(second_saved_hop.user.username, 'testuser')
        self.assertEqual(second_saved_hop.name, 'Chinook')
        self.assertEqual(second_saved_hop.min_alpha_acid, 12.00)
        self.assertEqual(second_saved_hop.max_alpha_acid, 14.00)
        self.assertEqual(second_saved_hop.country, 'USA')
        self.assertEqual(second_saved_hop.comments, 'Good for bittering, not great for aroma')

        first_es_hop_record = self.es_client.get_source(index="hop", doc_type="hop", id=first_hop.id)
        second_es_hop_record = self.es_client.get_source(index="hop", doc_type="hop", id=second_hop.id)

        # Elasticsearch returns string types even on floats and ints so
        # we check against string values
        self.assertEqual(first_es_hop_record['user'], 'testuser')
        self.assertEqual(first_es_hop_record['name'], 'Amarillo')
        self.assertEqual(first_es_hop_record['min_alpha_acid'], '8.00')
        self.assertEqual(first_es_hop_record['max_alpha_acid'], '11.00')
        self.assertEqual(first_es_hop_record['country'], 'USA')
        self.assertEqual(first_es_hop_record['comments'], 'Pretty good, all around')

        self.assertEqual(second_es_hop_record['user'], 'testuser')
        self.assertEqual(second_es_hop_record['name'], 'Chinook')
        self.assertEqual(second_es_hop_record['min_alpha_acid'], '12.00')
        self.assertEqual(second_es_hop_record['max_alpha_acid'], '14.00')
        self.assertEqual(second_es_hop_record['country'], 'USA')
        self.assertEqual(second_es_hop_record['comments'], 'Good for bittering, not great for aroma')


class GrainModelTest(TestCase):
    """
    Tests the ability to save and retrieve data using the Grain model
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email="antonio.alaniz@gmail.com",
                                             password='testpassword')
        self.es_client = Elasticsearch()
        call_command('push_grain_to_index')

    def tearDown(self):
        call_command('push_grain_to_index')

    def test_saving_grain_and_retrieving_later(self):
        """
        Asserts that a user can successfully enter and retrieve a hop record using the Grain model
                :return: pass or fail
        """

        first_grain = Grain()
        first_grain.user = self.user
        first_grain.name = 'Cara Red'
        first_grain.degrees_lovibond = '1.5'
        first_grain.specific_gravity = '1.000'
        first_grain.grain_type = 'GRN'
        first_grain.comments = 'Amber red color'
        first_grain.save()

        second_grain = Grain()
        second_grain.user = self.user
        second_grain.name = "Pale Chocolate"
        second_grain.degrees_lovibond = "150.00"
        second_grain.specific_gravity = "12.000"
        second_grain.grain_type = 'GRN'
        second_grain.comments = 'Dark malt that gives a rich red or brown color'
        second_grain.save()

        saved_grains = Grain.objects.all()
        self.assertEqual(saved_grains.count(), 2)

        first_saved_grain = saved_grains[0]
        second_saved_grain = saved_grains[1]

        self.assertEqual(first_saved_grain.user.username, 'testuser')
        self.assertEqual(first_saved_grain.name, 'Cara Red')
        self.assertEqual(first_saved_grain.degrees_lovibond, 1.50)
        self.assertEqual(first_saved_grain.specific_gravity, 1.000)
        self.assertEqual(first_saved_grain.grain_type, 'GRN')
        self.assertEqual(first_saved_grain.comments, 'Amber red color')

        self.assertEqual(second_saved_grain.user.username, 'testuser')
        self.assertEqual(second_saved_grain.name, 'Pale Chocolate')
        self.assertEqual(second_saved_grain.degrees_lovibond, 150.00)
        self.assertEqual(second_saved_grain.specific_gravity, 12.000)
        self.assertEqual(second_saved_grain.grain_type, 'GRN')
        self.assertEqual(second_saved_grain.comments, 'Dark malt that gives a rich red or brown color')

        first_es_grain_record = self.es_client.get_source(index="grain", doc_type="grain", id=first_grain.id)
        second_es_grain_record = self.es_client.get_source(index="grain", doc_type="grain", id=second_grain.id)

        self.assertEqual(first_es_grain_record['user'], 'testuser')
        self.assertEqual(first_es_grain_record['name'], 'Cara Red')
        self.assertEqual(first_es_grain_record['degrees_lovibond'], '1.5')
        self.assertEqual(first_es_grain_record['specific_gravity'], '1.000')
        self.assertEqual(first_es_grain_record['grain_type'], 'GRN')
        self.assertEqual(first_es_grain_record['comments'], 'Amber red color')

        self.assertEqual(second_es_grain_record['user'], 'testuser')
        self.assertEqual(second_es_grain_record['name'], 'Pale Chocolate')
        self.assertEqual(second_es_grain_record['degrees_lovibond'], '150.00')
        self.assertEqual(second_es_grain_record['specific_gravity'], '12.000')
        self.assertEqual(second_es_grain_record['grain_type'], 'GRN')
        self.assertEqual(second_es_grain_record['comments'], 'Dark malt that gives a rich red or brown color')


class YeastModelTest(TestCase):
    """
    Tests the ability to save and retrieve data using the Yeast model
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email="antonio.alaniz@gmail.com",
                                             password='testpassword')
        self.es_client = Elasticsearch()
        call_command('push_yeast_to_index')

    def tearDown(self):
        call_command('push_yeast_to_index')

    def test_saving_yeast_and_retrieving_later(self):
        """
        Asserts that a user can successfully enter and retrieve a hop record using the Yeast model
                :return: pass or fail
        """

        first_yeast = Yeast()
        first_yeast.user = self.user
        first_yeast.name = 'Alpine'
        first_yeast.lab = 'Wyeast'
        first_yeast.yeast_type = 'Ale'
        first_yeast.yeast_form = 'Liquid'
        first_yeast.min_temp = '60'
        first_yeast.max_temp = '70'
        first_yeast.attenuation = '75'
        first_yeast.flocculation = 'Medium'
        first_yeast.comments = 'Well balanced.'
        first_yeast.save()

        second_yeast = Yeast()
        second_yeast.user = self.user
        second_yeast.name = 'American Ale 1056'
        second_yeast.lab = 'Wyeast'
        second_yeast.yeast_type = 'Ale'
        second_yeast.yeast_form = 'Liquid'
        second_yeast.min_temp = '60'
        second_yeast.max_temp = '72'
        second_yeast.attenuation = '75'
        second_yeast.flocculation = 'Low'
        second_yeast.comments = 'Well balanced. Ferments dry, finishes soft.'
        second_yeast.save()

        saved_yeasts = Yeast.objects.all()
        first_yeast_record = saved_yeasts[0]
        second_yeast_record = saved_yeasts[1]

        self.assertEqual(first_yeast_record.user.username, 'testuser')
        self.assertEqual(first_yeast_record.name, 'Alpine')
        self.assertEqual(first_yeast_record.lab, 'Wyeast')
        self.assertEqual(first_yeast_record.yeast_type, 'Ale')
        self.assertEqual(first_yeast_record.yeast_form, 'Liquid')
        self.assertEqual(first_yeast_record.min_temp, 60)
        self.assertEqual(first_yeast_record.max_temp, 70)
        self.assertEqual(first_yeast_record.attenuation, 75)
        self.assertEqual(first_yeast_record.flocculation, 'Medium')
        self.assertEqual(first_yeast.comments, 'Well balanced.')

        self.assertEqual(second_yeast_record.user.username, 'testuser')
        self.assertEqual(second_yeast_record.name, 'American Ale 1056')
        self.assertEqual(second_yeast_record.lab, 'Wyeast')
        self.assertEqual(second_yeast_record.yeast_type, 'Ale')
        self.assertEqual(second_yeast_record.yeast_form, 'Liquid')
        self.assertEqual(second_yeast_record.min_temp, 60)
        self.assertEqual(second_yeast_record.max_temp, 72)
        self.assertEqual(second_yeast_record.attenuation, 75)
        self.assertEqual(second_yeast_record.flocculation, 'Low')
        self.assertEqual(second_yeast_record.comments, 'Well balanced. Ferments dry, finishes soft.')

        first_es_yeast_record = self.es_client.get_source(index="yeast", doc_type="yeast", id=first_yeast.id)
        second_es_yeast_record = self.es_client.get_source(index="yeast", doc_type="yeast", id=second_yeast.id)

        self.assertEqual(first_es_yeast_record['user'], 'testuser')
        self.assertEqual(first_es_yeast_record['name'], 'Alpine')
        self.assertEqual(first_es_yeast_record['lab'], 'Wyeast')
        self.assertEqual(first_es_yeast_record['yeast_type'], 'Ale')
        self.assertEqual(first_es_yeast_record['yeast_form'], 'Liquid')
        self.assertEqual(first_es_yeast_record['min_temp'], '60')
        self.assertEqual(first_es_yeast_record['max_temp'], '70')
        self.assertEqual(first_es_yeast_record['attenuation'], '75')
        self.assertEqual(first_es_yeast_record['flocculation'], 'Medium')
        self.assertEqual(first_es_yeast_record['comments'], 'Well balanced.')

        self.assertEqual(second_es_yeast_record['user'], 'testuser')
        self.assertEqual(second_es_yeast_record['name'], 'American Ale 1056')
        self.assertEqual(second_es_yeast_record['lab'], 'Wyeast')
        self.assertEqual(second_es_yeast_record['yeast_type'], 'Ale')
        self.assertEqual(second_es_yeast_record['yeast_form'], 'Liquid')
        self.assertEqual(second_es_yeast_record['min_temp'], '60')
        self.assertEqual(second_es_yeast_record['max_temp'], '72')
        self.assertEqual(second_es_yeast_record['attenuation'], '75')
        self.assertEqual(second_es_yeast_record['flocculation'], 'Low')
        self.assertEqual(second_es_yeast_record['comments'], 'Well balanced. Ferments dry, finishes soft.')
