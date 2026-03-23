from django.urls import path
from .views import home
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('jobs/<int:pk>/', views.job_detail_public, name='job_detail_public'),
    path('apply/<int:pk>/', views.apply_job, name='apply_job'),
]