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


class StandardForm(ModelForm):
    class Meta:
        model = Standard
        fields = '__all__'


    poste = forms.ModelChoiceField(queryset=Usine.objects.all(), widget=forms.Select(attrs= getAttrs('select')), empty_label="Usine")
    active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'type': 'checkbox', 'data-onstyle':'secondary', 'data-toggle':'switchbutton'}))
    max_2_5_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Max 2,5mm')))
    max_1_25_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Max 1,25mm')))
    max_0_6_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Max 0,6mm')))
    max_0_3_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Max 0,3mm')))
    max_0_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Max 0 (<63µm)')))
    min_2_5_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Min 2,5mm')))
    min_1_25_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Min 1,25mm')))
    min_0_6_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Min 0,6mm')))
    min_0_3_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Min 0,3mm')))
    min_0_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Min 0 (<63µm)')))


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
    