"""Block with logic for database update"""
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings.base'
django.setup()

from crm.models import Contact, Company, Project, Event, RoadMap, Task
from crm.busines_logic.company_data_dadata import get_company_data


def contact_update(contact_id, contact_data):
    """Принимает ID контакта и данные полученные из очищенной формы.
    Полученные данные сохраняются в экземпляр базы контактов с заданным ID"""
    contact = Contact.objects.get(id=contact_id)
    contact.first_name = contact_data['first_name']
    contact.second_name = contact_data['second_name']
    contact.last_name = contact_data['last_name']
    contact.email = contact_data['email']
    contact.phone = contact_data['phone']
    contact.additional_info = contact_data['additional_info']
    contact.save()
    return None


def company_contacts_update(company_id, contacts_data):
    """Принимает ID компании и список контактов.
    Полученные данные сохраняются в профиль компании"""
    company = Company.objects.get(id=company_id)
    company.contacts.set(contacts_data['contacts'])
    company.save()
    return None


def company_profile_update(ogrn_number):
    """Will receve OGRN number and return updated company profile"""
    company = Company.objects.get(ogrn_number=ogrn_number)
    data = get_company_data(ogrn_number)
    company.inn_number = data['inn_number']
    company.short_name = data['short_name']
    company.full_name = data['full_name']
    company.address = data['address']
    company.save()
    return company


def roadmap_update(roadmap_id, new_data):
    roadmap = RoadMap.objects.get(id=roadmap_id)
    roadmap.kick_off_meeting = new_data['kick_off_meeting']
    roadmap.contract = new_data['contract']
    roadmap.to_do_list = new_data['to_do_list']
    roadmap.save()
    return roadmap


def event_details_update(event_id, new_data):
    """Will retrun updated event instanse"""
    event = Event.objects.get(id=event_id)
    event.projects.set(new_data['projects'])
    event.category = new_data['category']
    event.description = new_data['description']
    event.date = new_data['date']
    event.time = new_data['time']
    # event.invited_persons.set(new_data['invited_persons'])
    event.result = new_data['result']
    event.small = new_data['small']
    event.save()
    return event


def project_details_update(project_id, new_data):
    """Will retrun updated projcet instance"""
    project = Project.objects.get(id=project_id)
    project.description = new_data['description']
    project.start_date = new_data['start_date']
    project.end_date = new_data['end_date']
    project.grant = new_data['grant']
    project.full_cost = new_data['full_cost']
    project.company = new_data['company']
    project.contacts.set(new_data['contacts'])
    project.project_deliver = new_data['project_deliver']
    project.save()
    return project


def task_details_update(task_id, new_data):
    """Will update a data for givven task"""
    task = Task.objects.get(id=task_id)
    task.name = new_data['name']
    task.start_date = new_data['start_date']
    task.end_date = new_data['end_date']
    task.doer = new_data['doer']
    task.event = new_data['event']
    task.description = new_data['description']
    task.save()
    return task
