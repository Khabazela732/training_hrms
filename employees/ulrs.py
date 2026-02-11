from .views import employee_list, employee_detail
from django.urls import path

urlpatterns = [
    path('list/', employee_list, name='employee_list'),
    path('detail/<int:id>', employee_detail, name='employee_detail'),
]