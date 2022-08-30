"""Administratin logic for debt app"""
from django.contrib import admin
from debts.models import Person, Expense, Transh, Debt


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Person admin panel"""

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """Expense admin panel"""

@admin.register(Transh)
class TransAdmin(admin.ModelAdmin):
    """Transh admin panel"""

@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    """Debt admin panel"""
