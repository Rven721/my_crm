from django.contrib import admin
from .models import Terms, Agent, Contract, StatusChangeLog


@admin.register(Terms)
class TermsAdmin(admin.ModelAdmin):
    '''Terms model admin'''


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    '''Terms model admin'''


@admin.register(Contract)
class ContactAdmin(admin.ModelAdmin):
    '''Terms model admin'''


@admin.register(StatusChangeLog)
class StatusChangeLogAdmin(admin.ModelAdmin):
    '''Terms model admin'''
