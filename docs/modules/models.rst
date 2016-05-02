Models
======

.. module:: homebrewdatabase.models

.. autoclass:: Hop()
    :members:

    Contains the following attributes:
           | -name: name of the hop strain
           | -min_alpha_acid: lowest alpha acid for hop range
           | -max_alpha_acid: highest alpha acid for hop range
           | -origin: country of origin, DEFAULT = USA
           | -country codes: AUS, CAN, CHN, CZE, FRA, DEU, NZL, POL, GBR, USA
           | -comments: final notes about the hop profile

.. autoclass:: Grain()
    :members:

    Contains the following attributes:
           | -name: name of the malt
           | -degrees_lovibond: SRM/color measurement
           | -grain_type: Grain, LME, DME or Adjunct
           | -specific_gravity: SG, measurement for converted sugars
           | -grain_type: Grain (GRN), Liquid Malt Extract (LME), Dry Malt Extract) DME, (Adjunct) ADJ
           | -comments: final comments about the malt

