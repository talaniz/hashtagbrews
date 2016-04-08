from django.db import models
from django.core.urlresolvers import reverse


class Hop(models.Model):

    name = models.CharField(max_length=200, default='')
    min_alpha_acid = models.DecimalField(max_digits=4, decimal_places=2)
    max_alpha_acid = models.DecimalField(max_digits=4, decimal_places=2)

    # Country codes for origin (as defined by http://countrycode.org)
    AUSTRALIA = 'AUS'
    CANADA = 'CAN'
    CHINA = 'CHN'
    CZECH_REPUBLIC = 'CZE'
    FRANCE = 'FRA'
    GERMANY = 'DEU'
    NEW_ZEALAND = 'NZL'
    POLAND = 'POL'
    UNITED_KINGDOM = 'GBR'
    UNITED_STATES = 'USA'

    COUNTRY_CODES = (
        (AUSTRALIA, 'Australia'),
        (CANADA, 'Canada'),
        (CHINA, 'China'),
        (CZECH_REPUBLIC, 'Czech Republic'),
        (FRANCE, 'France'),
        (GERMANY, 'Germany'),
        (NEW_ZEALAND, 'New Zealand'),
        (POLAND, 'Poland'),
        (UNITED_KINGDOM, 'United Kingdom'),
        (UNITED_STATES, 'United States'),
    )

    country = models.CharField(max_length=3,
                               choices=COUNTRY_CODES,
                               default=UNITED_STATES
                               )

    comments = models.TextField(default='')

    def get_absolute_url(self):
        return reverse('updatehops', kwargs={'pk': self.id})


class Grain(models.Model):

    name = models.CharField(max_length=200, default='')
    degrees_lovibond = models.DecimalField("Degrees (L)", max_digits=5, decimal_places=2)
    specific_gravity = models.DecimalField(max_digits=6, decimal_places=3)

    GRAIN = 'GRN'
    LIQUID_EXTRACT = 'LME'
    DRY_EXTRACT = 'DME'
    ADJUNCT = 'ADJ'

    MALT_FORMS = (
        (GRAIN, 'Grain'),
        (LIQUID_EXTRACT, 'Liquid Malt Extract'),
        (DRY_EXTRACT, 'Dry Malt Extract'),
        (ADJUNCT, 'Adjuncts'),
    )

    grain_type = models.CharField(max_length=3,
                                 choices=MALT_FORMS,
                                 default=LIQUID_EXTRACT)

    comments = models.TextField(default='')
