from django.test import TestCase

from homebrewdatabase.forms import HopForm, GrainForm, YeastForm


class HopFormTest(TestCase):
    """
    Test model for all tests related to HopForm
    """

    def test_form_returns_correct_elements(self):
        """
        This test makes sure that the form elements contain the correct html names and IDs
                :return: pass or fail
        """

        form = HopForm()

        form_elements = ['name="name"', 'id="new_hops"', 'name="min_alpha_acid"',
                         'id="min_alpha_acid', 'name="max_alpha_acid"',
                         'id="max_alpha_acid"', 'name="country"',
                         'id="comments"', 'name="comments', 'class="form-control"'
                         ]

        for element in form_elements:
            self.assertIn(element, form.as_p())

    def test_form_validates_blank_input(self):
        """
        Test to check that the HopForm provides validation errors for blank items
                :return: pass or fail
        """

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
        """
        Test to ensure that the HopForm provides the correct validation error messages when invalid input is submitted
                :return: pass or fail
        """

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
            ['Max alpha acid must be a decimal number']
        )

        # TODO: add validation for unique hops name


class GrainFormTest(TestCase):
    """
    Test model for all tests related to the GrainForm
    """

    def test_grain_form_returns_correct_elements(self):
        """
        Test checks that the Grain is rendered with the correct html id's and names
                :return: pass or fail
        """

        form = GrainForm()

        form_elements = ['name="name"', 'id="name"', 'id="degrees_lovibond"', 'name="degrees_lovibond"',
                         'id="id_grain_type"', 'name="grain_type"', 'id="comments"', 'name="comments"',
                         'class="form-control"'
                         ]

        for element in form_elements:
            self.assertIn(element, form.as_p())

    def test_grain_form_validates_blank_input(self):
        """
        Test to check that the GrainForm returns the correction validation input with blank data
                :return: pass or fail
        """

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
        """
        Test to check that the GrainForm returns invalid submissions with the correct validation errors
                :return: pass or fail
        """

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


class YeastFormTest(TestCase):
    """
    Test model for all tests related to YeastForm
    """

    def test_form_returns_correct_elements(self):
        """
        Checks that all form elements contain the correct html names and Ids
                :return: pass or fail
        """

        form = YeastForm()

        form_elements = ['name="name"', 'id="name"', 'id="lab', 'id="yeast_type"', 'id="yeast_form"',
                         'id="min_temp', 'id="max_temp"', 'id="attenuation"', 'id="flocculation"', 'id="comments"',
                         'class="form-control"']

        for element in form_elements:
            self.assertIn(element, form.as_p())

    def test_yeast_form_validates_blank_input(self):
        """
        Test to check that the YeastForm returns the correction validation input with blank data
                :return: pass or fail
        """

        yeast_form = YeastForm(data={'name': '',
                                     'lab': 'Brewferm',
                                     'yeast_type': 'Ale',
                                     'yeast_form': 'Liquid',
                                     'min_temp': '',
                                     'max_temp': '',
                                     'attenuation': '',
                                     'flocculation': 'Medium',
                                     'comments': ''})

        self.assertEqual(yeast_form.errors['name'],
                         ["A yeast name is required"]
                         )

        self.assertEqual(yeast_form.errors['min_temp'],
                         ["You must enter a min temp"]
                         )

        self.assertEqual(yeast_form.errors['max_temp'],
                         ["You must enter a max temp"]
                         )

        self.assertEqual(yeast_form.errors['attenuation'],
                         ["You must enter an attenuation"]
                         )

        self.assertEqual(yeast_form.errors['comments'],
                         ["You must enter a comment"]
                         )

    def test_yeast_form_validates_invalid_input(self):
        """
        Test to check that the YeastForm validates invalid input with the correct error messages.
                :return: pass or fail
        """

        yeast_form = YeastForm(data={'name': 'WLP0065 Ale Yeast',
                                     'lab': 'Brewferm',
                                     'yeast_type': 'Ale',
                                     'yeast_form': 'liquid',
                                     'min_temp': 'eighty eight',
                                     'max_temp': 'nintety three',
                                     'attenuation': 'twenty seven',
                                     'flocculation': 'Medium',
                                     'comments': 'Testing'})

        self.assertEqual(yeast_form.errors['min_temp'],
                         ["Min temp must be a number"]
                         )

        self.assertEqual(yeast_form.errors['max_temp'],
                         ["Max temp must be a number"]
                         )

        self.assertEqual(yeast_form.errors['attenuation'],
                         ["Attenuation must be a number"])