from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from report.forms import getAttrs

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'fullname', 'email', 'role', 'usines', 'is_admin', 'first_name', 'last_name']

    attr = {'class': 'form-control', 'style': 'background-color: #cacfd7;', 'readonly':'readonly'}

    username = forms.CharField(widget=forms.TextInput(attrs=attr))
    last_name = forms.CharField(widget=forms.TextInput(attrs=attr))
    first_name = forms.CharField(widget=forms.TextInput(attrs=attr))

    fullname = forms.CharField(widget=forms.TextInput(attrs=attr))
    email = forms.EmailField(widget=forms.EmailInput(attrs=attr))
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select(attrs=getAttrs('select')))
    usines = forms.SelectMultiple(attrs={'class': 'form-select'})
    is_admin = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'type': 'checkbox', 'data-onstyle':'secondary', 'data-toggle':'switchbutton'}))


class HoraireForm(ModelForm):
    class Meta:
        model = Horaire
        fields = ['hour_start', 'minutes_start', 'hour_end', 'minutes_end']

    hour_start = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','H')), initial=00)
    minutes_start = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','M')), initial=00)
    hour_end = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','H')), initial=00)
    minutes_end = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','M')), initial=00)


class UsineForm(ModelForm):
    class Meta:
        model = Usine
        fields = ['designation', 'horaires', 'address']

    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control', 'Désignation')))
    address = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control', 'Address')))
    horaires = forms.SelectMultiple(attrs={'class': 'form-select'})


class CustomLoginForm(AuthenticationForm):
    
    username = forms.EmailField( label="Email", widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Mot de passe'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' not in username:
            raise forms.ValidationError(
                self.error_messages['invalid_email'],
                code='invalid_email',
            )
        return username

    error_messages = {
        'invalid_login': "Email/Mot de passe incorrect.",
        'inactive': "Ce compte est inactif.",
        'invalid_email': "S'il vous plaît, mettez une adresse email valide.",
    }
    