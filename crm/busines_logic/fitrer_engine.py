import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings.base'
django.setup()


from crm.models import Project


def project_list_filter(company=None, project_deliver=None, project_status=None):
    result = Project.objects.order_by('name')
    if project_deliver:
        result = result.filter(project_deliver=project_deliver)
    if company:
        result = result.filter(company=company)
    if project_status:
        result = list(result)
        check_list = result.copy()
        for project in check_list:
            try:
                if project.statuses.last().status != project_status:
                    result.remove(project)
            except AttributeError:
                result.remove(project)
    return result
