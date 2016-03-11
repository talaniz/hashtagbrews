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

    def test_form_validates_blank_input(self):
        hop_form = HopForm(data={
            'name': '',
            'min_alpha_acid': '',
            'max_alpha_acid': '',
            'country': '',
            'comments': ''
        })

        self.assertFalse(hop_form.is_valid())

        self.assertEqual(
            hop_form.errors['name'],
            ["A hop name is required"]
        )

        self.assertEqual(
            hop_form.errors['min_alpha_acid'],
            ["You must enter a min alpha acid"]
        )

        self.assertEqual(
            hop_form.errors['max_alpha_acid'],
            ["You must enter a max alpha acid"]
        )

        self.assertEqual(
            hop_form.errors['country'],
            ["You must enter a country"]
        )

        self.assertEqual(
            hop_form.errors['comments'],
            ['You must enter a comment']
        )

    def test_form_validates_incorrect_input(self):
        hop_form = HopForm(data={
            'name': 'Chinook',
            'min_alpha_acid': 'str',
            'max_alpha_acid': 'str',
            'country': 'USA',
            'comments': 'Great for testing'
        })

        self.assertFalse(hop_form.is_valid())

        self.assertEqual(
            hop_form.errors['min_alpha_acid'],
            ['This field requires a decimal number']
        )

        self.assertEqual(
            hop_form.errors['max_alpha_acid'],
            ['This field requires a decimal number']
        )
