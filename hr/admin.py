from django.contrib import admin
from .models import Department, Role, Employee, Leave, Attendance, Payroll

admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Employee)
admin.site.register(Leave)
admin.site.register(Attendance)
admin.site.register(Payroll)