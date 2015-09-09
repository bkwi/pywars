from django import forms

from users.models import AppUser


class RegisterUserForm(forms.ModelForm):

    class Meta:
        model = AppUser
        fields = ['email', 'name', 'password']
        widgets = {'password': forms.PasswordInput()}

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

