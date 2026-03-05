from .views import EmployeeDashboardView, EmployeePayrollView, download_payroll_pdf, PerformanceDashboardView
from .views import EmployeeProfileView
from django.urls import path
from . import views 

urlpatterns = [
    path('', EmployeeDashboardView.as_view(), name='employee-dashboard'),
    path('attendance/', views.employee_attendance_list, name='employee_attendance'),
    path('attendance/add/', views.employee_attendance_create, name='employee_attendance_create'),
    path('profile/', EmployeeProfileView.as_view(), name='employee-profile'),
    path('payroll/', EmployeePayrollView.as_view(), name='employee-payroll'),
    path('payroll/pdf/<int:payroll_id>/', download_payroll_pdf, name='download_payroll_pdf'),
    path('dashboard/', EmployeeDashboardView.as_view(), name='employee-dashboard'),
    path('performance/', PerformanceDashboardView.as_view(), name='employee-performance'),
    
]