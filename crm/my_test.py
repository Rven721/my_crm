import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings.base'
django.setup()

from crm.models import Project, Status, Company
from busines_logic import report_generator

status_list = [
    ('new', 'Новый проект'),
    ('progress', 'В работе'),
    ('finished', 'Работа завершена')
]


choices=[(None, '------')]+status_list
print(choices)