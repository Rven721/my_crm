import os
import django
from openpyxl import Workbook

os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings'
django.setup()
from crm.models import Project

event_type_decoder = {
    'consult': 'Консультация',
    'discuss': 'Обсуждение',
    'call': 'Созвон',
    'due_dil': 'Контрактация',
    'formal': 'Формальная проверка'
}

project_status_decoder = {
    'new': 'Получена анкета. Ожидается финальное обсуждение и согласование',
    'progress': 'Идет работа по подготовке заявки',
    'finished': 'Работа по проекту завершена'
}


def project_event_history_report(project_id):
    """Принимает на вход id проекта и возвращает несохраненный excel файл
        c историей смены статусов по проекту"""
    project = Project.objects.get(id=project_id)
    event_history = project.events.all()
    wb = Workbook()
    ws = wb.active
    ws['a1'] = 'Проект:'
    ws['a2'] = 'Текущий статус'
    ws['b1'] = project.name
    ws['b2'] = project.statuses.all().last().status
    ws.append([''])
    ws.append(['Тип', 'Дата', 'Описание', 'результат'])
    for event in event_history:
        data = [event_type_decoder[event.type], event.date, event.description, event.result]
        ws.append(data)
    return wb


def project_status_report(company=None):
    """Функция возвращает несохраненный excel файл содержащий список всех проектов и описание их текущего статуса"""
    project_list = Project.objects.all()
    if company:
        project_list = project_list.filter(company=company)
    header = ['Проект', 'Текущий статус']
    wb = Workbook()
    ws = wb.active
    ws.append(header)
    for project in project_list:
        project_data = [project.name, project_status_decoder[project.statuses.all().last().status]]
        ws.append(project_data)
    return wb
