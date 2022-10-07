from django.urls import path
from cont import views

urlpatterns = [
    path('', views.contracts_list_view, name='contracts'),
]
