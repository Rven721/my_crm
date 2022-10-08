"""Here lives urls for contract app"""

from django.urls import path
from cont import views

urlpatterns = [
    path('', views.contract_list_view, name='contracts'),
    path('<int:contract_id>/', views.contract_details_view, name='contract_card'),
    path('add/', views.contract_add_view, name='contract_add'),
    path('terms/', views.terms_list_view, name='terms'),
    path('terms/<int:terms_id>/', views.terms_details_view, name='terms_card'),
    path('terms/add/', views.terms_add_view, name='terms_add'),
    path('agents/', views.agent_list_view, name='agents'),
    path('agents/<int:agent_id>/', views.agent_details_view, name='agent_card'),
    path('agents/add/', views.agent_add_view, name='agent_add'),
]
