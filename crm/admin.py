from django.contrib import admin
from crm.models import Contact, Company, Project, Status, Event


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
