from django import forms
from django.conf import settings

from .models import Challenge, Solution
from main.utils import encrypt

class ChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        exclude = ('id', )

class SolutionForm(forms.ModelForm):
    solution_token = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Solution
        widgets = {'challenge_id': forms.HiddenInput(),
                   'author': forms.HiddenInput()}
        exclude = ('id', )

    def clean_solution_token(self):
        token = self.cleaned_data.get('solution_token')
        user = self.cleaned_data.get('author')
        user_id = user.id if user else ''
        challenge_id = self.cleaned_data.get('challenge_id')

        if token != encrypt(challenge_id + user_id):
            raise forms.ValidationError('Incorrect solution token!')

        return token
