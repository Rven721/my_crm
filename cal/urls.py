"""
A set of urls for calendar
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('<int:year>/<int:month>', views.given_month_calendar_view, name="given_month_cal"),
]
