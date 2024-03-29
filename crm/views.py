import cal.google_calendar as gc
from calendar import HTMLCalendar
from datetime import datetime
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, FileResponse
from django.utils import timezone
from django.db.models import Q
from django.utils.encoding import uri_to_iri
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from crm.models import Contact, Company, Project, Status, Event, Task, ProjectDeliver, TaskStatus, RoadMap, Tag
from crm.forms import ContactAddForm,\
    CompanyAddForm,\
    ProjectAddForm,\
    ProjectUpdateForm,\
    StatusAddForm,\
    ProjectSummaryUpdateForm,\
    MultipleEventAddForm,\
    EventResultAddForm, \
    CompanyContactAddForm,\
    EventSmallAddForm,\
    EventUpdateForm,\
    FilterByCompanyForm,\
    FilterByCompanyAndSource, \
    ContactSearchForm,\
    TaskAddForm, \
    EventTaskAddForm, \
    TaskStatusChangeForm, \
    DoerChooseForm, \
    RoadMapForm, \
    TagForm,\
    ProjectTagSelectForm, \
    TagSearchForm
from crm.busines_logic import data_update
from crm.busines_logic.company_data_dadata import get_company_data
from crm.busines_logic.my_calendar import get_request_date
from crm.busines_logic import report_generator, fitrer_engine
import io
import os


def main_page_view(request):
    return render(request, 'crm/index.html')


@login_required
def contact_list_view(request):
    contact_list = Contact.objects.all().order_by('first_name')
    form = FilterByCompanyForm()
    contact_search_form = ContactSearchForm()
    if request.method == 'POST':
        form = FilterByCompanyForm(request.POST)
        if form.is_valid():
            contact_list = Contact.objects.filter(companies=form.cleaned_data['company'])
    if 'query' in request.GET:
        search_name = uri_to_iri(request.GET['query']).capitalize()
        contact_list = Contact.objects.filter(
            Q(last_name__icontains=search_name) |
            Q(first_name__icontains=search_name),
        )
    paginator = Paginator(contact_list, os.environ.get('STRINGS_ON_PAGE', 5))
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    ctx = {
        'form': form,
        'contact_search_form': contact_search_form,
        'page_object': page_object,
    }
    return render(request, 'crm/contact_list.html', ctx)


@login_required
def contact_details_view(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    ctx = {
        'contact': contact,
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
            'update': update,
        }
        return render(request, 'crm/contact_add.html', ctx)
    form = ContactAddForm(instance=contact)
    ctx = {
        'form': form,
        'update': update,
    }
    return render(request, 'crm/contact_add.html', ctx)


@login_required
def company_list_view(request):
    search_form = ContactSearchForm()
    company_list = Company.objects.all().order_by('short_name')
    if 'query' in request.GET:
        search_form = ContactSearchForm(request.GET)
        if search_form.is_valid():
            search_name = search_form.cleaned_data['query'].upper()
            company_list = company_list.filter(
                Q(short_name__icontains=search_name) |
                Q(full_name__icontains=search_name)
            )
    paginator = Paginator(company_list, os.environ.get('STRINGS_ON_PAGE', 5))
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    ctx = {
        'company_list': company_list,
        'page_object': page_object,
        'search_form': search_form,
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
        'flag': flag,
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


@login_required
def project_list_view(request):
    order_by = request.GET.get('order_by', 'name')
    project_list = fitrer_engine.project_list_filter(order_by, project_status="progress")
    status_projects_count = len(project_list)
    form = FilterByCompanyAndSource()
    tag_form = ProjectTagSelectForm()
    company = None
    project_deliver = None
    project_status = ''
    if request.method == "POST":
        order_by = request.POST.get('order_by', 'name')
        project_list = Project.objects.all()
        form = FilterByCompanyAndSource(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            project_deliver = form.cleaned_data['project_deliver']
            project_status = form.cleaned_data['project_status']
            project_list = fitrer_engine.project_list_filter(order_by, company, project_deliver, project_status)
    if 'key' in request.GET:
        project_list, status_projects_count = fitrer_engine.filter_by_tags(request)
        tag_form = ProjectTagSelectForm(request.GET)
    paginator = Paginator(project_list, os.environ.get('STRINGS_ON_PAGE', 5))
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    ctx = {
        'form': form,
        'tags_form': tag_form,
        'company': company,
        'project_deliver': project_deliver,
        'project_status': project_status,
        'project_list': project_list,
        'page_object': page_object,
        'cur_date': datetime.now().date(),
        'status_projects_count': status_projects_count,
    }
    return render(request, 'crm/project_list.html', ctx)


@login_required
def project_list_dates_view(request):
    project_list = Project.objects.all().order_by('start_date')
    project_list = [project for project in project_list if project.statuses.last().status == "progress"]
    ctx = {
        'project_list': project_list,
        'cur_date': datetime.now().date(),
    }
    return render(request, 'crm/project_list_dates.html', ctx)


@login_required
def project_details_view(request, project_id):
    project = Project.objects.get(id=project_id)
    events = project.events.all().order_by('-date', '-time')
    incomplete_events = fitrer_engine.get_incomplete_events(events)
    roadmap = RoadMap.objects.filter(project__id=project_id)
    if not roadmap:
        RoadMap.objects.create(project=project)
        roadmap = RoadMap.objects.filter(project__id=project_id)
        form = RoadMapForm(instance=roadmap)
    form = RoadMapForm(instance=roadmap[0])
    if request.method == "POST":
        form = RoadMapForm(request.POST)
        if form.is_valid():
            new_data = form.cleaned_data
            data_update.roadmap_update(roadmap[0].id, new_data)
    ctx = {
        'project': project,
        'events': events,
        'form': form,
        'incomplete_events': incomplete_events,
    }
    return render(request, 'crm/project_details.html', ctx)


@login_required
def project_add_view(request):
    if request.method == "POST":
        form = ProjectAddForm(request.POST)
        if form.is_valid():
            project = form.save()
            Status.objects.create(status='new', project=project)
            RoadMap.objects.create(project=project)
            return HttpResponseRedirect(reverse('project_details', kwargs={'project_id': project.id}))
        return render(request, 'crm/project_add.html', {'form': form})
    form = ProjectAddForm()
    return render(request, 'crm/project_add.html', {'form': form})


@login_required
def project_update_view(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = ProjectUpdateForm(request.POST)
        if form.is_valid():
            new_data = form.cleaned_data
            data_update.project_details_update(project_id, new_data)
            return HttpResponseRedirect(reverse('project_details', kwargs={'project_id': project.id}))
        return render(request, 'crm/company_contacts_add.html', {'form': form})
    form = ProjectUpdateForm(instance=project)
    return render(request, 'crm/project_add.html', {'form': form})


@login_required
def project_summary_update_view(request, project_id):
    project = Project.objects.get(id=project_id)
    form = ProjectSummaryUpdateForm(instance=project)
    if request.method == "POST":
        form = ProjectSummaryUpdateForm(request.POST)
        if form.is_valid():
            project.summary = form.cleaned_data['summary']
            project.save()
            return HttpResponseRedirect(reverse('projects'))
        return render(request, 'crm/project_summary_update.html', {'form': form})
    return render(request, 'crm/project_summary_update.html', {'form': form})


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


@login_required
def event_list_view(request):
    if request.method == 'POST':
        request_date = get_request_date(request.POST.get('date'))
        return HttpResponseRedirect(reverse('events_on_date', kwargs={
            'day': request_date['day'],
            'month': request_date['month'],
            'year': request_date['year'],
        }))
    event_list = Event.objects.all().order_by('date').reverse()
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
    cur_date = datetime.now().date()
    ctx = {
        'event': event,
        'cur_date': cur_date,
    }
    return render(request, 'crm/event_details.html', ctx)


@login_required
def event_add_view(request):
    if request.method == "POST":
        form = MultipleEventAddForm(request.POST)
        if form.is_valid():
            event = form.save()
            if event.small:
                gc_event = gc.add_google_calendar_event(event)
                if gc_event:
                    event.gc_event_id = gc_event['id']
            event.save()
            return HttpResponseRedirect(reverse('event_details', kwargs={'event_id': event.id}))
        return render(request, 'crm/event_add.html', {'form': form})
    form = MultipleEventAddForm()
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
            if event.small:
                gc_event = gc.add_google_calendar_event(event)
                if gc_event:
                    event.gc_event_id = gc_event['id']
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
            event.took_time = form.cleaned_data['took_time']
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
        'update': True,
    }
    if request.method == 'POST':
        form = EventUpdateForm(request.POST)
        if form.is_valid():
            data_update.event_details_update(event_id, form.cleaned_data)
            return HttpResponseRedirect(reverse('events'))
        ctx['error'] = 'Got errors'
        ctx['form'] = EventUpdateForm(request.POST)
        return render(request, 'crm/event_add.html', ctx)
    return render(request, 'crm/event_add.html', ctx)


@login_required
def event_task_add_view(request, event_id):
    event = Event.objects.get(id=event_id)
    form = EventTaskAddForm()
    ctx = {
        'form': form,
    }
    if request.method == 'POST':
        form = TaskAddForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.event = event
            task.save()
            TaskStatus.objects.create(status='NEW', task=task)
            return HttpResponseRedirect(reverse('event_details', kwargs={'event_id': event.id}))
        ctx = {
            'form': form,
        }
        return render(request, 'crm/task_add.html', ctx)
    return render(request, 'crm/task_add.html', ctx)


@login_required
def project_event_history_report_view(request, project_id):
    buffer = io.BytesIO()
    wb = report_generator.project_event_history_report(project_id)
    wb.save(buffer)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='my_report.xlsx')


@login_required
def project_list_statuses_report_view(request, company_id=None, project_deliver_slug=None, project_status=None):
    company = Company.objects.get(id=company_id) if company_id else None
    project_deliver = ProjectDeliver.objects.get(slug=project_deliver_slug) if project_deliver_slug else None
    buffer = io.BytesIO()
    wb = report_generator.project_status_report(company=company, project_deliver=project_deliver, project_status=project_status)
    wb.save(buffer)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='status_report.xlsx')


@login_required
def task_list_view(request, doer_id=None, day=None, month=None, year=None):
    form = DoerChooseForm()
    tasks = Task.objects.all().order_by('end_date').reverse()
    today = datetime.now().date
    if request.method == "POST" and request.POST['doer'] != "":
        doer = request.POST['doer']
        tasks = tasks.filter(doer=doer)
        form = DoerChooseForm(instance=tasks[0])
    elif doer_id:
        tasks = tasks.filter(doer=doer_id)
    if day and month and year:
        tasks = tasks.filter(
            end_date__day=day,
            end_date__month=month,
            end_date__year=year,
        )
    ctx = {
        'tasks': tasks,
        'form': form,
        'today': today,
    }
    return render(request, 'crm/task_list.html', ctx)


@login_required
def task_add_view(request, event_id=None):
    """A form to add a new task to event"""
    if request.method == "POST":
        form = TaskAddForm(request.POST)
        if form.is_valid():
            task = form.save()
            TaskStatus.objects.create(status='NEW', task=task)
            return HttpResponseRedirect(reverse('event_details', kwargs={'event_id': task.event.id}))
        return render(request, 'crm/task_add.html', {'form': form})
    form = TaskAddForm()
    return render(request, 'crm/task_add.html', {'form': form})


@login_required
def task_details_view(request, task_id):
    task = Task.objects.get(id=task_id)
    ctx = {'task': task}
    return render(request, 'crm/task_details.html', ctx)


@login_required
def task_status_change_view(request, task_id):
    task = Task.objects.get(id=task_id)
    event = task.event
    cur_status = task.statuses.last().status
    cur_result = task.event.result
    form = TaskStatusChangeForm(initial={'status': cur_status, 'result': cur_result})
    if request.method == "POST":
        form = TaskStatusChangeForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.task = task
            status.changer = request.user
            event.result = form.cleaned_data['result']
            event.save()
            status.save()
            return HttpResponseRedirect(reverse('event_details', kwargs={'event_id': task.event.id}))
        return render(request, 'crm/task_status_change.html', {'form': form})
    return render(request, 'crm/task_status_change.html', {'form': form})


@login_required
def task_update(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == "POST":
        form = TaskAddForm(request.POST)
        if form.is_valid():
            task_details = form.cleaned_data
            data_update.task_details_update(task_id, task_details)
            return HttpResponseRedirect(reverse(task_list_view))
    form = TaskAddForm(instance=task)
    return render(request, 'crm/task_add.html', {'form': form})


@login_required
def tag_add_view(request, project_id=None):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            if project_id:
                return HttpResponseRedirect(reverse('project_tag_list', kwargs={'project_id': project_id}))
            return HttpResponseRedirect(reverse(tag_list_view))
        return render(request, 'crm/tag_add.html', {'form': form})
    form = TagForm()
    return render(request, 'crm/tag_add.html', {'form': form})


@login_required
def tag_update_view(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag.name = form.cleaned_data['name']
            tag.save()
            return HttpResponseRedirect(reverse(tag_list_view))
        return render(request, 'crm/tag_update.html', {'form': form})
    form = TagForm(instance=tag)
    return render(request, 'crm/tag_update.html', {'form': form})


@login_required
def tag_list_view(request, project_id=None):
    form = TagSearchForm()
    current_taggs = None
    if project_id:
        current_taggs = Project.objects.get(id=project_id).tags.all().order_by('name')
        unused_tags = Tag.objects.exclude(id__in=[tag.id for tag in current_taggs]).order_by('name')
    else:
        unused_tags = Tag.objects.all()
    if "query" in request.GET:
        tag_request = uri_to_iri(request.GET["query"]).upper()
        unused_tags = unused_tags.filter(name__icontains=tag_request)
        form = TagSearchForm(request.GET)
    ctx = {
        "project_id": project_id,
        "current_tags": current_taggs,
        "unused_tags": unused_tags,
        "tag_search_form": form,
    }
    return render(request, 'crm/tag_list.html', ctx)


def test(request):
    calendar = HTMLCalendar()
    ctx = {
        "calendar": calendar.formatmonth(),
    }
    return render(request, 'crm/test.html', ctx)


@login_required
def project_tag_add_view(request, project_id, tag_id):
    project = Project.objects.get(id=project_id)
    tag = Tag.objects.get(id=tag_id)
    project.tags.add(tag)
    project.save()
    return HttpResponseRedirect(reverse('project_tag_list', kwargs={'project_id': project_id}))


@login_required
def project_tag_remove_view(request, project_id, tag_id):
    project = Project.objects.get(id=project_id)
    tag = Tag.objects.get(id=tag_id)
    project.tags.remove(tag)
    project.save()
    return HttpResponseRedirect(reverse('project_tag_list', kwargs={'project_id': project_id}))
