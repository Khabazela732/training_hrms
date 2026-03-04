from .views import CustomLoginView, SignOutView
from django.urls import path

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
]