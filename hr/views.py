from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.views import View
from .models import Employee, Department, Leave
from .forms import LeaveForm


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
            'leaves': leaves
        }
        return HttpResponse(template.render(context, request))

# List all leaves
def leave_list(request):
    leaves = Leave.objects.all()
    return render(request, 'hr/leave/list.html', {'leaves': leaves})

# View leave detail
def leave_detail(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    return render(request, 'hr/leave/detail.html', {'leave': leave})

# Update leave
def leave_update(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    if request.method == 'POST':
        form = LeaveForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('leave-list')
    else:
        form = LeaveForm(instance=leave)
    return render(request, 'hr/leave/update.html', {'form': form})

# Delete leave
def leave_delete(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    if request.method == 'POST':
        leave.delete()
        return redirect('leave-list')
    return render(request, 'hr/leave/delete.html', {'leave': leave})

# Create leave
def leave_create(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = LeaveForm()
    return render(request, 'hr/leave/create.html', {'form': form})

#staus functions
def leave_approve(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.status = "Approved"
    leave.save()
    return redirect('leave-list')


def leave_decline(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.status = "Declined"
    leave.save()
    return redirect('leave-list')