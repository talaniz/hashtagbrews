Models
======

.. module:: homebrewdatabase.models

.. autoclass:: Hop()
    :members:

    Contains the following attributes:
           | -name: name of the hop strain
           | -min_alpha_acid: lowest alpha acid for hop range
           | -max_alpha_acid: highest alpha acid for hop range
           | -origin: country of origin, choices=COUNTRY_CODES, default=USA
           | -comments: final notes about the hop profile

    * Dropdown Menus
            * COUNTRY_CODES: AUS, CAN, CHN, CZE, FRA, DEU, NZL, POL, GBR, USA

.. autoclass:: Grain()
    :members:

    Contains the following attributes:
           | -name: name of the malt
           | -degrees_lovibond: SRM/color measurement
           | -specific_gravity: SG, measurement for converted sugars
           | -grain_type: choices=MALT_FORMS
           | -comments: final comments about the malt

    * Dropdown Menus
            * MALT_FORMS: Grain (GRN), Liquid Malt Extract (LME), Dry Malt Extract) DME, (Adjunct) ADJ

.. autoclass:: Yeast()
    :members:

    Contains the following attributes:
           | -name: char, name of the yeast
           | -lab: max_length=4, choices=YEAST_LAB_CHOICES, default=Wylabs
           | -yeast_type: max_length=3, choices=YEAST_TYPE_CHOICES, default=ale
           | -yeast_form: max_length=3, choices=YEAST_FORM_CHOICES, default=liquid
           | -min_temp: integer, minimum effective temperature for yeast, fahrenheit
           | -max_temp: integer, maximum effective temperature for yeast, fahrenheit
           | -attenuation: decimal, max_length=3, decimal_places = 2, % of sugars yeast will consume
           | -flocculation: max_length=3, choices=YEAST_FLOCCULATION_CHOICES, default=medium
           | -comments: text field, final comments about the yeast profile

    * Dropdown Menus
            * YEAST_LAB_CHOICES: Wylabs, Wyeast, DCL/Fermentis, East Coast Yeast, The Yeast Bay, Coopers, Brewferm, Danstar, Doric,Edme, Glenbrew, Lallemend, Munton Fison, Red Star, Brewtek
            * YEAST_TYPE_CHOICES: ale, champagne, lager, wheat, wine
            * YEAST_FORM_CHOICES:liquid, dry
            * YEAST_FLOCCULATION_CHOICES: low, medium, high, very high