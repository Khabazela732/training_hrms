from .views import DashboardView, EmployeesView, LeaveListView
from django.urls import path

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('leaves/', LeaveListView.as_view(), name='leave-list')
]