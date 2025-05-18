from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from report.views import admin_required
from .forms import *
from .filters import *
from django.core.paginator import Paginator
import uuid
from django.urls import reverse
from functools import wraps
from django.contrib import messages
from django.http import JsonResponse
from .utils import *
from django.forms import modelformset_factory
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# DECORATORS

def check_creator(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'id' in kwargs:
            complaint_id = kwargs['id']
        elif 'pk' in kwargs:
            complaint_id = kwargs['pk']
        complaint = Complaint.objects.get(id=complaint_id)
        if complaint.creator != request.user and request.user.role != 'Admin':
            return render(request, '403.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper

def resp_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role in ['Admin', 'Résponsable'] or request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '403.html', status=403)
    return wrapper

def direc_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role in ['Admin', 'Directeur'] or request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '403.html', status=403)
    return wrapper

def comm_app_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role in ['Admin', 'Directeur', 'Résponsable', 'Commercial'] or request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '403.html', status=403)
    return wrapper


# Emplacements
@login_required(login_url='login')
@admin_required
def listEmplacementView(request):
    emplacements = Emplacement.objects.all().order_by('id')
    filteredData = EmplacementFilter(request.GET, queryset=emplacements)
    emplacements = filteredData.qs
    page_size_param = request.GET.get('page_size')
    page_size = int(page_size_param) if page_size_param else 12   
    paginator = Paginator(emplacements, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = { 'page': page, 'filtredData': filteredData}
    return render(request, 'list_emplacements.html', context)

@login_required(login_url='login')
@admin_required
def deleteEmplacementView(request, id):
    emplacement = Emplacement.objects.get(id=id)
    emplacement.delete()
    return redirect(getRedirectionURL(request, reverse('emplacements')))

@login_required(login_url='login')
@admin_required
def createEmplacementView(request):
    form = EmplacementForm()
    if request.method == 'POST':
        form = EmplacementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(getRedirectionURL(request, reverse('emplacements')))
    context = {'form': form}
    return render(request, 'emplacement_form.html', context)

@login_required(login_url='login')
@admin_required
def editEmplacementView(request, id):
    emplacement = Emplacement.objects.get(id=id)
    form = EmplacementForm(instance=emplacement)
    if request.method == 'POST':
        form = EmplacementForm(request.POST, instance=emplacement)
        if form.is_valid():
            form.save()
            return redirect(getRedirectionURL(request, reverse('emplacements')))
    context = {'form': form, 'emplacement': emplacement}

    return render(request, 'emplacement_form.html', context)

# PRODUCTS
@login_required(login_url='login')
@admin_required 
def listProductList(request):
    products = Product.objects.all().order_by('id')
    filteredData = ProductFilter(request.GET, queryset=products)
    products = filteredData.qs
    page_size_param = request.GET.get('page_size')
    page_size = int(page_size_param) if page_size_param else 12   
    paginator = Paginator(products, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = { 'page': page, 'filtredData': filteredData }
    return render(request, 'list_products.html', context)

@login_required(login_url='login')
@admin_required
def deleteProductView(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect(getRedirectionURL(request, reverse('products')))


@login_required(login_url='login')
@admin_required
def createProductView(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(getRedirectionURL(request, reverse('products')))
    context = {'form': form }
    return render(request, 'product_form.html', context)

@login_required(login_url='login')
@admin_required
def editProductView(request, id):
    product = Product.objects.get(id=id)

    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect(getRedirectionURL(request, reverse('products')))
    context = {'form': form, 'product': product }

    return render(request, 'product_form.html', context)

# CATEGORY
@login_required(login_url='login')
@admin_required 
def listCategoryView(request):
    categories = Category.objects.all().order_by('id')
    filteredData = CategoryFilter(request.GET, queryset=categories)
    categories = filteredData.qs
    page_size_param = request.GET.get('page_size')
    page_size = int(page_size_param) if page_size_param else 12   
    paginator = Paginator(categories, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = { 'page': page, 'filtredData': filteredData }
    return render(request, 'list_categories.html', context)

@login_required(login_url='login')
@admin_required
def deleteCategoryView(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect(getRedirectionURL(request, reverse('categories')))


@login_required(login_url='login')
@admin_required
def createCategoryView(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(getRedirectionURL(request, reverse('categories')))
    context = {'form': form }
    return render(request, 'category_form.html', context)

@login_required(login_url='login')
@admin_required
def editCategoryView(request, id):
    category = Category.objects.get(id=id)

    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect(getRedirectionURL(request, reverse('categories')))
    context = {'form': form, 'category': category }

    return render(request, 'category_form.html', context)


# COMPLAINTS
@login_required(login_url='login')
@comm_app_required 
def listComplaintsList(request):
    complaints = Complaint.objects.all().order_by('-date_modified')
    filteredData = ComplaintFilter(request.GET, queryset=complaints)
    complaints = filteredData.qs
    page_size_param = request.GET.get('page_size')
    page_size = int(page_size_param) if page_size_param else 12   
    paginator = Paginator(complaints, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = { 'page': page, 'filtredData': filteredData }
    return render(request, 'list_complaints.html', context)

@login_required(login_url='login')
@check_creator
def deleteComplaintView(request, id):
    complaint = Complaint.objects.get(id=id)
    complaint.delete()
    return redirect(getRedirectionURL(request, reverse('list_complaint')))

@login_required(login_url='login')
@comm_app_required
def createComplaintView(request):
    form = ComplaintCommForm(user=request.user)
    ImageFormSet = modelformset_factory(Image,form=ImageForm, extra=1, can_delete=True)
    if request.method == 'POST':
        form = ComplaintCommForm(request.POST, user=request.user)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if form.is_valid() and formset.is_valid():
            complaint = form.save(commit=False)
            complaint.state = 'Brouillon'
            complaint.save()
            for image in formset:
                if image.cleaned_data.get('DELETE'):
                    if image.instance.pk:
                        image.instance.delete()
                else:
                    if image.instance.pk is None:
                        image.instance.complaint = complaint
                    if image.instance.image:
                        image.save() 
            return redirect(getRedirectionURL(request, reverse('list_complaint')))
        else:
            print("Form Errors:", form.errors)
            print("Formset Errors:")
            for subform in formset:
                print(subform.errors)
    else:
        formset = ImageFormSet(queryset=Image.objects.none())
    context = {'form': form, 'formset': formset }
    return render(request, 'complaint_form.html', context)

@login_required(login_url='login')
@check_creator
def editComplaintView(request, id):
    complaint = Complaint.objects.get(id=id)
    old_lab_attachment = complaint.treatment_labo_att
    old_site_attachment = complaint.treatment_site_att
    form = ComplaintCommForm(instance=complaint, user=request.user)
    ImageFormSet = modelformset_factory(Image,form=ImageForm, extra=0, can_delete=True)
    if request.method == 'POST':
        form = ComplaintCommForm(request.POST, request.FILES, instance=complaint, user=request.user)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.filter(complaint=complaint))
        if form.is_valid() and formset.is_valid():
            complaint = form.save(commit=False)
            if not complaint.treatment_labo_att and old_lab_attachment:
                old_lab_attachment.delete(save=False)
            if not complaint.treatment_site_att and old_site_attachment:
                old_site_attachment.delete(save=False)
            complaint.save()
            for image in formset:
                if image.cleaned_data.get('DELETE'):
                    if image.instance.pk:
                        image.instance.delete()
                else:
                    if image.instance.pk is None:
                        image.instance.complaint = complaint
                    if image.instance.image:
                        image.save() 
            return redirect(getRedirectionURL(request, reverse('complaint_detail', args=[complaint.id])))
        else:
            print("Form Errors:", form.errors)
            print("Formset Errors:")
            for subform in formset:
                print(subform.errors)
    else:
        formset = ImageFormSet(queryset=Image.objects.filter(complaint=complaint))
    context = {'form': form, 'complaint': complaint, 'formset': formset }
    return render(request, 'complaint_form.html', context)

@login_required(login_url='login')
@check_creator
def confirmComplaint(request, id):
    try:
        complaint = Complaint.objects.get(id=id)
    except Complaint.DoesNotExist:
        messages.success(request, 'Complaint Does not exit')

    url_path = reverse('complaint_detail', args=[complaint.id])
    if complaint.state == 'En traitement':
        return redirect(getRedirectionURL(request, url_path))
    
    old_state = complaint.state
    complaint.state = 'En traitement'
    new_state = complaint.state
    actor = request.user
    cycle = Cycle(old_state=old_state, new_state=new_state, actor=actor, complaint=complaint)
    complaint.save()
    cycle.save()
    messages.success(request, 'Complaint En traitement avec succès')

    subject = f"Réclamation {complaint.n_reclamation}" 
    context = { 'complaint': complaint }
    html_message = render_to_string('complaint_confirmation.html', context)
    email = EmailMultiAlternatives(subject, None, 'Puma Commercial', [complaint.usine.address])
    email.attach_alternative(html_message, "text/html") 
    for image in complaint.images():
        email.attach(image.image.name, image.image.read(), 'image/jpeg')
    email.send() 

    return redirect(getRedirectionURL(request, url_path))

@login_required(login_url='login')
@check_creator
def cancelComplaint(request, id):
    try:
        complaint = Complaint.objects.get(id=id)
    except Complaint.DoesNotExist:
        messages.success(request, 'Complaint Does not exit')

    url_path = reverse('complaint_detail', args=[complaint.id])
    if complaint.state == 'Annulé':
        return redirect(getRedirectionURL(request, url_path))
    
    old_state = complaint.state
    complaint.state = 'Annulé'
    new_state = complaint.state
    actor = request.user
    cycle = Cycle(old_state=old_state, new_state=new_state, actor=actor, complaint=complaint)
    complaint.save()
    cycle.save()
    messages.success(request, 'Complaint Annulé avec succès')
    return redirect(getRedirectionURL(request, url_path))

@login_required(login_url='login')
@resp_required
def completeComplaintView(request, id):
    complaint = Complaint.objects.get(id=id)
    form = ComplaintResponsableForm(instance=complaint)
    old_lab_attachment = complaint.treatment_labo_att
    old_site_attachment = complaint.treatment_site_att
    if request.method == 'POST':
        form = ComplaintResponsableForm(request.POST, request.FILES, instance=complaint)
        if form.is_valid():
            complaint = form.save(commit=False)
            if not complaint.treatment_labo_att and old_lab_attachment:
                old_lab_attachment.delete(save=False)
            if not complaint.treatment_site_att and old_site_attachment:
                old_site_attachment.delete(save=False)
            complaint.save()
            old_state = complaint.state
            complaint.state = 'Traité'
            new_state = complaint.state
            actor = request.user
            cycle = Cycle(old_state=old_state, new_state=new_state, actor=actor, complaint=complaint)
            complaint.save()
            cycle.save()
            return redirect(getRedirectionURL(request, reverse('complaint_detail', args=[complaint.id])))
    context = {'form': form, 'complaint': complaint }
    return render(request, 'complete_complaint_form.html', context)

@login_required(login_url='login')
@direc_required
def finishComplaintView(request, id):
    complaint = Complaint.objects.get(id=id)
    form = ComplaintDirectorForm(instance=complaint)
    if request.method == 'POST':
        form = ComplaintDirectorForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            old_state = complaint.state
            complaint.state = 'Clôturé'
            new_state = complaint.state
            actor = request.user
            cycle = Cycle(old_state=old_state, new_state=new_state, actor=actor, complaint=complaint)
            complaint.save()
            cycle.save()
            subject = f"Re: Réclamation {complaint.n_reclamation}" 
            context = { 'complaint': complaint, 'decider': cycle.actor, 'date_decided': cycle.date }
            html_message = render_to_string('complaint_decision.html', context)
            email = EmailMultiAlternatives(subject, None, 'Puma Commercial', [complaint.usine.address])
            email.attach_alternative(html_message, "text/html")
            for image in complaint.images():
                email.attach(image.image.name, image.image.read(), 'image/jpeg')
            if complaint.treatment_labo_att:
                email.attach(complaint.treatment_labo_att.name, complaint.treatment_labo_att.read())
            if complaint.treatment_site_att:
                email.attach(complaint.treatment_site_att.name, complaint.treatment_site_att.read())
            email.send() 
            return redirect(getRedirectionURL(request, reverse('complaint_detail', args=[complaint.id])))
    context = {'form': form, 'complaint': complaint }
    return render(request, 'finish_complaint_form.html', context)

@login_required(login_url='login')
@comm_app_required
def detailComplaintView(request, id):
    complaint = Complaint.objects.get(id=id)
    context = {'complaint': complaint }
    return render(request, 'complaint_detail.html', context)

@login_required(login_url='login')
def live_search(request):
    search_for = request.GET.get('search_for', '')
    term = request.GET.get('search_term', '')

    if search_for == 'distributeur':
        records = getDistributeurId(term)
    elif search_for == 'client':
        records = getClientId(term)

    if len(records) > 0:
        return JsonResponse([{'id': obj[0], 'name': f'''{obj[1]} - [ref: 0{obj[0]}] : ({obj[0]})'''.replace("'","\\'")} for obj in records], safe=False)
        
    return JsonResponse([], safe=False)

def getRedirectionURL(request, url_path):
    params = {
        'page': request.GET.get('page', '1'),
        'page_size': request.GET.get('page_size', '12'),
        'search': request.GET.get('search', ''),
        'state': request.GET.get('state', ''),
        'usine': request.GET.get('usine', ''),
    }
    cache_param = str(uuid.uuid4())
    query_string = '&'.join([f'{key}={value}' for key, value in params.items() if value])
    return f'{url_path}?cache={cache_param}&{query_string}'