from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Login')
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    password1 = forms.CharField(label='password')
    password2 = forms.CharField(label='repeat password')


    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        lables = {
            'first_name': 'First name',
            'last_name': 'Last name',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Password not match')
        return cd['password1']