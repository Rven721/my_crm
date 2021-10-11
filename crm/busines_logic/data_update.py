import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings.base'
django.setup()

from crm.models import Contact, Company, Project, Event
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
    company = Company.objects.get(ogrn_number=ogrn_number)
    data = get_company_data(ogrn_number)
    company.inn_number = data['inn_number']
    company.short_name = data['short_name']
    company.full_name = data['full_name']
    company.address = data['address']
    company.save()
    return company


def event_details_update(event_id, new_data):
    event = Event.objects.get(id=event_id)
    event.projects.set(new_data['projects'])
    event.type = new_data['type']
    event.description = new_data['description']
    event.date = new_data['date']
    event.time = new_data['time']
    event.invited_persons.set(new_data['invited_persons'])
    event.result = new_data['result']
    event.save()
    return event
