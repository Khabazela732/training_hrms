from urllib import response

from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.views import LogoutView

from authenication.models import CustomUser
from .forms import LoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect



# Create your views here.
#admin ---> admin portal
#hr ---> hr portal
#employee ---> employee portal

class CustomLoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'authenication/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_model = get_user_model()
            try:
                user = user_model.objects.get(username=username)
                if user.check_password(password):
                    login(request, user)
                    # Redirect based on role
                    if user.role == 'admin':
                        return redirect('dashboard')
                    elif user.role == 'hr':
                        return redirect('dashboard')
                    elif user.role == 'employee':
                        return redirect('employee-dashboard')
                else:
                    form.add_error(None, "Invalid email or password")
            except user_model.DoesNotExist:
                form.add_error(None, "Invalid email or password")
        return render(request, 'authenication/login.html', {'form': form})

class SignOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("login"))