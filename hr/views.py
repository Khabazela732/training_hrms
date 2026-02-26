from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import View
from .models import Employee, Department, Leave

#my changes

class DashboardView(View):
    def get(self, request):
        template = loader.get_template('hr/pages/dashboard.html')
        employees = Employee.objects.all()
        context = {
            'employee_count': employees.count(),
            'department_count': Department.objects.count(),
        }
        return HttpResponse(template.render(context, request))

class EmployeesView(View):
    def get(self, request):
        template = loader.get_template('hr/pages/employees.html')
        employees = Employee.objects.all()
        context = {
            'employees': employees,
            'department_count': Department.objects.count(),
           
        }
        return HttpResponse(template.render(context, request))

class LeaveListView(View):
    def get(self, request):
        template = loader.get_template('hr/pages/leave.html')
        leaves = Leave.objects.all()
        context = {
            'leaves' : leaves
        }

        return HttpResponse(template.render(context, request))