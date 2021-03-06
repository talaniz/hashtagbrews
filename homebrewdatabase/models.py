from django.conf import settings
from django.urls import reverse
from django.db import models

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient


class Hop(models.Model):
    """Class representing a hops profile."""

    # This allows for customizing the user model later, the AUTH_USER_MODEL just
    # needs to be defined in settings.py
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
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

    def save(self, *args, **kwargs):
        es_client = Elasticsearch()
        es_index_client = IndicesClient(client=es_client)
        super(Hop, self).save(*args, **kwargs)
        if self.pk is not None:
            es_client.index(
                index="hop",
                doc_type="hop",
                id=self.pk,
                body={
                      'user': self.user.username,
                      'name': self.name,
                      'min_alpha_acid': self.min_alpha_acid,
                      'max_alpha_acid': self.max_alpha_acid,
                      'country': self.country,
                      'comments': self.comments
                      },
                refresh=True
            )
        else:
            es_client.create(
                index="hop",
                doc_type="hop",
                id=self.pk,
                body={'user': self.user.username,
                      'name': self.name,
                      'min_alpha_acid': self.min_alpha_acid,
                      'max_alpha_acid': self.max_alpha_acid,
                      'country': self.country,
                      'comments': self.comments
                      },
                refresh=True
            )

    def delete(self, *args, **kwargs):
        es_client = Elasticsearch()
        hop_id = self.pk
        super(Hop, self).delete(*args, **kwargs)
        es_client.delete(
                index="hop",
                doc_type="hop",
                id=hop_id,
                refresh=True
        )


class Grain(models.Model):
    """Class representing the general profile of a malt."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
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

    def save(self, *args, **kwargs):
        es_client = Elasticsearch()
        es_index_client = IndicesClient(client=es_client)
        super(Grain, self).save(*args, **kwargs)
        if self.pk is not None:
            es_client.index(
                index="grain",
                doc_type="grain",
                id=self.pk,
                body={
                    'user': self.user.username,
                    'name': self.name,
                    'degrees_lovibond': self.degrees_lovibond,
                    'specific_gravity': self.specific_gravity,
                    'grain_type': self.grain_type,
                    'comments': self.comments
                    },
                refresh=True
            )
        else:
            es_client.create(
                index="grain",
                doc_type="grain",
                id=self.pk,
                body={
                    'user': self.user.username,
                    'name': self.name,
                    'degrees_lovibond': self.degrees_lovibond,
                    'specific_gravity': self.specific_gravity,
                    'grain_type': self.grain_type,
                    'comments': self.comments
                    },
                refresh=True
            )

    def delete(self, *args, **kwargs):
        es_client = Elasticsearch()
        grain_id = self.pk
        super(Grain, self).delete(*args, **kwargs)
        es_client.delete(
                index="grain",
                doc_type="grain",
                id=grain_id,
                refresh=True
        )


class Yeast(models.Model):
    """Class representing a yeast profile."""

    # YEAST_LAB_CHOICES
    BREWFERM = 'Brewferm'
    BREWTEK = 'Brewtek'
    COOPERS = 'Coopers'
    DANSTAR = 'Danstar'
    DCL_FERMENTIS = 'DCL/Fermentis'
    DORIC = 'Doric'
    EAST_COAST_YEAST = 'East Coast Yeast'
    EDME = 'Edme'
    GLENBREW = 'Glenbrew'
    LALLEMEND = 'Lallemend'
    MUNTON_FISON = 'Munton Fison'
    RED_STAR = 'Red Star'
    WHITE_LABS = 'White Labs'
    WYEAST = 'Wyeast'
    WYLABS = 'Wylabs'
    YEAST_BAY = 'Yeast Bay'

    # YEAST_TYPE_CHOICES
    ALE = 'Ale'
    CHAMPAGNE = 'Champagne'
    LAGER = 'Lager'
    SAISON = 'Saison'
    WHEAT = 'Wheat'
    WINE = 'Wine'

    # YEAST_FORM_CHOICES
    LIQUID = 'Liquid'
    DRY = 'Dry'

    # YEAST_FLOCCULATION_CHOICES
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    VERY_HIGH = 'Very High'

    YEAST_LAB_CHOICES = (
        (BREWFERM, 'Brewferm'),
        (BREWTEK, 'Brewtek'),
        (COOPERS, 'Coopers'),
        (DANSTAR, 'Danstar'),
        (DCL_FERMENTIS, 'DCL/Fermentis'),
        (DORIC, 'Doric'),
        (EAST_COAST_YEAST, 'East Coast Yeast'),
        (EDME, 'Edme'),
        (GLENBREW, 'Glenbrew'),
        (LALLEMEND, 'Lallemend'),
        (MUNTON_FISON, 'Munton Fison'),
        (RED_STAR, 'Red Star'),
        (WHITE_LABS, 'White Labs'),
        (WYEAST, 'Wyeast'),
        (WYLABS, 'Wylabs'),
        (YEAST_BAY, 'The Yeast Bay'),
    )

    YEAST_TYPE_CHOICES = (
        (ALE, 'Ale'),
        (CHAMPAGNE, 'Champagne'),
        (LAGER, 'Lager'),
        (SAISON, 'Saison'),
        (WHEAT, 'Wheat'),
        (WINE, 'Wine'),
    )

    YEAST_FORM_CHOICES = (
        (LIQUID, 'Liquid'),
        (DRY, 'Dry'),
    )

    YEAST_FLOCCULATION_CHOICES = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
        (VERY_HIGH, 'Very high'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    name = models.CharField(max_length=200, unique=True)
    lab = models.CharField(max_length=20, choices=YEAST_LAB_CHOICES, default=WYLABS)
    yeast_type = models.CharField(max_length=15, choices=YEAST_TYPE_CHOICES, default=ALE)
    yeast_form = models.CharField(max_length=10, choices=YEAST_FORM_CHOICES, default=LIQUID)
    min_temp = models.IntegerField()
    max_temp = models.IntegerField()
    attenuation = models.IntegerField()
    flocculation = models.CharField(max_length=15, choices=YEAST_FLOCCULATION_CHOICES, default=MEDIUM)
    comments = models.TextField()

    def save(self, *args, **kwargs):
        es_client = Elasticsearch()
        es_index_client = IndicesClient(client=es_client)
        super(Yeast, self).save(*args, **kwargs)
        if self.pk is not None:
            es_client.index(
                index="yeast",
                doc_type="yeast",
                id=self.pk,
                body={
                    'user': self.user.username,
                    'name': self.name,
                    'lab': self.lab,
                    'yeast_type': self.yeast_type,
                    'yeast_form': self.yeast_form,
                    'min_temp': self.min_temp,
                    'max_temp': self.max_temp,
                    'attenuation': self.attenuation,
                    'flocculation': self.flocculation,
                    'comments': self.comments
                    },
                refresh=True
            )
        else:
            es_client.create(
                index="yeast",
                doc_type="yeast",
                id=self.pk,
                body={
                    'user': self.user.username,
                    'name': self.name,
                    'lab': self.lab,
                    'yeast_type': self.yeast_type,
                    'yeast_form': self.yeast_form,
                    'min_temp': self.min_temp,
                    'max_temp': self.max_temp,
                    'attenuation': self.attenuation,
                    'flocculation': self.flocculation,
                    'comments': self.comments
                },
                refresh=True
            )

    def delete(self, *args, **kwargs):
        es_client = Elasticsearch()
        yeast_id = self.pk
        super(Yeast, self).delete(*args, **kwargs)
        es_client.delete(
            index="yeast",
            doc_type="yeast",
            id=yeast_id,
            refresh=True
        )

    def __unicode__(self):
        return self.name
