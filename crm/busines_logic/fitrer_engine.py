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
    """Tag proceed logic. Will parce request and return tags and key"""
    tags = [int(tag_id) for tag_id in request.GET.getlist('tags')]
    key = request.GET.get('key')
    grant_min = request.GET.get('grant_min')
    grant_max = request.GET.get('grant_max')
    status = request.GET.get('status')
    request_parms = [tags, key, grant_min, grant_max, status]
    result = []
    for param in request_parms:
        if not param or len(param) == 0:
            result.append(None)
        else:
            result.append(param)
    return result


def get_projects_count(status=None):
    """Will return a total cout of projects in current.status"""
    if status:
        res = len([project for project in Project.objects.all() if project.statuses.last().status == status])
    else:
        res = len([project for project in Project.objects.all() if project.statuses.last().status == "progress"])
    return res


def has_include_tags(project, search_tags):
    """Will return a list of True/False statuses behalf the serching tags"""
    proj_tags = {tag.id for tag in project.tags.all()}
    result = [tag in proj_tags for tag in search_tags]
    return result


def get_projects_by_status(projects, status=None):
    """Will retrun a list of active projects"""
    if status:
        projects = [project for project in projects if project.statuses.last().status == status]
    else:
        projects = [project for project in projects if project.statuses.last().status == "progress"]
    return projects


def get_projects_by_grant(grant_min=None, grant_max=None):
    """Will return projects query set in given grant limints"""
    projects = Project.objects.all()
    if grant_min:
        projects = projects.filter(grant__gte=grant_min)
    if grant_max:
        projects = projects.filter(grant__lte=grant_max)
    return projects


def filter_by_tags(request):
    """Will retrun a list of projects with required tags"""
    tags, key, grant_min, grant_max, status = parce_request(request)
    projects = get_projects_by_grant(grant_min, grant_max)
    projects = get_projects_by_status(projects, status)
    if tags:
        if key == "not_like":
            projects = [project for project in projects if not any(has_include_tags(project, tags))]
        else:
            projects = [project for project in projects if len(tags) == has_include_tags(project, tags).count(True)]
    result = create_final_result(projects)
    projects_count = get_projects_count(status)
    return [result, projects_count]
