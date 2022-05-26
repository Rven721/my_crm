from django.contrib import admin
from crm.models import Contact, Company, Project, Status, Event, Task, ProjectDeliver, Document, RoadMap


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    ordering = ("first_name", )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(RoadMap)
class RoadMapAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectDeliver)
class ProjectDeliverAdmin(admin.ModelAdmin):
    pass


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'event']
