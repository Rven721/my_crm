from crm.models import Project


ORDERING = {
    'name': 'name',
    'company': 'company_name',
    'event_date_rev': 'last_event_date',
}


def project_list_filter(order_by='name', company=None, project_deliver=None, project_status=None):
    """will return a list of projects based on given data"""
    ordering = ORDERING[order_by]
    result = Project.objects.all()
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
    res = []
    for project in result:
        try:
            company_name = project.company.short_name
        except AttributeError:
            company_name = r'"Не определено'
        if len(project.events.all()) > 0:
            res.append({
                'id': project.id,
                'name': project.name,
                'company_name': company_name,
                'summary': project.summary,
                'last_event_date': project.events.order_by('-date')[0].date,
            })
        else:
            res.append({
                'id': project.id,
                'name': project.name,
                'company_name': company_name,
                'summary': project.summary,
                'last_event_date': None,
            })
    return sorted(res, key=lambda element: (element[ordering] is None, element[ordering]))


def get_incomplete_events(events):
    """Will return a events with incomplete tasks"""
    incomplete_events = []
    for event in events:
        for task in event.tasks.all():
            if task.statuses.all().last().status != 'DONE':
                incomplete_events.append(event)
                break
    return incomplete_events
