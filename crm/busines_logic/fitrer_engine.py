import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings.base'
django.setup()


from crm.models import Project


def project_list_filter(company=None, project_deliver=None, project_status=None):
    """will return a list of projects based on given data"""
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


def get_incomplete_events(events):
    """Will return a events with incomplete tasks"""
    incomplete_events = []
    for event in events:
        for task in event.tasks.all():
            if task.statuses.all().last().status != 'DONE':
                incomplete_events.append(event)
                break
    return incomplete_events
