import django_filters
from django_filters import ChoiceFilter, CharFilter, DateFilter, ModelChoiceFilter, FilterSet, DateTimeFilter
from django import forms
from .forms import getAttrs
from .models import *
from django.db.models import Q

class PosteFilter(FilterSet):

    search = CharFilter(method='filter_search', widget=forms.TextInput(attrs=getAttrs('search', 'Rechercher Emplacement..')))

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(designation__icontains=value) |
            Q(region__icontains=value)
        ).distinct()

    class Meta:
        model = Poste
        fields = ['search']

class ReportFilter(FilterSet):

    other = {'style': 'background-color: rgba(202, 207, 215, 0.5); border-color: transparent; box-shadow: 0 0 6px rgba(0, 0, 0, 0.2); color: #f2f2f2; height: 40px; border-radius: 5px;'}
    other_line = {'style': 'background-color: rgba(202, 207, 215, 0.5); border-color: transparent; box-shadow: 0 0 6px rgba(0, 0, 0, 0.2); color: #30343b; height: 40px; border-radius: 5px;'}
    search = CharFilter(method='filter_search', widget=forms.TextInput(attrs=getAttrs('search', 'Rechercher..')))
    state = ChoiceFilter(choices=Report.STATE_REPORT, widget=forms.Select(attrs=getAttrs('select')), empty_label="État")
    start_date = DateTimeFilter(field_name='date_prelev', lookup_expr='gte', widget=forms.widgets.DateTimeInput(attrs= getAttrs('date', other=other), format='%d-%m-%Y'))
    end_date = DateTimeFilter(field_name='date_prelev', lookup_expr='lte', widget=forms.widgets.DateTimeInput(attrs= getAttrs('date', other=other), format='%d-%m-%Y'))
    usine = ModelChoiceFilter(queryset=Usine.objects.all(), widget=forms.Select(attrs= getAttrs('select', other=other)), empty_label="Usine")

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(n_report__icontains=value) | 
            Q(creator__fullname__icontains=value) | 
            Q(usine__designation__icontains=value)
        ).distinct()

    class Meta:
        model = Report
        fields = ['search', 'state', 'start_date', 'end_date', 'usine']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ReportFilter, self).__init__(*args, **kwargs)
        if user:
            if user.role == 'Gestionnaire de stock':
                self.filters['state'].field.choices = [choice for choice in self.filters['state'].field.choices if choice[0] in 
                                        ['Confirmé', 'Validé par GS', 'Refusé par DI', 'Refusé par GS']]
            elif user.role == 'Directeur Industriel':
                self.filters['state'].field.choices = [choice for choice in self.filters['state'].field.choices if choice[0] in 
                                        ['Validé par GS', 'Validé par DI',  'Refusé par DI']]
            elif user.role == 'Nouveau':
                self.filters['state'].field.choices = [choice for choice in self.filters['state'].field.choices if choice[0] not in 
                                        ['Brouillon', 'Confirmé', 'Validé par GS', 'Validé par DI', 'Refusé par GS', 'Refusé par DI', 'Annulé']]
            self.filters['usine'].queryset = user.usines.all()

