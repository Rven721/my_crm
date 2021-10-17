import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings.base'
django.setup()


from crm.models import Project


def project_list_filter(company=None, project_deliver=None):
    result = Project.objects.all().order_by('name')
    if project_deliver:
        result = result.filter(project_deliver=project_deliver)
    if company:
        result = result.filter(company=company)
    return result
