from django import forms
from .models import Leave, Attendance, Performance, Employee


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = "__all__"

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = [
            'employee',
            'date',
            'status',
            'check_in_time',
            'check_out_time'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'check_in_time': forms.TimeInput(attrs={'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = '__all__'

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'user',
            'first_name',
            'last_name',
            'email',
            'department',
            'role',
            'contract_copy',
        ]
