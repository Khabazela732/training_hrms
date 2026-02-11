from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def home(request):
    user = request.user
    template = loader.get_template('web/home.html')
    context = {
    'user': user,
    }
    return HttpResponse(template.render(context, request))