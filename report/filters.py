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

    other = {'style': 'background-color: rgba(187, 191, 204, 0.2); border-color: transparent; box-shadow: 0 0 5px rgba(0, 0, 0, 0.2); color: #6c757d; height: 40px; border-radius: 5px;'}
    other_line = {'style': 'background-color: rgba(187, 191, 204, 0.2); border-color: transparent; box-shadow: 0 0 5px rgba(0, 0, 0, 0.2); color: #6c757d; height: 40px; border-radius: 5px;'}
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
            if user.role == 'Technicien':
                self.filters['state'].field.choices = [choice for choice in self.filters['state'].field.choices if choice[0] in 
                                        ['Confirmé', 'Validé', 'Refusé']]
            elif user.role == 'Nouveau':
                self.filters['state'].field.choices = [choice for choice in self.filters['state'].field.choices if choice[0] not in 
                                        ['Brouillon', 'Confirmé', 'Validé', 'Refusé', 'Annulé']]
            self.filters['usine'].queryset = user.usines.all()

