from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from hr.models import Employee, Attendance, Leave, Payroll, Performance
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Count, Avg
from hr.forms import AttendanceForm
from django.views import View
from django import forms
from django.contrib.auth.decorators import login_required
from hr.models import Payroll
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

class EmployeeDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        
        try:
            employee = Employee.objects.select_related('department', 'role').get(user=user)
        except Employee.DoesNotExist:
            context = {'error': 'Employee record not found. Contact administrator.'}
            return render(request, 'employee/pages/dashboard.html', context)

        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        attendance_qs = Attendance.objects.filter(
            employee=employee,
            date__range=[start_date, end_date]
        )
        
        total_attendance_days = attendance_qs.count()
        present_days = attendance_qs.filter(status='present').count()
        attendance_pct = round((present_days / total_attendance_days * 100), 1) if total_attendance_days > 0 else 0
        
        
        approved_leaves = Leave.objects.filter(
            employee=employee,
            status='Approved'
        ).aggregate(total_days=Count('id'))['total_days'] or 0
        
        annual_leave_quota = 21
        leave_balance = max(0, annual_leave_quota - approved_leaves)
        
        latest_payroll = Payroll.objects.filter(
            employee=employee
        ).order_by('-created_at').first()
        
        if latest_payroll:
            payroll_status = f"₹{latest_payroll.total_salary():,.2f} - {latest_payroll.month}"
        else:
            payroll_status = "No payroll records"
        
        avg_performance = Performance.objects.filter(
            employee=employee
        ).aggregate(avg_rating=Avg('rating'))['avg_rating']
        
        performance_rating = f"{avg_performance:.1f}/5" if avg_performance else "No reviews"
        
        context = {
            'employee': employee,
            
            'attendance_pct': f"{attendance_pct}%",
            'leave_balance': f"{leave_balance} Days",
            'payroll_status': payroll_status,
            'performance_rating': performance_rating,

            'attendance_recent_summary': f"{present_days}/{total_attendance_days} days",
            'attendance_trend': "Excellent" if attendance_pct > 90 else "Good" if attendance_pct > 80 else "Fair",
            'leave_used': approved_leaves,
            'leave_remaining': leave_balance,
            'leave_total': annual_leave_quota,

            'department_name': employee.department.name,
            'role_name': employee.role.name,
            'date_joined_formatted': employee.date_joined.strftime('%B %Y'),
            'days_employed': (date.today() - employee.date_joined).days,

            'recent_attendance_count': total_attendance_days,
            'recent_leaves_count': Leave.objects.filter(employee=employee).count(),
            'payroll_count': Payroll.objects.filter(employee=employee).count(),
            'performance_count': Performance.objects.filter(employee=employee).count(),
        }
        
        return render(request, 'employee/pages/dashboard.html', context)

@login_required
def employee_attendance_list(request):
    employee = request.user.employee

    attendances = Attendance.objects.filter(
        employee=employee
    ).order_by('-date', '-created_at')

    return render(
        request,
        'employee/pages/my_attendance.html',
        {'attendances': attendances}
    )

@login_required
def employee_attendance_create(request):
    employee = request.user.employee

    if request.method == 'POST':
        form = AttendanceForm(
            request.POST,
            employee=employee,
            hide_employee=True
        )
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.employee = employee
            attendance.save()
            return redirect('employee_attendance')
    else:
        form = AttendanceForm(
            employee=employee,
            hide_employee=True
        )

    return render(request, 'employee/pages/attendance_form.html', {
        'form': form,
        'title': 'Add Attendance'
    })

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status', 'check_in_time', 'check_out_time']

    def __init__(self, *args, **kwargs):
        employee = kwargs.pop('employee', None)
        hide_employee = kwargs.pop('hide_employee', False)
        super().__init__(*args, **kwargs)

        if hide_employee and employee:
            self.fields['employee'].initial = employee
            self.fields['employee'].widget = forms.HiddenInput()



#France

class EmployeeProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        try:
            employee = Employee.objects.select_related('department', 'role', 'user').get(user=user)
        except Employee.DoesNotExist:
            context = {'error': 'Employee record not found. Contact administrator.'}
            return render(request, 'employee/pages/profile.html', context)

        context = {
            'employee': employee,
            'department_name': employee.department.name,
            'role_name': employee.role.name,
            'date_joined_formatted': employee.date_joined.strftime('%B %d, %Y'),
            'username': employee.user.username,
        }

        return render(request, 'employee/pages/profile.html', context)

class EmployeePayrollView(View):
    def get(self, request):
     
        payrolls = Payroll.objects.filter(employee__user=request.user).order_by('-month')
        return render(request, 'employee/pages/payroll.html', {'payrolls': payrolls})



def download_payroll_pdf(request, payroll_id):
    payroll = get_object_or_404(Payroll, id=payroll_id, employee__user=request.user)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=(8.5*inch, 11*inch))
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'title',
        parent=styles['Title'],
        alignment=1, 
        fontSize=20,
        textColor=colors.HexColor("#2980b9")
    )


    elements.append(Paragraph("Payroll Statement", title_style))
    elements.append(Spacer(1, 0.2*inch))

    
    data = [
        ['Month', 'Salary (R)', 'Bonus (R)', 'Deductions (R)', 'Net Pay (R)'],
        [payroll.month, f"{payroll.basic_salary:,.2f}", f"{payroll.bonus:,.2f}", f"{payroll.deductions:,.2f}", f"{payroll.net_pay:,.2f}"]
    ]

    table = Table(data, hAlign='CENTER')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2980b9')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#bdc3c7')),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
