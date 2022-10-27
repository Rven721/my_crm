"""Filter for to check wether project has undone tasks"""
from django import template
from ..models import Project, Task

register = template.Library()


@register.filter
def has_undone_tasks(project_id: int) -> bool:
    """Will return true if project has events with undone tasks"""
    project = Project.objects.get(id=project_id)
    events = project.events.all()
    for event in events:
        for task in event.tasks.all():
            if task.statuses.all().last().status != 'DONE':
                return True
    return False


@register.filter
def user_has_undone_tasks(user_id: int) -> bool:
    """Will return True if user has undone tasks"""
    tasks = Task.objects.filter(doer__id=user_id)
    for task in tasks:
        if task.statuses.last().status in ['NEW', 'PROGRESS']:
            return True
    return False
