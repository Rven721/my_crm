from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page_view, name='main'),
    path('contacts/', views.contact_list_view, name='contacts'),
    path('contacts/<contact_id>/', views.contact_details_view, name='contact_details'),
    path('contacts/<contact_id>/update/', views.contact_update_view, name='contact_update'),
    path('new_contact/', views.contact_add_view, name='contact_add'),
    path('companies/', views.company_list_view, name='companies'),
    path('companies/<company_id>/', views.company_details_view, name='company_details'),
    path('companies/<company_id>/contact_update', views.company_contacts_update_view, name='company_contacts_update'),
    path('new_company/', views.company_add_view, name='company_add'),
    path('projects/', views.project_list_view, name='projects'),
    path('projects/status_report/', views.project_list_statuses_report_view, name='project_list_status_report'),
    path('projects/<project_id>/', views.project_details_view, name='project_details'),
    path('project/<project_id>/status_change/', views.status_change_view, name='status_change'),
    path('project/<project_id>/event_add/', views.event_small_add_view, name='event_small_add'),
    path('project/<project_id>/event_history', views.project_event_history_report_view, name='project_event_history'),
    path('new_project/', views.project_add_view, name='project_add'),
    path('events/', views.event_list_view, name='events'),
    path('events/<int:day>/<int:month>/<int:year>/', views.event_list_on_date_view, name='events_on_date'),
    path('events/<event_id>/', views.event_details_view, name='event_details'),
    path('event/<event_id>/result_add/', views.event_result_add_view, name='event_result_add'),
    path('event/<event_id>/update', views.event_update_view, name='event_update'),
    path('new_event/', views.event_add_view, name='event_add'),
    path('test/<project_id>/', views.test, name='test'),
]
