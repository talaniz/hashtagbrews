from django import forms

from homebrewdatabase.models import Hop, Grain


class HopForm(forms.models.ModelForm):

    class Meta:
        model = Hop
        fields = ('name', 'min_alpha_acid', 'max_alpha_acid', 'country', 'comments',)
        widgets = {
            'name': forms.fields.TextInput(attrs={'id': 'new_hops'}),
            'min_alpha_acid': forms.fields.TextInput(attrs={'id': 'min_alpha_acid'}),
            'max_alpha_acid': forms.fields.TextInput(attrs={'id': 'max_alpha_acid'}),
            'comments': forms.fields.TextInput(attrs={'id': 'comments'}),
        }

        error_messages = {
            'name': {'required': 'A hop name is required'},
            'min_alpha_acid': {'required': 'You must enter a min alpha acid',
                               'invalid': 'This field requires a decimal number'},
            'max_alpha_acid': {'required': 'You must enter a max alpha acid',
                               'invalid': 'This field requires a decimal number'},
            'country': {'required': 'You must enter a country'},
            'comments': {'required': 'You must enter a comment'}
        }
    # TODO: Adjust error messages from min/max alpha acid to "{{ field name}} must be a decimal number"


class GrainForm(forms.models.ModelForm):

    class Meta:
        model = Grain
        fields = ('name', 'degrees_lovibond', 'specific_gravity', 'grain_type', 'comments')

        widgets = {
            'name': forms.fields.TextInput(attrs={'id': 'name'}),
            'degrees_lovibond': forms.fields.TextInput(attrs={'id': 'degrees_lovibond'}),
            'specific_gravity': forms.fields.TextInput(attrs={'id': 'specific_gravity'}),
            'comments': forms.fields.TextInput(attrs={'id': 'comments'})
        }

        error_messages = {
            'name': {'required': 'A grain name is required'},
            'degrees_lovibond': {'required': 'You must specify degrees lovibond',
                                 'invalid': 'Degrees lovibond must be a decimal number'},
            'specific_gravity': {'required': 'You must enter a specific gravity',
                                 'invalid': 'Specific gravity must be a decimal number'},
            'comments': {'required': 'You must leave a comment'}
        }
