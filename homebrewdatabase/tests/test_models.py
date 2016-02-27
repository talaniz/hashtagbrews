from django.test import TestCase

from homebrewdatabase.models import Hop


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