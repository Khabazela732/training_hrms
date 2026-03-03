from .views import DashboardView, EmployeesView, LeaveListView
from django.urls import path
from . import views

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('leaves/', LeaveListView.as_view(), name='leave-list'),

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
    path('leave/<int:pk>/delete/', views.leave_delete, name='leave_delete')
]