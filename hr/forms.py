from django import forms
from .models import Leave, Attendance, Performance, Employee, Job, Candidate, Interview


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

class PerformanceBulkUploadForm(forms.Form):
    file = forms.FileField(label="Upload CSV or Excel file")

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

class AttendanceUploadForm(forms.Form):
    file = forms.FileField(label="Upload CSV File")

class EmployeeAttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['check_in_time', 'check_out_time']
        widgets = {
            'check_in_time': forms.TimeInput(attrs={'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time'}),
        }
class BulkEmployeeUploadForm(forms.Form):
    file = forms.FileField(label="CSV file")


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['profile_picture']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['candidate', 'job', 'date', 'time', 'interviewer', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
            'time': forms.TimeInput(attrs={'type':'time'}),
        }