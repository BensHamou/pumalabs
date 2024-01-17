from django.shortcuts import render
from account.models import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.views import admin_required, Validator_required
import uuid
from .forms import *
from .filters import *
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django_filters.views import FilterView
from django.views.generic.detail import DetailView
from django.db.models import Count
from django.template.defaulttags import register
from functools import wraps
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import format_html
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import matplotlib
matplotlib.use('Agg')

def check_creator(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        report_id = kwargs.get('pk')
        report = Report.objects.get(id=report_id)
        if (report.creator != request.user or request.user.role != "Technicien") and request.user.role != 'Admin':
            return render(request, '403.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key,0)
# POSTE

@login_required(login_url='login')
@admin_required
def listPosteView(request):
    postes = Poste.objects.all().order_by('id')
    filteredData = PosteFilter(request.GET, queryset=postes)
    postes = filteredData.qs
    page_size_param = request.GET.get('page_size')
    page_size = int(page_size_param) if page_size_param else 12   
    paginator = Paginator(postes, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page, 'filtredData': filteredData, 
    }
    return render(request, 'list_postes.html', context)

@login_required(login_url='login')
@admin_required
def deletePosteView(request, id):
    poste = Poste.objects.get(id=id)
    poste.delete()
    cache_param = str(uuid.uuid4())
    url_path = reverse('postes')
    page = request.GET.get('page', '1')
    page_size = request.GET.get('page_size', '12')
    search = request.GET.get('search', '')
    redirect_url = f'{url_path}?cache={cache_param}&page={page}&page_size={page_size}&search={search}'
    return redirect(redirect_url)

@login_required(login_url='login')
@admin_required
def createPosteView(request):
    form = PosteForm()
    standard_form = StandardForm()
    if request.method == 'POST':
        form = PosteForm(request.POST)
        if form.is_valid():
            poste = form.save()
            
            standard_data = {
                'poste': poste.id, 'active': True, 'max_2_5_value': 0, 'max_1_25_value': 0,
                'max_0_6_value': 0, 'max_0_3_value': 0, 'max_0_value': 0, 'min_2_5_value': 0,
                'min_1_25_value': 0, 'min_0_6_value': 0, 'min_0_3_value': 0, 'min_0_value': 0,
            }
            standard_form = StandardForm(standard_data)
            if standard_form.is_valid():
                standard_form.save()

            cache_param = str(uuid.uuid4())
            url_path = reverse('postes')
            redirect_url = f'{url_path}?cache={cache_param}'
            return redirect(redirect_url)
    context = {'form': form}
    return render(request, 'poste_form.html', context)

@login_required(login_url='login')
@admin_required
def editPosteView(request, id):
    poste = Poste.objects.get(id=id)
    form = PosteForm(instance=poste)
    if request.method == 'POST':
        form = PosteForm(request.POST, instance=poste)
        if form.is_valid():
            form.save()
            cache_param = str(uuid.uuid4())
            url_path = reverse('postes')
            page = request.GET.get('page', '1')
            page_size = request.GET.get('page_size', '12')
            search = request.GET.get('search', '')
            redirect_url = f'{url_path}?cache={cache_param}&page={page}&page_size={page_size}&search={search}'
            return redirect(redirect_url)
    context = {'form': form, 'poste': poste}

    return render(request, 'poste_form.html', context)


#STANDARD

@login_required(login_url='login')
@admin_required
def editStandardView(request, id):
    standard = Standard.objects.get(id=id)
    form = StandardForm(instance=standard)
    if request.method == 'POST':
        form = StandardForm(request.POST, instance=standard)
        if form.is_valid():
            standard = form.save()
            if standard.active:
                related_standards = Standard.objects.filter(poste=standard.poste).exclude(pk=standard.pk)
                related_standards.update(active=False)
            elif all(not s.active for s in standard.poste.standards()):
                standard.active = True
                standard.save()
            cache_param = str(uuid.uuid4())
            url_path = reverse('edit_poste', args=[standard.poste.pk])
            page = request.GET.get('page', '1')
            page_size = request.GET.get('page_size', '12')
            search = request.GET.get('search', '')
            redirect_url = f'{url_path}?cache={cache_param}&page={page}&page_size={page_size}&search={search}'
            return redirect(redirect_url)
    context = {'form': form, 'standard': standard}

    return render(request, 'standard_form.html', context)

@login_required(login_url='login')
@admin_required
def deleteStandardView(request, id):
    standard = Standard.objects.get(id=id)
    if len(standard.poste.standards()) > 1:
        standard.delete()
    cache_param = str(uuid.uuid4())
    url_path = reverse('edit_poste', args=[standard.poste.pk])
    page = request.GET.get('page', '1')
    page_size = request.GET.get('page_size', '12')
    search = request.GET.get('search', '')
    redirect_url = f'{url_path}?cache={cache_param}&page={page}&page_size={page_size}&search={search}'
    return redirect(redirect_url)

@login_required(login_url='login')
@admin_required
def createStandardView(request, id):
    poste = Poste.objects.get(id=id)
    form = StandardForm(poste = poste)
    if request.method == 'POST':
        form = StandardForm(request.POST)
        if form.is_valid():
            standard = form.save()
            if standard.active:
                related_standards = Standard.objects.filter(poste=standard.poste).exclude(pk=standard.pk)
                related_standards.update(active=False)
            cache_param = str(uuid.uuid4())
            url_path = reverse('edit_poste', args=[id])
            page = request.GET.get('page', '1')
            page_size = request.GET.get('page_size', '12')
            search = request.GET.get('search', '')
            redirect_url = f'{url_path}?cache={cache_param}&page={page}&page_size={page_size}&search={search}'
            return redirect(redirect_url)
    context = {'form': form, 'poste': poste}
    return render(request, 'standard_form.html', context)

@login_required(login_url='login')
@admin_required
def setDefaultStandardView(request, id):
    standard = Standard.objects.get(id=id)
    standard.active = True
    standard.save()
    related_standards = Standard.objects.filter(poste=standard.poste).exclude(pk=standard.pk)
    related_standards.update(active=False)
    cache_param = str(uuid.uuid4())
    url_path = reverse('edit_poste', args=[standard.poste.pk])
    page = request.GET.get('page', '1')
    page_size = request.GET.get('page_size', '12')
    search = request.GET.get('search', '')
    redirect_url = f'{url_path}?cache={cache_param}&page={page}&page_size={page_size}&search={search}'
    return redirect(redirect_url)


# REPORT

class CheckEditorMixin:
    def check_editor(self, report):
        if (report.creator != self.request.user or self.request.user.role != "Technicien" 
                or report.state not in ['Brouillon','Refusé']) and self.request.user.role != 'Admin':
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()  
        if not self.check_editor(report):
            return render(request, '403.html', status=403)
        return super().dispatch(request, *args, **kwargs)
    
class CheckCreatorMixin:
    def check_can_create(self):
        if self.request.user.role in ['Observateur', 'Nouveau']:
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.check_can_create():
            return render(request, '403.html', status=403)
        return super().dispatch(request, *args, **kwargs)    
    
class CheckReportViewerMixin:
    def check_viewer(self, report):
        usines = self.request.user.usines.all()
        if report.usine not in usines and self.request.user.role != 'Admin':
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()  
        if not self.check_viewer(report):
            return render(request, '403.html', status=403)
        return super().dispatch(request, *args, **kwargs)

class ReportInline():
    form_class = ReportForm
    model = Report
    template_name = "report_form.html"    
    login_url = 'login'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['admin'] = self.request.user.role == 'Admin'
        kwargs['usines'] = self.request.user.usines.all()
        if self.object:
            kwargs['state'] = self.object.state
        return kwargs

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        
        report = form.save(commit=False) 
        if not report.state or report.state == 'Brouillon':
            report.state = 'Brouillon'
        
        if not report.id:
            report.creator = self.request.user
        
        report.save()

        new = True
        if self.object:
            new = False
        else:
            self.object = report

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()

        if not new:
            cache_param = str(uuid.uuid4())
            url_path = reverse('report_detail', args=[self.object.pk])
            redirect_url = f'{url_path}?cache={cache_param}'
            return redirect(redirect_url)
        return redirect('list_report')

    def formset_samples_valid(self, formset):
        samples = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for sample in samples:
            sample.report = self.object
            sample.save()

class ReportCreate(LoginRequiredMixin, CheckCreatorMixin, ReportInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(ReportCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'samples': SamplesFormSet(prefix='samples'),
            }
        else:
            return {
                'samples': SamplesFormSet(self.request.POST or None, prefix='samples'),
            }

class ReportUpdate(LoginRequiredMixin, CheckEditorMixin, ReportInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(ReportUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'samples': SamplesFormSet(self.request.POST or None, instance=self.object, prefix='samples'),
        }
    
class ReportDetail(LoginRequiredMixin, CheckReportViewerMixin, DetailView):
    model = Report
    template_name = 'report_detail.html'
    context_object_name = 'report'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        samples = self.object.samples()

        postes = [s.poste.designation for s in samples]
        sample_ids = [s.id for s in samples]
        standards = [s.poste.default_standard() for s in samples]

        tami_25 = [{'value': s.value_2_5, 'id': s.id, 'color': 'black' if st.min_2_5_value <= s.value_2_5 <= st.max_2_5_value else 'red'} for s, st in zip(samples, standards)]
        tami_125 = [{'value': s.value_1_25, 'id': s.id, 'color': 'black' if st.min_1_25_value <= s.value_1_25 <= st.max_1_25_value else 'red'} for s, st in zip(samples, standards)]
        tami_06 = [{'value': s.value_0_6, 'id': s.id, 'color': 'black' if st.min_0_6_value <= s.value_0_6 <= st.max_0_6_value else 'red'} for s, st in zip(samples, standards)]
        tami_03 = [{'value': s.value_0_3, 'id': s.id, 'color': 'black' if st.min_0_3_value <= s.value_0_3 <= st.max_0_3_value else 'red'} for s, st in zip(samples, standards)]
        tami_063 = [{'value': s.value_0, 'id': s.id, 'color': 'black' if st.min_0_value <= s.value_0 <= st.max_0_value else 'red'} for s, st in zip(samples, standards)]
        tami_h = [s.value_h for s in samples]

        context.update({ 'postes': postes, 'tami_25': tami_25, 'tami_125': tami_125, 'tami_06': tami_06, 'tami_03': tami_03, 'tami_063': tami_063, 'tami_h': tami_h, 'ids': sample_ids })

        return context

class ReportList(LoginRequiredMixin, FilterView):
    model = Report
    template_name = "list_reports.html"
    context_object_name = "reports"
    filterset_class = ReportFilter
    ordering = ['-date_prelev']
        
    all_T = ['Brouillon', 'Confirmé', 'Validé', 'Refusé', 'Annulé']
    all_A = ['Brouillon', 'Confirmé', 'Validé', 'Refusé', 'Annulé']
    all_V = ['Confirmé', 'Validé', 'Refusé']
    all_NV = ['']

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.user.role
        usines = self.request.user.usines.all()

        if role == 'Technicien':
            queryset = queryset.filter(Q(usine__in=usines) & Q(state__in=self.all_T))

        elif role == 'Validateur':
            queryset = queryset.filter(Q(usine__in=usines) & Q(state__in=self.all_V))
                
        elif role == 'Nouveau':
            queryset = queryset.filter(Q(state__in=self.all_NV))

        elif role in ['Admin', 'Observateur']:
            queryset = queryset.filter(Q(usine__in=usines) & Q(state__in=self.all_A))

        return queryset    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_size_param = self.request.GET.get('page_size')
        page_size = int(page_size_param) if page_size_param else 12        
        paginator = Paginator(context['reports'], page_size)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page'] = page_obj
        context['state_totals'] = self.get_state_totals()
        context['all_total'] = len(context['reports'])
        role_state = {'Technicien': self.all_T, 'Validateur': self.all_V, 'Admin': self.all_A, 'Observateur': self.all_A, 'Nouveau': self.all_NV}
        context['role_state'] = role_state
        return context
    
    def get_state_totals(self):
        user = self.request.user
        usine_condition = Q(usine__in=user.usines.all())

        if user.role == 'Technicien':
            creator_condition = Q(creator=user)
        else:
            creator_condition = Q()

        state_totals = (
            Report.objects.filter(creator_condition | usine_condition)
            .values('state')
            .annotate(total=Count('state'))
            .order_by('state')
        )

        return {state['state']: state['total'] for state in state_totals}

@login_required(login_url='login')
@check_creator
def delete_report(request, pk):
    try:
        report = Report.objects.get(id=pk)
    except Report.DoesNotExist:
        messages.success(request, 'Le rapport n\'existe pas')
        url_path = reverse('list_report')
        cache_param = str(uuid.uuid4())
        redirect_url = f'{url_path}?cache={cache_param}'
        return redirect(redirect_url)

    report.delete()
    messages.success(request, 'Rapport supprimé avec succès')
    url_path = reverse('list_report')
    cache_param = str(uuid.uuid4())
    redirect_url = f'{url_path}?cache={cache_param}'
    return redirect(redirect_url)

@login_required(login_url='login')
def get_data_by_usine(request):
    usine_id = request.GET.get('usine_id')
    if usine_id == '':
        return JsonResponse({'postes': [], 'horaires_list': [] })
    
    usine = Usine.objects.get(pk=usine_id)
    
    poste_list = [ poste.id for poste in Poste.objects.filter(usine_id=usine_id, active=True)]
    horaires_list = [{'id': horaire.id, 'designation': horaire.__str__()} for horaire in usine.horaires.all()]

    return JsonResponse({ 'postes': poste_list, 'horaires_list': horaires_list })

@login_required(login_url='login')
@check_creator
def confirmReport(request, pk):

    params = {
        'page': request.GET.get('page', 1),
        'page_size': request.GET.get('page_size', ''),
        'search': request.GET.get('search', ''),
        'state': request.GET.get('state', ''),
        'start_date': request.GET.get('start_date', ''),
        'end_date': request.GET.get('end_date', ''),
        'usine': request.GET.get('usine', '')
    }
    query_string = '&'.join([f'{key}={value}' for key, value in params.items() if value])

    try:
        report = Report.objects.get(id=pk)
    except Report.DoesNotExist:
        messages.success(request, 'Le rapport n\'existe pas')
        url_path = reverse('report_detail', args=[report.id])
        cache_param = str(uuid.uuid4())
        redirect_url = f'{url_path}?cache={cache_param}&{query_string}'
        return redirect(redirect_url)
    
    if report.state == 'Confirmé':
        url_path = reverse('report_detail', args=[report.id])
        cache_param = str(uuid.uuid4())
        redirect_url = f'{url_path}?cache={cache_param}&{query_string}'
        return redirect(redirect_url)
    
    old_state = report.state

    refusal_reason = '/'

    if old_state != 'Brouillon':
        refusal_reason = 'Corrigée.'
    
    report.state = 'Confirmé'
    
    new_state = report.state
    actor = request.user

    validation = Validation(old_state=old_state, new_state=new_state, actor=actor, refusal_reason=refusal_reason, report=report)
    report.save()
    validation.save()
    report.save()

    if report.usine.address:
        recipient_list = report.usine.address.split('&')
    else:
        recipient_list = ['benshamou@gmail.com'] 
     
    #recipient_list = ['benshamou@gmail.com']

    messages.success(request, 'Rapport validé avec succès')
    subject, formatHtml = getMail('confirm', report, request.user.fullname, old_state == 'Brouillon')
    send_mail(subject, "", 'Puma Labs', recipient_list, html_message=formatHtml)


    url_path = reverse('report_detail', args=[report.id])
    cache_param = str(uuid.uuid4())
    redirect_url = f'{url_path}?cache={cache_param}&{query_string}'
    return redirect(redirect_url)

@login_required(login_url='login')
def cancelReport(request, pk):

    params = {
        'page': request.GET.get('page', 1),
        'page_size': request.GET.get('page_size', ''),
        'search': request.GET.get('search', ''),
        'state': request.GET.get('state', ''),
        'start_date': request.GET.get('start_date', ''),
        'end_date': request.GET.get('end_date', ''),
        'usine': request.GET.get('usine', '')
    }
    query_string = '&'.join([f'{key}={value}' for key, value in params.items() if value])
    try:
        report = Report.objects.get(id=pk)
    except Report.DoesNotExist:
        messages.success(request, 'Le rapport n\'existe pas')
        url_path = reverse('report_detail', args=[report.id])
        cache_param = str(uuid.uuid4())
        redirect_url = f'{url_path}?cache={cache_param}&{query_string}'
        return redirect(redirect_url)
    
    old_state = report.state
    
    report.state = 'Annulé'
    
    new_state = report.state
    actor = request.user

    validation = Validation(old_state=old_state, new_state=new_state, actor=actor, refusal_reason='/', report=report)
    report.save()
    validation.save()

    if old_state != 'Brouillon':    
        if report.usine.address:
            recipient_list = report.usine.address.split('&')
        else:
            recipient_list = ['benshamou@gmail.com']
        #recipient_list = ['benshamou@gmail.com']
        subject, formatHtml = getMail('cancel', report, request.user.fullname)
        send_mail(subject, "", 'Puma Labs', recipient_list, html_message=formatHtml)
        
    messages.success(request, 'Report Annulé successfully' )
    url_path = reverse('report_detail', args=[report.id])
    cache_param = str(uuid.uuid4())
    redirect_url = f'{url_path}?cache={cache_param}&{query_string}'
    return redirect(redirect_url)

@login_required(login_url='login')
@Validator_required
def validateReport(request, pk):
    
    params = {
        'page': request.GET.get('page', 1),
        'page_size': request.GET.get('page_size', ''),
        'search': request.GET.get('search', ''),
        'state': request.GET.get('state', ''),
        'start_date': request.GET.get('start_date', ''),
        'end_date': request.GET.get('end_date', ''),
        'usine': request.GET.get('usine', '')
    }
    query_string = '&'.join([f'{key}={value}' for key, value in params.items() if value])

    try:
        report = Report.objects.get(id=pk)
    except Report.DoesNotExist:
        messages.success(request, 'Le rapport n\'existe pas')
        url_path = reverse('report_detail', args=[report.id])
        cache_param = str(uuid.uuid4())
        redirect_url = f'{url_path}?cache={cache_param}'
        return redirect(redirect_url)
    
    if report.state == 'Validé':
        url_path = reverse('report_detail', args=[report.id])
        cache_param = str(uuid.uuid4())
        redirect_url = f'{url_path}?cache={cache_param}&{query_string}'
        return redirect(redirect_url)
    
    old_state = report.state

    report.state = 'Validé'
    
    new_state = report.state
    actor = request.user

    validation = Validation(old_state=old_state, new_state=new_state, actor=actor, refusal_reason='/', report=report)
    report.save()
    validation.save()

    if report.usine.address:
        recipient_list = report.usine.address.split('&')
    else:
        recipient_list = ['benshamou@gmail.com']
    
    #recipient_list = ['benshamou@gmail.com']

    subject, formatHtml = getMail('validate', report, request.user.fullname)
    send_mail(subject, "", 'Puma Labs', recipient_list, html_message=formatHtml)

    messages.success(request, 'Rapport validé avec succès' )
    url_path = reverse('report_detail', args=[report.id])
    cache_param = str(uuid.uuid4())
    redirect_url = f'{url_path}?cache={cache_param}&{query_string}'
    return redirect(redirect_url)

@login_required(login_url='login')
@Validator_required
def refuseReport(request, pk):
    
    params = {
        'page': request.GET.get('page', 1),
        'page_size': request.GET.get('page_size', ''),
        'search': request.GET.get('search', ''),
        'state': request.GET.get('state', ''),
        'start_date': request.GET.get('start_date', ''),
        'end_date': request.GET.get('end_date', ''),
        'usine': request.GET.get('usine', '')
    }
    query_string = '&'.join([f'{key}={value}' for key, value in params.items() if value])

    try:
        report = Report.objects.get(id=pk)
    except Report.DoesNotExist:
        messages.success(request, 'Le rapport n\'existe pas')
        url_path = reverse('report_detail', args=[report.id])
        cache_param = str(uuid.uuid4())
        redirect_url = f'{url_path}?cache={cache_param}'
        return redirect(redirect_url)
    
    if report.state == 'Refusé':
        messages.success(request, 'Rapport refusé avec succès' )
        url_path = reverse('report_detail', args=[report.id])
        cache_param = str(uuid.uuid4())
        redirect_url = f'{url_path}?cache={cache_param}&{query_string}'
        return redirect(redirect_url)
    
    old_state = report.state

    report.state = 'Refusé'
    
    new_state = report.state
    actor = request.user
    refusal_reason = request.POST.get('refusal_reason')

    validation = Validation(old_state=old_state, new_state=new_state, actor=actor, refusal_reason=refusal_reason, report=report)
    report.save()
    validation.save()

    if report.usine.address:
        recipient_list = report.usine.address.split('&')
    else:
        recipient_list = ['benshamou@gmail.com']
     
    #recipient_list = ['benshamou@gmail.com']

    subject, formatHtml = getMail('refuse', report, request.user.fullname, refusal_reason=refusal_reason)
    send_mail(subject, "", 'Puma Labs', recipient_list, html_message=formatHtml)

    messages.success(request, 'Rapport refusé avec succès' )
    url_path = reverse('report_detail', args=[report.id])
    cache_param = str(uuid.uuid4())
    redirect_url = f'{url_path}?cache={cache_param}&{query_string}'
    return redirect(redirect_url)
    
def getMail(action, report, fullname, old_state = False, refusal_reason = '/'):

    subject = 'Rapport de laboratoire ' + '[' + str(report.id) + ']' + ' - '  + report.usine.__str__()
    address = 'http://10.10.10.53:8000/report/'
    message = ''''''
    if action == 'confirm':
            if old_state:
                oui_13 = 'Oui' if report.retour_1_3 else 'Non'
                oui_06 = 'Oui' if report.retour_1_3 else 'Non'
                message = '''
                <p>Bonjour l'équipe,</p>
                <p>Un rapport a été créé par <b style="color: #45558a">''' + report.creator.fullname + '''</b> <b>(''' + report.usine.designation + ''')</b>''' + ''' le <b>''' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '''</b>:</p>
                <ul>
                    <li><b>N° Rapport :</b> <b style="color: #45558a">''' + str(report.n_report) + '''/''' + report.date_prelev.strftime("%y") + '''</b></li>
                    <li><b>Type de Sable :</b> <b style="color: #45558a">''' + report.type_sable + '''</b></li>
                    <li><b>Date de prélevement :</b> <b style="color: #45558a">''' + str(report.date_prelev) + '''</b></li>
                    <li><b>Horaire :</b> <b style="color: #45558a">''' + report.shift.__str__() + '''</b></li>
                    <li><b>Variateur (%) :</b> <b style="color: #45558a">''' + str(report.variateur) + '''</b></li>
                    <li><b>Débit (t/h) :</b> <b style="color: #45558a">''' + str(report.debit) + '''</b></li>
                    <li><b>T consigne (˚C) :</b> <b style="color: #45558a">''' + str(report.t_consigne) + '''</b></li>
                    <li><b>T réelle (˚C) :</b> <b style="color: #45558a">''' + str(report.t_real) + '''</b></li>
                    <li><b>Fréquence (HZ) B1 :</b> <b style="color: #45558a">''' + str(report.freq_b1) + '''</b></li>
                    <li><b>Fréquence (HZ) B2 :</b> <b style="color: #45558a">''' + str(report.freq_b2) + '''</b></li>
                    <li><b>Retour > 1,3 - </b> <b style="color: #45558a">''' + oui_13 + '''</b></li>
                    <li><b>Retour > 0,6 - </b> <b style="color: #45558a">''' + oui_06 + '''</b></li>'''
                message += '''</ul>'''

                message += '''<p><b>Avec les résultats de laboratoire suivants des échantillons</b></p>
                '''

                for sample in report.samples():
                    standard = sample.poste.default_standard()
                    color_25 = 'black' if standard.min_2_5_value <= sample.value_2_5 <= standard.max_2_5_value else 'red'
                    color_125 = 'black' if standard.min_1_25_value <= sample.value_1_25 <= standard.max_1_25_value else 'red'
                    color_06 = 'black' if standard.min_0_6_value <= sample.value_0_6 <= standard.max_0_6_value else 'red'
                    color_03 = 'black' if standard.min_0_3_value <= sample.value_0_3 <= standard.max_0_3_value else 'red'
                    color_0 = 'black' if standard.min_0_value <= sample.value_0 <= standard.max_0_value else 'red'
                    message += f'''<p><b style="color: #45558a">{sample.poste.designation}</b></p>
                        <ul>
                        <li><b>Tamis 2,5mm :</b> <b style="color: {color_25}">{sample.value_2_5}</b></li>
                        <li><b>Tamis 1,25mm :</b> <b style="color: {color_125}">{sample.value_1_25}</b></li>
                        <li><b>Tamis 0,6mm :</b> <b style="color: {color_06}">{sample.value_0_6}</b></li>
                        <li><b>Tamis 0,3mm :</b> <b style="color: {color_03}">{sample.value_0_3}</b></li>
                        <li><b>Tamis 0mm :</b> <b style="color: {color_0}">{sample.value_0}</b></li>
                        <li><b>Humidité :</b> <b style="color: #6da7d0">{sample.value_h}</b></li>
                        </ul>'''

                
                message += '''<p>Pour plus de détails, veuillez visiter <a href="''' + address + str(report.id) +'''/">''' + address + str(report.id) +'''/</a>.</p>'''
            else:
                message += '''<p><b style="color: #45558a">''' + fullname + '''</b><b>(''' + report.usine.designation + ''')</b> a mis à jour son rapport, vous pouvez le vérifier ici: ''' + address + str(report.id) + '''/</p>'''

    elif action == 'cancel':
        message = '''<p><b>Le rapport [''' + str(report.id) + ''']</b> a été  <b>annulé</b> par <b>''' + fullname + '''</b><b>(''' + report.usine.designation + ''')</b></p>
        </br>

        <p>Pour plus de détails, veuillez visiter <a href="''' + address + str(report.id) +'''/">''' + address + str(report.id) +'''/</a>.</p>'''

    elif action == 'refuse':
        message = '''<p><b>Le rapport [''' + str(report.id) + ''']</b> a été  <b>refusé</b> par <b>''' + fullname + '''</b><b>(''' + report.usine.designation + ''')</b></p>
        </br>
        <p><b>Motif: ''' + refusal_reason + '''</b></p></br>

        <p>Pour plus de détails, veuillez visiter <a href="''' + address + str(report.id) +'''/">''' + address + str(report.id) +'''/</a>.</p>'''

    elif action == 'validate':
        message = '''<p><b>Le rapport [''' + str(report.id) + ''']</b> a été <b>validé</b> par <b>''' + fullname + '''</b><b>(''' + report.usine.designation + ''')</b>
    
    <p>Pour plus de détails, veuillez visiter <a href="''' + address + str(report.id) +'''/">''' + address + str(report.id) +'''/</a>.</p>'''

    return subject, format_html(message)

@login_required(login_url='login')
def get_sample_plot_by_poste(request):
    sample_id = request.GET.get('sampleId')    
    try:
        sample = Sample.objects.get(id=sample_id)
        poste_standard = sample.poste.default_standard()
        interactive_plot = generate_standard_and_sample_plot(poste_standard, sample)

        return JsonResponse({'interactive_plot': interactive_plot})
    except Sample.DoesNotExist:
        return JsonResponse({'error': 'Sample not found'}, status=404)
    
@login_required(login_url='login')
def get_humidity_plot_by_report(request):
    report_id = request.GET.get('reportId')    
    try:
        report = Report.objects.get(id=report_id)
        interactive_plot = generate_humidity_plot(report.samples())

        return JsonResponse({'interactive_plot': interactive_plot})
    except Sample.DoesNotExist:
        return JsonResponse({'error': 'Sample not found'}, status=404)

def generate_standard_and_sample_plot(standard, sample):
    standard_data = {
        'Max Values': [standard.max_2_5_value, standard.max_1_25_value, standard.max_0_6_value, standard.max_0_3_value, standard.max_0_value],
        'Min Values': [standard.min_2_5_value, standard.min_1_25_value, standard.min_0_6_value, standard.min_0_3_value, standard.min_0_value]
    }
    sample_data = {
        'Sample Values': [sample.value_2_5, sample.value_1_25, sample.value_0_6, sample.value_0_3, sample.value_0]
    }

    df_standard = pd.DataFrame(standard_data, index=['2.5mm', '1.25mm', '0.6mm', '0.3mm', '0mm'])
    df_sample = pd.DataFrame(sample_data, index=['2.5mm', '1.25mm', '0.6mm', '0.3mm', '0mm'])

    trace_max = go.Scatter(x=df_standard.index, y=df_standard['Max Values'], mode='lines+markers',
                           name='Max Valeurs', line=dict(color='blue', dash='dash', shape='spline'))
    trace_min = go.Scatter(x=df_standard.index, y=df_standard['Min Values'], mode='lines+markers',
                           name='Min Valeurs', line=dict(color='red', dash='dash', shape='spline'))
    
    trace_sample = go.Scatter(x=df_sample.index, y=df_sample['Sample Values'], mode='lines+markers',
                              name='Valeurs d\'échantillant', line=dict(color='green', shape='spline'))

    title = 'Les standard entre le poste - ' + standard.poste.designation + ' et les valeur d\'échantillant'
    layout = go.Layout( title=title, xaxis=dict(title='Tamis'), yaxis=dict(title='Valeurs'), 
                       plot_bgcolor='rgba(229, 232, 235, 1)', paper_bgcolor='rgba(229, 232, 235, 1)')

    fig = go.Figure(data=[trace_max, trace_min, trace_sample], layout=layout)

    interactive_plot = plot(fig, output_type='div', include_plotlyjs='cdn')

    return interactive_plot

def generate_humidity_plot(samples):

    humidity_data = {
        'Humidity Values': [s.value_h for s in samples]
    }

    df_humidity = pd.DataFrame(humidity_data, index=[s.poste.designation for s in samples])
    
    trace_humidity = go.Scatter(x=df_humidity.index, y=df_humidity['Humidity Values'], mode='lines+markers',
                              name='Valeurs d\'humidité', line=dict(color='#698ed0', shape='spline'))

    title = 'Taux d\'Humidité vs phassage'
    layout = go.Layout( title=title, xaxis=dict(title='Axis'), yaxis=dict(title='Valeurs'), 
                       plot_bgcolor='rgba(229, 232, 235, 1)', paper_bgcolor='rgba(229, 232, 235, 1)')

    fig = go.Figure(data=[trace_humidity], layout=layout)

    interactive_plot = plot(fig, output_type='div', include_plotlyjs='cdn')

    return interactive_plot


