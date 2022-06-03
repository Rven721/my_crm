from django.contrib import admin
from crm.models import Contact, Company, Project, Status, Event, Task, ProjectDeliver, Document, RoadMap, TaskStatus


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Class for contact model administration"""
    ordering = ("first_name", )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Class for Company model administration"""
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Class for project model administration"""
    pass


@admin.register(RoadMap)
class RoadMapAdmin(admin.ModelAdmin):
    """Class for roadmap model administration"""
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Class for project status model administration"""
    pass


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    """Class for task status model administration"""
    list_display = ("date", "status", "task")
    list_filter = ("changer", "date")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Class for event model administration"""
    ordering = ("date",)
    list_display = ("category", "date", "get_project", "author")
    list_filter = ("author", "date")

    def get_project(self, event):
        """Will return first project of event"""
        return event.projects.all()[0]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Class for task model administration"""
    pass


@admin.register(ProjectDeliver)
class ProjectDeliverAdmin(admin.ModelAdmin):
    """Class for project deliver model administration"""
    pass


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Class for document model administration"""
    list_display = ['name', 'event']
