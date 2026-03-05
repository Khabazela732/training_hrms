from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.views import View
from psycopg2 import IntegrityError
from .models import Employee, Department, Leave, Attendance, Performance, Payroll
from .forms import LeaveForm, EmployeeForm
from django.utils import timezone
from .forms import AttendanceForm, PerformanceForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from authenication.models import CustomUser


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

class EmployeeCreateView(SuccessMessageMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'hr/pages/employee_form.html'
    success_url = reverse_lazy('employees')
    success_message = 'Employee created successfully!'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['user'].queryset = CustomUser.objects.filter(employee__isnull=True)
        return form


class EmployeeUpdateView(SuccessMessageMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'hr/pages/employee_form.html'
    success_url = reverse_lazy('employees')
    success_message = 'Employee updated successfully!'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['user'].queryset = CustomUser.objects.filter(
            Q(employee__isnull=True) | Q(employee=self.object)
        )
        return form


class EmployeeDeleteView(SuccessMessageMixin, DeleteView):
    model = Employee
    template_name = 'hr/pages/employee_confirm_delete.html'
    success_url = reverse_lazy('employees')
    success_message = 'Employee deleted successfully!'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, self.success_message)
        return response


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'hr/pages/employee_detail.html'
    context_object_name = 'employee'

class LeaveListView(View):
    def get(self, request):
        template = loader.get_template('hr/pages/leave.html')
        leaves = Leave.objects.all()
        context = {
            'leaves': leaves
        }
        return HttpResponse(template.render(context, request))

# LIST ALL LEAVES
def leave_list(request):

    leaves = Leave.objects.all()   # Fetch all records from database

    context = {
        "leaves": leaves
    }

    return render(request, "hr/pages/leave.html", context)


# CREATE LEAVE
def leave_create(request):
    if request.method == "POST":
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave')
    else:
        form = LeaveForm()

    return render(request, "hr/pages/create.html", {"form": form})


# VIEW LEAVE DETAILS
def leave_view(request, id):
    leave = get_object_or_404(Leave, id=id)
    return render(request, "hr/pages/leave_view.html", {"leave": leave})


# UPDATE LEAVE
def leave_update(request, id):
    leave = get_object_or_404(Leave, id=id)

    if request.method == "POST":
        form = LeaveForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('leave')
    else:
        form = LeaveForm(instance=leave)

    return render(request, "hr/pages/leave_update.html", {"form": form})


# DELETE LEAVE
def leave_delete(request, id):
    leave = get_object_or_404(Leave, id=id)

    if request.method == "POST":
        leave.delete()
        return redirect('leave')

    return redirect('leave')

#Mbali's code

class Attendance_View(View):
    def get(self, request):
        template = loader.get_template('hr/pages/attendance.html')
        
        today = timezone.now().date()
        recent_attendances = Attendance.objects.select_related(
            'employee__department'  
        ).prefetch_related(
            'employee'  
        ).filter(
            employee__isnull=False 
        ).order_by('-date', '-created_at')[:50]
        total_employees = Employee.objects.count()
        present_today = Attendance.objects.filter(date=today, status='present').count()
        late_today = Attendance.objects.filter(date=today, status='late').count()
        absent_today = Attendance.objects.filter(date=today, status='absent').count()
        
        stats = {
            'present': present_today,
            'late': late_today,
            'absent': absent_today,
            'total': total_employees
        }
        
        context = {
            'recent_attendances': recent_attendances,
            'stats': stats,
            'today': today,
        }
        return HttpResponse(template.render(context, request))

def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save()
            print("SAVED:", attendance)
            return redirect('attendance')
        else:
            print(form.errors)
    else:
        form = AttendanceForm()

    return render(request, 'hr/pages/attendance_form.html', {
        'form': form,
        'title': 'Add Attendance'
    })

def attendance_edit(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)

    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('attendance')
    else:
        form = AttendanceForm(instance=attendance)

    return render(request, 'hr/pages/attendance_form.html', {
        'form': form,
        'title': 'Edit Attendance'
    })

def attendance_delete(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)

    if request.method == 'POST':
        attendance.delete()
        return redirect('attendance')

    return render(request, 'hr/pages/attendance_confirm_delete.html', {
        'attendance': attendance
    })

def attendance_list(request):
    recent_attendances = Attendance.objects.select_related('employee').order_by('-date', '-id')

    return render(request, 'hr/pages/attendance.html', {
        'recent_attendances': recent_attendances
    })

#Lusanda code will go here

def departments(request):
    context = {
        'departments': Department.objects.all(),
        'department_count': Department.objects.count(),
    }
    return render(request, 'hr/pages/departments.html', context)


def performance_list(request):
    search_query = request.GET.get('search', '')

    performance_qs = Performance.objects.select_related(
        'employee',
        'department'
    ).order_by('-rating', '-id')

    # Filter by employee first or last name if search query is provided
    if search_query:
        performance_qs = performance_qs.filter(
            Q(employee__first_name__icontains=search_query) |
            Q(employee__last_name__icontains=search_query)
        )

    paginator = Paginator(performance_qs, 10)
    page_number = request.GET.get('page')
    performances = paginator.get_page(page_number)

    return render(request, 'hr/pages/performance.html', {
        'performances': performances,
        'search_query': search_query  # Pass the current search term back to template
    })


# ADD PERFORMANCE
def add_performance(request):
    if request.method == 'POST':
        form = PerformanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Performance record added successfully.')
            return redirect('performance')
    else:
        form = PerformanceForm()

    return render(request, 'hr/pages/performance_add.html', {
        'form': form,
        'title': 'Add Performance'
    })


# EDIT PERFORMANCE
def edit_performance(request, pk):
    performance = get_object_or_404(Performance, pk=pk)

    if request.method == 'POST':
        form = PerformanceForm(request.POST, instance=performance)

        if form.is_valid():
            form.save()  # Just save normally

            messages.success(request, "Performance review updated successfully.")
            return redirect('performance')
    else:
        form = PerformanceForm(instance=performance)

    return render(request, 'hr/pages/performance_edit.html', {
        'form': form,
        'title': 'Edit Performance'
    })

# DELETE PERFORMANCE
def delete_performance(request, pk):
    performance = get_object_or_404(Performance, pk=pk)

    if request.method == 'POST':
        performance.delete()
        messages.success(request, 'Performance record deleted successfully.')
        return redirect('performance')
    return render(request, 'hr/pages/performance_confirm_delete.html', {
        'performance': performance
    })

class DepartmentsView(View):
    def get(self, request):
        departments = Department.objects.prefetch_related('employee_set').all()
        context = {
            'departments': departments,
        }
        return render(request, 'hr/pages/departments.html', context)

class DepartmentCreateView(SuccessMessageMixin, CreateView):
    model = Department
    fields = ['name', 'description']
    template_name = 'hr/pages/department_form.html'
    success_url = reverse_lazy('department_list')
    success_message = 'Department created successfully!'

class DepartmentUpdateView(SuccessMessageMixin, UpdateView):
    model = Department
    fields = ['name', 'description']
    template_name = 'hr/pages/department_form.html'
    success_url = reverse_lazy('department_list')
    success_message = 'Department updated successfully!'

class DepartmentDeleteView(SuccessMessageMixin, DeleteView):
    model = Department
    template_name = 'hr/pages/department_confirm_delete.html'
    success_url = reverse_lazy('department_list')
    success_message = 'Department deleted successfully!'

#Zee's code will go here
class PayrollView(View):
    def get(self, request):
        payrolls = Payroll.objects.select_related('employee').all()
        employees = Employee.objects.all()
        context = {
            'payrolls': payrolls,
            'employees': employees,
            'total_employees': employees.count(),
            'total_payroll': payrolls.count(),
        }
        return render(request, 'hr/pages/payroll.html', context)


class AddPayrollView(View):
    def post(self, request):
        employee_id = request.POST.get('employee')
        month = request.POST.get('month')
        try:
            Payroll.objects.create(
                employee_id=employee_id,
                basic_salary=float(request.POST.get('basic_salary')),
                bonus=float(request.POST.get('bonus') or 0),
                deductions=float(request.POST.get('deductions') or 0),
                month=month
            )
            messages.success(request, "Payroll added successfully.")
        except IntegrityError:
            messages.error(
                request,
                f"Payroll for this employee in {month} already exists!"
            )
        return redirect('payroll')

class EditPayrollView(View):
    def get(self, request, pk):
        payroll = get_object_or_404(Payroll, pk=pk)
        employees = Employee.objects.all()
        context = {
            'payroll': payroll,
            'employees': employees,
        }
        return render(request, 'hr/pages/edit_payroll.html', context)

    def post(self, request, pk):
        payroll = get_object_or_404(Payroll, pk=pk)
        payroll.employee_id = request.POST.get('employee')
        payroll.basic_salary = float(request.POST.get('basic_salary'))
        payroll.bonus = float(request.POST.get('bonus') or 0)
        payroll.deductions = float(request.POST.get('deductions') or 0)
        payroll.month = request.POST.get('month')
        payroll.save()
        messages.success(request, "Payroll updated successfully.")
        return redirect('payroll')


class DeletePayrollView(View):
    def get(self, request, pk):
        payroll = get_object_or_404(Payroll, pk=pk)
        return render(request, 'hr/pages/delete_payroll.html', {'payroll': payroll})

    def post(self, request, pk):
        payroll = get_object_or_404(Payroll, pk=pk)
        payroll.delete()
        messages.success(request, "Payroll deleted successfully.")
        return redirect('payroll')


class ViewPayrollReport(View):
    template_name = 'hr/pages/view_payroll.html'

    def get(self, request):
        payrolls = Payroll.objects.select_related('employee').all()
        return render(request, self.template_name, {'payrolls': payrolls})

    def post(self, request):
        payrolls = Payroll.objects.select_related('employee').all()

        if 'export_pdf' in request.POST:
            return self.export_pdf(payrolls)

        if 'export_excel' in request.POST:
            return self.export_excel(payrolls)

        return render(request, self.template_name, {'payrolls': payrolls})

    def export_pdf(self, payrolls):
        from io import BytesIO
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()
        elements.append(Paragraph("Monthly Payroll Report", styles['Title']))
        elements.append(Spacer(1, 20))

        
        data = [["Employee", "Month", "Basic Salary", "Bonus", "Deductions", "Total Salary"]]
        for p in payrolls:
            total_salary = float(p.basic_salary or 0) + float(p.bonus or 0) - float(p.deductions or 0)
            data.append([
                f"{p.employee.first_name} {p.employee.last_name}",
                p.month,
                f"{p.basic_salary:.2f}",
                f"{p.bonus:.2f}",
                f"{p.deductions:.2f}",
                f"{total_salary:.2f}"
            ])

        table = Table(data, hAlign='LEFT', colWidths=[120, 80, 80, 60, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 10),
            ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ]))
        elements.append(table)

        
        def add_watermark(canvas_obj, doc_obj):
            canvas_obj.saveState()
            canvas_obj.setFont('Helvetica-Bold', 40)
            canvas_obj.setFillColorRGB(0.6, 0.3, 0.8, alpha=0.3)  
            canvas_obj.drawString(450, 800, "HRMS")  
            canvas_obj.restoreState()

        
        doc.build(elements, onFirstPage=add_watermark, onLaterPages=add_watermark)

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="monthly_payroll_report.pdf"'
        return response

    def export_excel(self, payrolls):
        import pandas as pd
        from io import BytesIO

        data = []
        for p in payrolls:
            total_salary = float(p.basic_salary or 0) + float(p.bonus or 0) - float(p.deductions or 0)
            data.append({
                'Employee': f"{p.employee.first_name} {p.employee.last_name}",
                'Month': p.month,
                'Basic Salary': p.basic_salary,
                'Bonus': p.bonus,
                'Deductions': p.deductions,
                'Total Salary': total_salary
            })

        df = pd.DataFrame(data)
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Payroll')
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="monthly_payroll_report.xlsx"'
        return response
