from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, FileResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from crm.models import Contact, Company, Project, Status, Event
from crm.forms import ContactAddForm, CompanyAddForm, ProjectAddForm, StatusAddForm, MeetingAddForm, EventResultAddForm, \
    CompanyContactAddForm, EventSmallAddForm, EventUpdateForm, FilterByCompanyForm
from crm.busines_logic import data_update
from crm.busines_logic.company_data_dadata import get_company_data
from crm.busines_logic.my_calendar import get_request_date
from crm.busines_logic import report_generator
import io


def main_page_view(request):
    return render(request, 'crm/index.html')


def contact_list_view(request):
    contact_list = Contact.objects.all().order_by('first_name')
    form = FilterByCompanyForm()
    if request.method == 'POST':
        form = FilterByCompanyForm(request.POST)
        if form.is_valid():
            contact_list = Contact.objects.filter(companies=form.cleaned_data['company'])
    ctx = {
        'contact_list': contact_list,
        'form': form,
    }
    return render(request, 'crm/contact_list.html', ctx)

@login_required
def contact_details_view(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    ctx = {
        'contact': contact
    }
    return render(request, 'crm/contact_details.html', ctx)

@login_required
def contact_add_view(request):
    if request.method == 'POST':
        form = ContactAddForm(request.POST)
        if form.is_valid():
            contact = form.save()
            return HttpResponseRedirect(reverse('contact_details', kwargs={'contact_id': contact.id}))
        return render(request, 'crm/contact_add.html', {'form': form})
    form = ContactAddForm()
    return render(request, 'crm/contact_add.html', {'form': form})

@login_required
def contact_update_view(request, contact_id):
    update = True
    contact = Contact.objects.get(id=contact_id)
    if request.method == "POST":
        form = ContactAddForm(request.POST)
        if form.is_valid():
            contact_data = form.cleaned_data
            data_update.contact_update(contact_id, contact_data)
            return HttpResponseRedirect(reverse('contact_details', kwargs={'contact_id': contact.id}))
        ctx = {
            'form': form,
            'update': update
        }
        return render(request, 'crm/contact_add.html', ctx)
    form = ContactAddForm(instance=contact)
    ctx = {
        'form': form,
        'update': update
    }
    return render(request, 'crm/contact_add.html', ctx)


def company_list_view(request):
    company_list = Company.objects.all().order_by('short_name')
    ctx = {
        'company_list': company_list,
    }
    return render(request, 'crm/company_list.html', ctx)

@login_required
def company_details_view(request, company_id):
    company = Company.objects.get(id=company_id)
    flag = 'get'
    if request.method == "POST":
        ogrn_number = request.POST['ogrn_number']
        company = data_update.company_profile_update(ogrn_number)
        flag = 'post'
    ctx = {
        'company': company,
        'flag': flag
    }
    return render(request, 'crm/company_details.html', ctx)

@login_required
def company_add_view(request):
    if request.method == 'POST':
        form = CompanyAddForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            data = get_company_data(form.cleaned_data['ogrn_number'])
            company.inn_number = data['inn_number']
            company.short_name = data['short_name']
            company.full_name = data['full_name']
            company.address = data['address']
            company.save()
            company.contacts.set(form.cleaned_data['contacts'])
            return HttpResponseRedirect(reverse('company_details', kwargs={'company_id': company.id}))
        return render(request, 'crm/company_add.html', {'form': form})
    form = CompanyAddForm()
    return render(request, 'crm/company_add.html', {'form': form})

@login_required
def company_contacts_update_view(request, company_id):
    company = Company.objects.get(id=company_id)
    if request.method == "POST":
        form = CompanyContactAddForm(request.POST)
        if form.is_valid():
            contacts_data = form.cleaned_data
            data_update.company_contacts_update(company_id, contacts_data)
            return HttpResponseRedirect(reverse('company_details', kwargs={'company_id': company.id}))
        return render(request, 'crm/company_contacts_add.html', {'form': form})
    form = CompanyContactAddForm(instance=company)
    return render(request, 'crm/company_contacts_add.html', {'form': form})


def project_list_view(request):
    project_list = Project.objects.all().order_by('name')
    form = FilterByCompanyForm()
    company = None
    if request.method == "POST":
        form = FilterByCompanyForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            project_list = Project.objects.filter(company=company).order_by('name')
    ctx = {
        'project_list': project_list,
        'form': form,
        'company': company,
    }
    return render(request, 'crm/project_list.html', ctx)

@login_required
def project_details_view(request, project_id):
    project = Project.objects.get(id=project_id)
    ctx = {
        'project': project,
    }
    return render(request, 'crm/project_details.html', ctx)

@login_required
def project_add_view(request):
    if request.method == "POST":
        form = ProjectAddForm(request.POST)
        if form.is_valid():
            project = form.save()
            Status.objects.create(status='new', project=project)
            return HttpResponseRedirect(reverse('project_details', kwargs={'project_id': project.id}))
        return render(request, 'crm/project_add.html', {'form': form})
    form = ProjectAddForm()
    return render(request, 'crm/project_add.html', {'form': form})

@login_required
def status_change_view(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(id=project_id)
        form = StatusAddForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.project = project
            status.save()
            return HttpResponseRedirect(reverse('project_details', kwargs={'project_id': project.id}))
    form = StatusAddForm()
    return render(request, 'crm/status_change.html', {'form': form})


def event_list_view(request):
    if request.method == 'POST':
        request_date = get_request_date(request.POST.get('date'))
        return HttpResponseRedirect(reverse('events_on_date', kwargs={
            'day': request_date['day'],
            'month': request_date['month'],
            'year': request_date['year'],
        }))
    event_list = Event.objects.filter(small=False)
    today = timezone.now().date()
    yesterday = today.day - 1
    tomorrow = today.day + 1
    ctx = {
        'event_list': event_list,
        'today': today,
        'yesterday': yesterday,
        'tomorrow': tomorrow,
    }
    return render(request, 'crm/event_list.html', ctx)

@login_required
def event_list_on_date_view(request, day, month, year):
    if request.method == 'POST':
        request_date = get_request_date(request.POST.get('date'))
        return HttpResponseRedirect(reverse('events_on_date', kwargs={
            'day': request_date['day'],
            'month': request_date['month'],
            'year': request_date['year'],
        }))
    event_list = Event.objects.filter(
        date__day=day,
        date__month=month,
        date__year=year,
        small=False,
    )
    today = timezone.now().date()
    yesterday = today.day - 1
    tomorrow = today.day + 1
    ctx = {
        'event_list': event_list,
        'today': today,
        'yesterday': yesterday,
        'tomorrow': tomorrow,
    }
    return render(request, 'crm/event_list.html', ctx)

@login_required
def event_details_view(request, event_id):
    event = Event.objects.get(id=event_id)
    ctx = {
        'event': event
    }
    return render(request, 'crm/event_details.html', ctx)

@login_required
def event_add_view(request):
    if request.method == "POST":
        form = MeetingAddForm(request.POST)
        if form.is_valid():
            event = form.save()
            event.small = False
            event.save()
            return HttpResponseRedirect(reverse('event_details', kwargs={'event_id': event.id}))
        return render(request, 'crm/event_add.html', {'form': form})
    form = MeetingAddForm()
    return render(request, 'crm/event_add.html', {'form': form})

@login_required
def event_small_add_view(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == "POST":
        form = EventSmallAddForm(request.POST)
        if form.is_valid():
            event = form.save()
            event.author = request.user
            event.projects.add(project)
            event.save()
            return HttpResponseRedirect(reverse('project_details', kwargs={'project_id': project.id}))
        return render(request, 'crm/event_add.html', {'form': form})
    form = EventSmallAddForm()
    return render(request, 'crm/event_add.html', {'form': form})

@login_required
def event_result_add_view(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = EventResultAddForm(request.POST)
        if form.is_valid():
            event.result = form.cleaned_data['result']
            event.save()
            return HttpResponseRedirect(reverse('event_details', kwargs={'event_id': event_id}))
        return render(request, 'crm/event_result_add.html', {'form': form})
    form = EventResultAddForm()
    return render(request, 'crm/event_result_add.html', {'form': form})

@login_required
def event_update_view(request, event_id):
    event = Event.objects.get(id=event_id)
    form = EventUpdateForm(instance=event)
    ctx = {
        'form': form,
        'update': True
    }
    if request.method == 'POST':
        form = EventUpdateForm(request.POST)
        if form.is_valid():
            data_update.event_details_update(event_id, form.cleaned_data)
            return HttpResponseRedirect(reverse('event_details', kwargs={'event_id': event.id}))
        return render(request, 'crm/event_add.html', ctx)
    return render(request, 'crm/event_add.html', ctx)


def project_event_history_report_view(request, project_id):
    buffer = io.BytesIO()
    wb = report_generator.project_event_history_report(project_id)
    wb.save(buffer)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='my_report.xlsx')


def project_list_statuses_report_view(request, company_id=None):
    company = Company.objects.get(id=company_id) if company_id else None
    buffer = io.BytesIO()
    wb = report_generator.project_status_report(company)
    wb.save(buffer)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='status_report.xlsx')


def test(request):
    pass
