from django import forms
from django.db.models import Q
from django_filters import FilterSet, CharFilter, ChoiceFilter, ModelChoiceFilter, DateFilter
from .models import *
from report.forms import getAttrs

class ProductFilter(FilterSet):

    search = CharFilter(method='filter_search', widget=forms.TextInput(attrs=getAttrs('search', 'Rechercher Produit..')))

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(designation__icontains=value)).distinct()

    class Meta:
        model = Product
        fields = ['search']
        
class EmplacementFilter(FilterSet):

    search = CharFilter(method='filter_search', widget=forms.TextInput(attrs=getAttrs('search', 'Rechercher Emplacement..')))

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(designation__icontains=value) |Q(region__icontains=value)).distinct()

    class Meta:
        model = Emplacement
        fields = ['search']
        
class ComplaintFilter(FilterSet):

    other = {'style': 'background-color: rgba(202, 207, 215, 0.5); box-shadow: 0 0 6px rgba(0, 0, 0, 0.2); color: #45558a; height: 40px; border-radius: 5px;'}

    search = CharFilter(method='filter_search', widget=forms.TextInput(attrs=getAttrs('search', 'Rechercher Réclamation..')))
    state = ChoiceFilter(choices=Complaint.STATE_COMPLAINT, widget=forms.Select(attrs=getAttrs('select', other=other)), empty_label="État")
    usine = ModelChoiceFilter(queryset=Usine.objects.all(), widget=forms.Select(attrs= getAttrs('select', other=other)), empty_label="Usine")

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(emplacement_designation__icontains=value) | Q(emplacement_region__icontains=value) | Q(pk__icontains=value) | 
                                Q(product__icontains=value) | Q(n_lot__icontains=value) | Q(n_bc__icontains=value) | 
                                Q(distributeur__icontains=value) | Q(client__icontains=value)).distinct()

    class Meta:
        model = Complaint
        fields = ['search', 'state', 'usine']