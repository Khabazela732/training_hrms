from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Employee

def employee_list(request):
    template = loader.get_template('employee_list.html')  
    employees = Employee.objects.all()
    context = {
        'employees': employees,
    }
    return HttpResponse(template.render(context, request))

def employee_detail(request, id):
    template = loader.get_template('employee_detail.html')  
    employee = Employee.objects.get(id=id)
    context = {
        'employee': employee,
    }
    return HttpResponse(template.render(context, request))