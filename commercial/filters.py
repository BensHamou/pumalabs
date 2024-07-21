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

    search = CharFilter(method='filter_search', widget=forms.TextInput(attrs=getAttrs('search', 'Rechercher Réclamation..')))

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(emplacement_designation__icontains=value) | Q(emplacement_region__icontains=value)).distinct()

    class Meta:
        model = Complaint
        fields = ['search']