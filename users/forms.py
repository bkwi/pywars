from django import forms

from users.models import AppUser
# from django.utils.translation import ugettext, ugettext_lazy as _


class RegisterUserForm(forms.ModelForm):
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = AppUser
        fields = ['email', 'name', 'password']
        widgets = {'password': forms.PasswordInput()}

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match',
                                        code='invalid')
        return password2


class UserSettingsForm(forms.ModelForm):

    class Meta:
        model = AppUser
        fields = ['name', 'email']

