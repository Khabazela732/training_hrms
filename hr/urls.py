from .views import DashboardView, EmployeesView, Attendance_View, LeaveListView, DepartmentsView, DepartmentCreateView, DepartmentUpdateView, DepartmentDeleteView, PayrollView, AddPayrollView, EditPayrollView, DeletePayrollView, ViewPayrollReport
from django.urls import path
from . import views 

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('leaves/', LeaveListView.as_view(), name='leave-list'),
    
    # Sethu's code
    path('leave/create/', views.leave_create, name='leave_create'),
    path('leave/<int:pk>/', views.leave_detail, name='leave_detail'),
    path('leave/<int:pk>/update/', views.leave_update, name='leave_update'),
    path('leave/<int:pk>/delete/', views.leave_delete, name='leave_delete'),

    path('leave/<int:id>/approve/', views.leave_approve, name='leave_approve'),
    path('leave/<int:id>/decline/', views.leave_decline, name='leave_decline'),

    path('leave/create/', views.leave_create, name='leave_create'),

    path('leaves/', views.leave_list, name='leave-list'),
    path('leave/create/', views.leave_create, name='leave_create'),
    path('leave/<int:pk>/', views.leave_detail, name='leave_detail'),
    path('leave/<int:pk>/update/', views.leave_update, name='leave_update'),
    path('leave/<int:pk>/delete/', views.leave_delete, name='leave_delete'),

    #Mbali's code
    path('attendance/', Attendance_View.as_view(), name='attendance'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    path('attendance/<int:pk>/edit/', views.attendance_edit, name='attendance_edit'),
    path('attendance/<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),

    #lusanda's code
    path('performance/', views.performance_list, name='performance'),
    path('performance/add/', views.add_performance, name='add_performance'),
    path('performance/<int:pk>/edit/', views.edit_performance, name='edit_performance'),
    path('performance/<int:pk>/delete/', views.delete_performance, name='delete_performance'),

    #Senze's code
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('departments/', DepartmentsView.as_view(), name='department_list'),
    path('departments/create/', DepartmentCreateView.as_view(), name='department_create'),
    path('departments/<int:pk>/update/', DepartmentUpdateView.as_view(), name='department_update'),
    path('departments/<int:pk>/delete/', DepartmentDeleteView.as_view(), name='department_delete'),

    #Zee's code
    path('payroll/', PayrollView.as_view(), name='payroll'),
    path('add-payroll/', AddPayrollView.as_view(), name='add_payroll'),
    path('edit-payroll/<int:pk>/', EditPayrollView.as_view(), name='edit_payroll'),
    path('delete-payroll/<int:pk>/', DeletePayrollView.as_view(), name='delete_payroll'),
    path('payroll/report/', ViewPayrollReport.as_view(), name='view_payroll_report'),
]