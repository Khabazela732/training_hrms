from .views import EmployeeDashboardView
from django.urls import path
from . import views 

urlpatterns = [
    path('', EmployeeDashboardView.as_view(), name='employee-dashboard'),
    
]