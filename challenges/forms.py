from django import forms

from .models import Challenge

class ChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        #fiels = ('first_name', 'last_name', 'phone', 'notes', 'office')
        exclude = ('id', )
