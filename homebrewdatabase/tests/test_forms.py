from django.test import TestCase

from homebrewdatabase.forms import HopForm


class HopFormTest(TestCase):

    def test_form_returns_correct_elements(self):
        form = HopForm()

        form_elements = ['name="name', 'id="new_hops"', 'name="min_alpha_acid"',
                         'id="min_alpha_acid', 'name="max_alpha_acid"',
                         'id="max_alpha_acid"', 'name="country"',
                         'id="comments"', 'name="comments'
                         ]

        for element in form_elements:
            self.assertIn(element, form.as_p())
