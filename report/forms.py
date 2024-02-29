from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import *
from django.utils import timezone
from django.db.models import Q

def getAttrs(type, placeholder='', other={}):
    ATTRIBUTES = {
        'control': {'class': 'form-control', 'style': 'background-color: #e0e5f5;', 'placeholder': ''},
        'search': {'class': 'form-control form-input', 'style': 'background-color: rgba(202, 207, 215, 0.5); box-shadow: 0 0 6px rgba(0, 0, 0, 0.2); color: #45558a; height: 40px; text-indent: 33px; border-radius: 5px;', 'type': 'search', 'placeholder': '', 'id': 'search'},
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
        fields = ['designation', 'code', 'usine', 'header', 'sequence', 'active']

    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Designation')))    
    code = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Code')))    
    usine = forms.ModelChoiceField(queryset=Usine.objects.all(), widget=forms.Select(attrs= getAttrs('select')), empty_label="Usine")
    header = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Header')))    
    sequence = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','Séquence')))
    active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'type': 'checkbox', 'data-onstyle':'secondary', 'data-toggle':'switchbutton',  'data-onlabel': "Active", 'data-offlabel': "Unactive"}))

class FournisseurForm(ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['designation']

    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control', 'Désignation')))

class SableTypeForm(ModelForm):
    class Meta:
        model = SableType
        fields = ['designation']

    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control', 'Désignation')))

class StandardForm(ModelForm):
    class Meta:
        model = Standard
        fields = ['poste', 'active', 'max_2_5_value', 'max_1_25_value', 'max_0_6_value', 'max_0_3_value', 'max_0_06_value', 'max_0_value', 
                  'min_2_5_value', 'min_1_25_value', 'min_0_6_value', 'min_0_3_value', 'min_0_06_value', 'min_0_value']

    poste = forms.ModelChoiceField(queryset=Poste.objects.all(), widget=forms.Select(attrs= getAttrs('select')), empty_label="Poste")
    active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'type': 'checkbox', 'data-onstyle':'secondary', 'data-toggle':'switchbutton'}))
    max_2_5_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Max 2,5mm')))
    max_1_25_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Max 1,25mm')))
    max_0_6_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Max 0,6mm')))
    max_0_3_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Max 0,3mm')))
    max_0_06_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Max 0,063mm')))
    max_0_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Max 0 (<63µm)')))
    min_2_5_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Min 2,5mm')))
    min_1_25_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Min 1,25mm')))
    min_0_6_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Min 0,6mm')))
    min_0_3_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Min 0,3mm')))
    min_0_06_value = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Min 0,063mm')))
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
        fields = ['n_report', 'n_lot', 'usine', 'shift', 'gp_user', 'date_prelev', 'type_sable', 'fournisseur', 'variateur', 'debit', 't_consigne', 't_real', 
                  'freq_b1', 'variateur_b1', 'freq_b2', 'variateur_b2', 'freq_b3', 'variateur_b3', 'retour_2_5', 'retour_1_3', 'retour_0_6', 'observation']
                

    n_report = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','N° Rapport')))
    n_lot = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','N° Lot')))
    usine = forms.ModelChoiceField(queryset=Usine.objects.all(), widget=forms.Select(attrs= getAttrs('select')), empty_label="Usine")
    shift = forms.ModelChoiceField(queryset=Horaire.objects.all(), widget=forms.Select(attrs= getAttrs('select')), empty_label="Horaire")
    gp_user = forms.ModelChoiceField(queryset=User.objects.filter(role='Gestionnaire de production'), widget=forms.Select(attrs=getAttrs('select2')), empty_label="Gestionnaire de production")
    date_prelev = forms.DateTimeField(initial=timezone.now().date(), widget=forms.widgets.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs= getAttrs('datetime')))
    type_sable = forms.ModelChoiceField(queryset=SableType.objects.all(), widget=forms.Select(attrs= getAttrs('select2')), empty_label="Type de Sable")
    fournisseur = forms.ModelChoiceField(queryset=Fournisseur.objects.all(), widget=forms.Select(attrs= getAttrs('select2')), empty_label="Fournisseur")
    variateur = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Variateur (%)')))
    debit = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Débit (t/h)')))
    t_consigne = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','T consigne (˚C)')))
    t_real = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','T réelle (˚C)')))
    freq_b1 = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Fréquence (HZ) B1')))
    variateur_b1 = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Variateur B1 (%)')))
    freq_b2 = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Fréquence (HZ) B2')))
    variateur_b2 = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Variateur B2 (%)')))
    freq_b3 = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Fréquence (HZ) B3')), required=False)
    variateur_b3 = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Variateur B3 (%)')), required=False)
    retour_2_5 = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'type': 'checkbox', 'data-onstyle':'primary', 'data-toggle':'switchbutton',  'data-onlabel': "Oui", 'data-offlabel': "Non"}))
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
    
    def clean(self):
        cleaned_data = super().clean()
        n_report = cleaned_data.get('n_report')
        usine = cleaned_data.get('usine')
        date_prelev = cleaned_data.get('date_prelev')

        if n_report and n_report != 0 and usine:
            if self.instance.pk:
                existing_report = Report.objects.filter(n_report=n_report, usine=usine, date_prelev__year=date_prelev.year).exclude( Q(id=self.instance.pk) | Q(state='Annulé')).exists()
            else:
                existing_report = Report.objects.filter(n_report=n_report, usine=usine, date_prelev__year=date_prelev.year).exclude(state='Annulé').exists()
            if n_report and n_report != 0 and usine:
                if existing_report:
                    self.add_error('n_report', 'Un rapport avec ce numéro existe déjà pour cette usine.')

        return cleaned_data


class SampleForm(ModelForm):
    class Meta:
        model = Sample
        fields = ['poste', 'value_2_5', 'value_1_25', 'value_0_6', 'value_0_3', 'value_0_06', 'value_0', 'value_h']

    min_max = {'max': '100', 'min': '0', 'step': '0.001'}
    
    poste = forms.ModelChoiceField(label = 'Poste', queryset=Poste.objects.all(), widget=forms.Select(attrs=getAttrs('select2')), empty_label="Poste")
    value_2_5 = forms.FloatField(label = '2,5mm', widget=forms.NumberInput(attrs= getAttrs('control','2,5mm', min_max)), required=True)
    value_1_25 = forms.FloatField(label = '1,25mm', widget=forms.NumberInput(attrs= getAttrs('control','1,25mm', min_max)), required=True)
    value_0_6 = forms.FloatField(label = '0,6mm', widget=forms.NumberInput(attrs= getAttrs('control','0,6mm', min_max)), required=True)
    value_0_3 = forms.FloatField(label = '0,3mm', widget=forms.NumberInput(attrs= getAttrs('control','0,3mm', min_max)), required=True)
    value_0_06 = forms.FloatField(label = '0,063mm', widget=forms.NumberInput(attrs= getAttrs('control','0,063mm', min_max)), required=False)
    value_0 = forms.FloatField(label = '0 (<63µm)', widget=forms.NumberInput(attrs= getAttrs('control','0 (<63µm)', min_max)), required=True)
    value_h = forms.FloatField(label = 'Humidité (%)', widget=forms.NumberInput(attrs= getAttrs('control','Humidité (%)', min_max)), required=True)
        
    def __init__(self, *args, **kwargs):
        poste = kwargs.pop('poste', None)
        super(SampleForm, self).__init__(*args, **kwargs)
        if poste:
            self.fields['poste'].initial = poste
        self.fields['poste'].widget.attrs['disabled'] = True


SamplesFormSet = inlineformset_factory(Report, Sample, form=SampleForm, fields=['poste', 'value_2_5', 'value_1_25', 'value_0_6', 'value_0_3', 'value_0_06', 'value_0', 'value_h'], extra=0)
