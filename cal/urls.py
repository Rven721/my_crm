"""
A set of urls for calendar
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('gc/approvment/', views.get_approvment_view, name='get_approvment'),
    path('gc/clear/', views.clear_credentials_view, name='clear_creds'),
    path('gc/', views.handle_approvment_response_view, name='response_handler'),
    path('<int:year>/<int:month>', views.given_month_calendar_view, name="given_month_cal"),
]
