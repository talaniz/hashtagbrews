from django import forms

from homebrewdatabase.models import Hop


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
