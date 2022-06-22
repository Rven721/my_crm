"""Filter for to check wether project has undone tasks"""
from django import template
from ..models import Project

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
