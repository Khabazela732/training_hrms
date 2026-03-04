from django.shortcuts import render
from django.views import View

# Create your views here.

class EmployeeDashboardView(View):
    def get(self, request):
        return render(request, 'employee/pages/dashboard.html')
