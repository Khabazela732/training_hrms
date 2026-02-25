from .views import DashboardView, EmployeesView
from django.urls import path

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('employees/', EmployeesView.as_view(), name='employees')
]