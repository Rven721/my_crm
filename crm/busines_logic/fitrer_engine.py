from crm.models import Project


ORDERING = {
    'name': 'name',
    'company': 'company_name',
    'event_date_rev': 'last_event_date',
}


def create_final_result(result_list):
    res = []
    for project in result_list:
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
    return res


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
    result = create_final_result(result)
    return sorted(result, key=lambda element: (element[ordering] is None, element[ordering]))


def get_incomplete_events(events):
    """Will return a events with incomplete tasks"""
    incomplete_events = []
    for event in events:
        for task in event.tasks.all():
            if task.statuses.all().last().status != 'DONE':
                incomplete_events.append(event)
                break
    return incomplete_events


def parce_request(request):
    """Will parce request with tags"""
    tags = [int(tag_id) for tag_id in request.GET.getlist('tags')]
    key = request.GET.get('key')
    return [tags, key]


def has_include_tags(project, search_tags):
    """Will return True if project has all required tags"""
    proj_tags = {tag.id for tag in project.tags.all()}
    result = [tag in proj_tags for tag in search_tags]
    return result


def filter_by_tags(request):
    """Will retrun a list of projects with required tags"""
    tags, key = parce_request(request)
    if key == "not_like":
        projects = [project for project in Project.objects.all() if not any(has_include_tags(project, tags))]
    else:
        projects = [project for project in Project.objects.all() if len(tags) == has_include_tags(project, tags).count(True)]
    result = create_final_result(projects)
    return result
