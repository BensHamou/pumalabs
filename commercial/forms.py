from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import *
from django.utils import timezone
from django.db.models import Q
from report.forms import getAttrs


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Designation')))

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Designation')))

class EmplacementForm(ModelForm):
    class Meta:
        model = Emplacement
        fields = '__all__'
    
    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Désignation')))
    region = forms.ChoiceField(choices=Emplacement.REGION, widget=forms.Select(attrs=getAttrs('select')))

class ComplaintCommForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['creator', 'distributeur_id', 'distributeur', 'client_id', 'client', 'categ_client', 'emplacement', 'product', 
                  'usine', 'project', 'n_bc', 'n_lot', 'qte', 'date_delivery', 'date_prod', 'observation',
                  'treatment_labo', 'treatment_labo_att', 'treatment_site', 'treatment_site_att', 'actions', 'decision']
    
    creator = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs= getAttrs('select2')), empty_label="Commercial")
    
    distributeur_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlID','ID_dist_id')))
    distributeur = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch','Distributeur')))

    client_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlID','ID_client_id')))
    client = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch','Client')))

    emplacement = forms.ModelChoiceField(queryset=Emplacement.objects.all(), widget=forms.Select(attrs= getAttrs('select2')), empty_label="Site")
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs= getAttrs('select2')), empty_label="Produit")
    usine = forms.ModelChoiceField(queryset=Usine.objects.all(), widget=forms.Select(attrs= getAttrs('select2')), empty_label="Usine")
    categ_client = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs= getAttrs('select2')), empty_label="Catégorie Client")

    project = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Projet')))
    n_bc = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','N° BC')))
    n_lot = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','N° Lot')))
    qte = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','Quantité')))

    date_delivery = forms.DateField(initial=timezone.now().date(), widget=forms.widgets.DateInput(attrs= getAttrs('date'), format='%Y-%m-%d'))
    date_prod = forms.DateField(initial=timezone.now().date(), widget=forms.widgets.DateInput(attrs= getAttrs('date'), format='%Y-%m-%d'))

    observation = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textarea','Description')), required=False)
    treatment_labo = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textarea2','Traitement de la Réclamation Au Laboratoire')), required=False)
    treatment_labo_att = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input', 'accept': '.zip,.pdf,.doc,.docx,.jpg,.jpeg,.png'}), required=False)
    treatment_site = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textarea2','Traitement de la Réclamation sur Site')), required=False)
    treatment_site_att = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input', 'accept': '.zip,.pdf,.doc,.docx,.jpg,.jpeg,.png'}), required=False)
    actions = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textarea2','Actions à mettre en œuvre')), required=False)
    decision = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textarea2','Décision final')), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ComplaintCommForm, self).__init__(*args, **kwargs)
        self.fields['creator'].initial = user
        if not user.role == 'Admin':
            self.fields['creator'].widget.attrs['disabled'] = True
    

class ComplaintResponsableForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['treatment_labo', 'treatment_labo_att', 'treatment_site', 'treatment_site_att', 'actions']
    
    treatment_labo = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textarea2','Traitement de la Réclamation Au Laboratoire')))
    treatment_site = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textarea2','Traitement de la Réclamation sur Site')))
    treatment_labo_att = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input', 'accept': '.zip,.pdf,.doc,.docx,.jpg,.jpeg,.png'}), required=False)
    treatment_site_att = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input', 'accept': '.zip,.pdf,.doc,.docx,.jpg,.jpeg,.png'}), required=False)
    actions = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textarea2','Actions à mettre en œuvre')))

class ComplaintDirectorForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['decision']

    decision = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textarea2','Décision final')))

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['image']

    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input','accept': 'image/*'}))