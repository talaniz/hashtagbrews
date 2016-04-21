from django.test import TestCase

from homebrewdatabase.forms import HopForm, GrainForm


class HopFormTest(TestCase):

    def test_form_returns_correct_elements(self):
        form = HopForm()

        form_elements = ['name="name"', 'id="new_hops"', 'name="min_alpha_acid"',
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
            ['Min alpha acid must be a decimal number']
        )

        self.assertEqual(
            hop_form.errors['max_alpha_acid'],
            ['Max alpha acid must be a decimal number a decimal number']
        )

        # TODO: add validation for unique hops name


class GrainFormTest(TestCase):

    def test_grain_form_returns_correct_elements(self):
        form = GrainForm()

        form_elements = ['name="name"', 'id="name"', 'id="degrees_lovibond"', 'name="degrees_lovibond"',
                         'id="id_grain_type"', 'name="grain_type"', 'id="comments"', 'name="comments"'
                         ]

        for element in form_elements:
            self.assertIn(element, form.as_p())

    def test_grain_form_validates_blank_input(self):
        grain_form = GrainForm(data={'name': '',
                                     'degrees_lovibond': '',
                                     'specific_gravity': '',
                                     'comments': ''
                                     })

        self.assertFalse(grain_form.is_valid())

        self.assertEqual(
            grain_form.errors['name'],
            ["A grain name is required"]
        )

        self.assertEqual(
            grain_form.errors['degrees_lovibond'],
            ['You must specify degrees lovibond']
        )

        self.assertEqual(
            grain_form.errors['specific_gravity'],
            ['You must enter a specific gravity']
        )

        self.assertEqual(
            grain_form.errors['comments'],
            ['You must leave a comment']
        )

    def test_grain_form_validates_incorrect_input(self):
        grain_form = GrainForm(data={'name': 'Amber Pale',
                                     'degrees_lovibond': 'ninety three',
                                     'specific_gravity': 'seventy one',
                                     'grain_type': 'LME',
                                     'comments': 'Gives an amber color'
                                     })

        self.assertFalse(grain_form.is_valid())

        self.assertEqual(
            grain_form.errors['degrees_lovibond'],
            ['Degrees lovibond must be a decimal number']
        )

        self.assertEqual(
            grain_form.errors['specific_gravity'],
            ['Specific gravity must be a decimal number']
        )
