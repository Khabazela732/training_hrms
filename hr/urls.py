from .views import DashboardView, EmployeesView, EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView, EmployeeDetailView, Attendance_View, LeaveListView, DepartmentsView, DepartmentCreateView, DepartmentUpdateView, DepartmentDeleteView, PayrollView,DepartmentBulkCreateView, AddPayrollView, EditPayrollView, DeletePayrollView, ViewPayrollReport
from django.urls import path
from . import views 
#France
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/<int:pk>/edit/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('leaves/', LeaveListView.as_view(), name='leave-list'),
    
    # Sethu's code
    path('leave/', views.leave_list, name='leave'),
    path('leave/create/', views.leave_create, name='create'),
    path('leave/view/<int:id>/', views.leave_view, name='leave_view'),
    path('leave/update/<int:id>/', views.leave_update, name='leave_update'),
    path('leave/delete/<int:id>/', views.leave_delete, name='leave_delete'),

    #Mbali's code
    path('attendance/', Attendance_View.as_view(), name='attendance'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    path('attendance/<int:pk>/edit/', views.attendance_edit, name='attendance_edit'),
    path('attendance/<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),
    path('attendance/bulk-upload/', views.bulk_upload_attendance, name='bulk_upload_attendance'),
    path('attendance/bulk-delete/', views.attendance_bulk_delete, name='attendance_bulk_delete'),

    #lusanda's code
    path('performance/', views.performance_list, name='performance'),
    path('performance/add/', views.add_performance, name='add_performance'),
    path('performance/<int:pk>/edit/', views.edit_performance, name='edit_performance'),
    path('performance/<int:pk>/delete/', views.delete_performance, name='delete_performance'),

    #Senzo's code
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('departments/', DepartmentsView.as_view(), name='department_list'),
    path('departments/create/', DepartmentCreateView.as_view(), name='department_create'),
    path('departments/<int:pk>/update/', DepartmentUpdateView.as_view(), name='department_update'),
    path('departments/<int:pk>/delete/', DepartmentDeleteView.as_view(), name='department_delete'),
    path('departments/bulk-create/', DepartmentBulkCreateView.as_view(), name='department_bulk_create'),

    #Zee's code
    path('payroll/', PayrollView.as_view(), name='payroll'),
    path('add-payroll/', AddPayrollView.as_view(), name='add_payroll'),
    path('edit-payroll/<int:pk>/', EditPayrollView.as_view(), name='edit_payroll'),
    path('delete-payroll/<int:pk>/', DeletePayrollView.as_view(), name='delete_payroll'),
    path('payroll/report/', ViewPayrollReport.as_view(), name='view_payroll_report'),

    path('upload-contract/<int:employee_id>/', views.upload_contract, name='upload_contract'),
]
