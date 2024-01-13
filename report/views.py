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
