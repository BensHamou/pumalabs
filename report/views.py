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
        standards = [s.poste.default_standard() for s in samples]

        tami_25 = [{'value': s.value_2_5, 'color': 'black' if st.min_2_5_value <= s.value_2_5 <= st.max_2_5_value else 'red'} for s, st in zip(samples, standards)]
        tami_125 = [{'value': s.value_1_25, 'color': 'black' if st.min_1_25_value <= s.value_1_25 <= st.max_1_25_value else 'red'} for s, st in zip(samples, standards)]
        tami_06 = [{'value': s.value_0_6, 'color': 'black' if st.min_0_6_value <= s.value_0_6 <= st.max_0_6_value else 'red'} for s, st in zip(samples, standards)]
        tami_03 = [{'value': s.value_0_3, 'color': 'black' if st.min_0_3_value <= s.value_0_3 <= st.max_0_3_value else 'red'} for s, st in zip(samples, standards)]
        tami_063 = [{'value': s.value_0, 'color': 'black' if st.min_0_value <= s.value_0 <= st.max_0_value else 'red'} for s, st in zip(samples, standards)]
        tami_h = [s.value_h for s in samples]

        context.update({ 'postes': postes, 'tami_25': tami_25, 'tami_125': tami_125, 'tami_06': tami_06, 'tami_03': tami_03, 'tami_063': tami_063, 'tami_h': tami_h })

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

