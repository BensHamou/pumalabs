from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import *
from django.utils import timezone
from django.db.models import Q

def getAttrs(type, placeholder='', other={}):
    ATTRIBUTES = {
        'control': {'class': 'form-control', 'style': 'background-color: #e0e5f5;', 'placeholder': ''},
        'search': {'class': 'form-control form-input', 'style': 'background-color: rgba(202, 207, 215, 0.5); box-shadow: 0 0 6px rgba(0, 0, 0, 0.2); color: #f2f2f2; height: 40px; text-indent: 33px; border-radius: 5px;', 'type': 'search', 'placeholder': '', 'id': 'search'},
        'select': {'class': 'form-select', 'style': 'background-color: #e0e5f5;'},
        'select2': {'class': 'form-select custom-select', 'style': 'background-color: #e0e5f5; width: 100%;'},
        'date': {'type': 'date', 'class': 'form-control dateinput','style': 'background-color: #e0e5f5;'},
        'datetime': {'type': 'datetime-local', 'class': 'form-control dateinput','style': 'background-color: #e0e5f5;'},
        'textarea': {"rows": "3", 'style': 'width: 100%', 'class': 'form-control', 'placeholder': '', 'style': 'background-color: #e0e5f5;'}
    }

    
    if type in ATTRIBUTES:
        attributes = ATTRIBUTES[type]
        if 'placeholder' in attributes:
            attributes['placeholder'] = placeholder
        if other:
            attributes.update(other)
        return attributes
    else:
        return {}

class PosteForm(ModelForm):
    class Meta:
        model = Poste
        fields = ['designation', 'usine', 'active']

    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Designation')))    
    usine = forms.ModelChoiceField(queryset=Usine.objects.all(), widget=forms.Select(attrs= getAttrs('select')), empty_label="Usine")
    active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'type': 'checkbox', 'data-onstyle':'secondary', 'data-toggle':'switchbutton',  'data-onlabel': "Active", 'data-offlabel': "Unactive"}))

class StandardForm(ModelForm):
    class Meta:
        model = Standard
        fields = ['poste', 'active', 'max_2_5_value', 'max_1_25_value', 'max_0_6_value', 'max_0_3_value', 'max_0_value', 'min_2_5_value', 'min_1_25_value', 
                  'min_0_6_value', 'min_0_3_value', 'min_0_value']

    poste = forms.ModelChoiceField(queryset=Poste.objects.all(), widget=forms.Select(attrs= getAttrs('select')), empty_label="Poste")
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
        
    def __init__(self, *args, **kwargs):
        poste = kwargs.pop('poste', None)
        super(StandardForm, self).__init__(*args, **kwargs)
        if poste:
            self.fields['poste'].initial = poste
        self.fields['poste'].widget.attrs['disabled'] = True
    
class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['n_report', 'usine', 'shift', 'date_prelev', 'type_sable', 'variateur', 'debit', 't_consigne', 't_real', 
                  'freq_b1', 'freq_b2', 'retour_1_3', 'retour_0_6', 'observation']
                

    n_report = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','N° Rapport')))
    usine = forms.ModelChoiceField(queryset=Usine.objects.all(), widget=forms.Select(attrs= getAttrs('select')), empty_label="Usine")
    shift = forms.ModelChoiceField(queryset=Horaire.objects.all(), widget=forms.Select(attrs= getAttrs('select')), empty_label="Horaire")
    date_prelev = forms.DateTimeField(initial=timezone.now().date(), widget=forms.widgets.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs= getAttrs('datetime')))
    type_sable = forms.ChoiceField(choices=Report.SAND_TYPE, widget=forms.Select(attrs=getAttrs('select')))
    variateur = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Variateur (%)')))
    debit = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Débit (t/h)')))
    t_consigne = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','T consigne (˚C)')))
    t_real = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','T réelle (˚C)')))
    freq_b1 = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Fréquence (HZ) B1')))
    freq_b2 = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Fréquence (HZ) B2')))
    retour_1_3 = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'type': 'checkbox', 'data-onstyle':'primary', 'data-toggle':'switchbutton',  'data-onlabel': "Oui", 'data-offlabel': "Non"}))
    retour_0_6 = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'type': 'checkbox', 'data-onstyle':'primary', 'data-toggle':'switchbutton',  'data-onlabel': "Oui", 'data-offlabel': "Non"}))
    observation = forms.CharField(widget=forms.Textarea(attrs= getAttrs('textarea','Observation')), required=False)

    def __init__(self, *args, **kwargs):
        admin = kwargs.pop('admin', None)
        usines = kwargs.pop('usines', None)
        state = kwargs.pop('state', None)
        super(ReportForm, self).__init__(*args, **kwargs)
        if usines is not None:
            self.fields['usine'].queryset = usines
            self.fields['usine'].initial = usines.first()
            if not admin and len(usines) < 2:
                self.fields['usine'].widget.attrs['disabled'] = True


class SampleForm(ModelForm):
    class Meta:
        model = Sample
        fields = ['poste', 'value_2_5', 'value_1_25', 'value_0_6', 'value_0_3', 'value_0', 'value_h']
    
    poste = forms.ModelChoiceField(label = 'Poste', queryset=Poste.objects.all(), widget=forms.Select(attrs=getAttrs('select2')), empty_label="Poste")
    value_2_5 = forms.FloatField(label = '2,5mm', widget=forms.NumberInput(attrs= getAttrs('control','2,5mm')))
    value_1_25 = forms.FloatField(label = '1,25mm', widget=forms.NumberInput(attrs= getAttrs('control','1,25mm')))
    value_0_6 = forms.FloatField(label = '0,6mm', widget=forms.NumberInput(attrs= getAttrs('control','0,6mm')))
    value_0_3 = forms.FloatField(label = '0,3mm', widget=forms.NumberInput(attrs= getAttrs('control','0,3mm')))
    value_0 = forms.FloatField(label = '0 (<63µm)', widget=forms.NumberInput(attrs= getAttrs('control','0 (<63µm)')))
    value_h = forms.FloatField(label = 'Humidité (%)', widget=forms.NumberInput(attrs= getAttrs('control','Humidité (%)')))
        
    def __init__(self, *args, **kwargs):
        poste = kwargs.pop('poste', None)
        super(SampleForm, self).__init__(*args, **kwargs)
        if poste:
            self.fields['poste'].initial = poste
        self.fields['poste'].widget.attrs['disabled'] = True


SamplesFormSet = inlineformset_factory(Report, Sample, form=SampleForm, fields=['poste', 'value_2_5', 'value_1_25', 'value_0_6', 'value_0_3', 'value_0', 'value_h'], extra=0)
