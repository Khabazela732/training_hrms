from .views import EmployeeDashboardView
from .views import EmployeeProfileView
from django.urls import path
from . import views 

urlpatterns = [
    path('', EmployeeDashboardView.as_view(), name='employee-dashboard'),
    path('attendance/', views.employee_attendance_list, name='employee_attendance'),
    path('attendance/add/', views.employee_attendance_create, name='employee_attendance_create'),
    path('profile/', EmployeeProfileView.as_view(), name='employee-profile'),
    
]