"""Here urls lives"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_page_view, name='smeta_calculation'),
]
