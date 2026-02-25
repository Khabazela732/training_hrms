from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from authenication.models import CustomUser as User

# Create your views here.
def home(request):
    user = User.objects.first()  # Just for demonstration, get the first user
    template = loader.get_template('web/home.html')
    context = {
    'user': user,
    }
    return HttpResponse(template.render(context, request))