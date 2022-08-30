"""Here will be ursl"""
from django.urls import path
from debts import views

urlpatterns = [
    path('', views.debt_list_view, name='debts'),
    path('person/<int:person_id>/', views.person_view, name='person_page'),
    path('person/add/', views.person_add_view, name='new_person'),
    path('expense/<int:expense_id>/', views.expense_view, name='expense_page'),
    path('expense/add/', views.expense_add_view, name='new_expense'),
    path('transh/list/', views.transh_list_view, name='transh_list'),
    path('transh/list/<int:day>/<int:month>/<int:year>/', views.transh_list_view, name='transhes_on_date'),
    path('transh/<int:transh_id>/', views.transh_view, name='transh_view'),
    path('transh/add/', views.transh_add_view, name='new_transh'),
    path('payment_order/', views.debt_calculation_view, name='payment_order'),
    path('success/', views.success_page_view, name='success'),
]
