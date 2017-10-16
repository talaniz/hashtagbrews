from django import forms

from homebrewdatabase.models import Hop, Grain, Yeast


class HopForm(forms.models.ModelForm):
    """
    Instance of a form used to add/edit/delete data related to hop records

            * error_messages
                - required: name, min_alpha_acid, max_alpha_acid, comments
                - invalid: name, min_alpha_acid, max_alpha_acid, country, comments
    """

    class Meta:
        model = Hop
        fields = ('name', 'min_alpha_acid', 'max_alpha_acid', 'country', 'comments',)
        widgets = {
            'name': forms.fields.TextInput(attrs={'id': 'new_hops', 'class': 'form-control'}),
            'min_alpha_acid': forms.fields.TextInput(attrs={'id': 'min_alpha_acid', 'class': 'form-control'}),
            'max_alpha_acid': forms.fields.TextInput(attrs={'id': 'max_alpha_acid', 'class': 'form-control'}),
            'country': forms.fields.Select(attrs={'class': 'form-control'}),
            'comments': forms.fields.TextInput(attrs={'id': 'comments', 'class': 'form-control'}),
        }

        error_messages = {
            'name': {'required': 'A hop name is required'},
            'min_alpha_acid': {'required': 'You must enter a min alpha acid',
                               'invalid': 'Min alpha acid must be a decimal number'},
            'max_alpha_acid': {'required': 'You must enter a max alpha acid',
                               'invalid': 'Max alpha acid must be a decimal number'},
            'country': {'required': 'You must enter a country'},
            'comments': {'required': 'You must enter a comment'}
        }


class GrainForm(forms.models.ModelForm):
    """
    Instance of a form used to add/edit/delete data related to grain records

            * error_messages
                - required: name, degrees_lovibond, specific_gravity, comments
                - invalid: derees_lovibond, specific_gravity
    """

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


class YeastForm(forms.models.ModelForm):
    """
    Instance of a form used to add/edit/delete data related to yeast records

            * error_messages
                - required: name, lab, min_temp, max_temp, attenuation, flocculation, comments
                - invalid: min_temp, max_temp, attenuation
    """

    class Meta:
        model = Yeast
        fields = ('name', 'lab', 'yeast_type', 'yeast_form', 'min_temp', 'max_temp', 'attenuation', 'flocculation',
                  'comments')

        widgets = {
            'name': forms.fields.TextInput(attrs={'id': 'name'}),
            'lab': forms.fields.Select(attrs={'id': 'lab'}),
            'yeast_type': forms.fields.Select(attrs={'id': 'yeast_type'}),
            'yeast_form': forms.fields.Select(attrs={'id': 'yeast_form'}),
            'min_temp': forms.fields.TextInput(attrs={'id': 'min_temp'}),
            'max_temp': forms.fields.TextInput(attrs={'id': 'max_temp'}),
            'attenuation': forms.fields.TextInput(attrs={'id': 'attenuation'}),
            'flocculation': forms.fields.Select(attrs={'id': 'flocculation'}),
            'comments': forms.fields.TextInput(attrs={'id': 'comments'})
        }

        error_messages = {
            'name': {'required': 'A yeast name is required'},
            'min_temp': {'required': 'You must enter a min temp',
                         'invalid': 'Min temp must be a number'},
            'max_temp': {'required': 'You must enter a max temp',
                         'invalid': 'Max temp must be a number'},
            'attenuation': {'required': 'You must enter an attenuation',
                            'invalid': 'Attenuation must be a number'},
            'comments': {'required': 'You must enter a comment'}
        }
