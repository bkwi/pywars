from django import forms

from .models import Challenge, Solution

class ChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        #fiels = ('first_name', 'last_name', 'phone', 'notes', 'office')
        exclude = ('id', )

class SolutionForm(forms.ModelForm):

    class Meta:
        model = Solution
        widgets = {'challenge_id': forms.HiddenInput(),
                   'author': forms.HiddenInput()}
        exclude = ('id', )
