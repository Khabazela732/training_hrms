from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from hr.models import Employee, Attendance, Leave, Payroll, Performance
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Count, Avg

class EmployeeDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        
        if getattr(user, "role", None) != "employee":
            return render(request, "employee/pages/dashboard.html", {"error": "Access restricted to employees."})

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
            payroll_status = f"EUR {latest_payroll.total_salary():,.2f} - {latest_payroll.month}"
        else:
            payroll_status = "No payroll records"
        
        avg_performance = Performance.objects.filter(
            employee=employee
        ).aggregate(avg_rating=Avg('rating'))['avg_rating']
        
        performance_rating = f"{avg_performance:.1f}/5" if avg_performance else "No reviews"

        recent_attendance = Attendance.objects.filter(
            employee=employee
        ).order_by("-date", "-id")[:7]

        recent_leaves = Leave.objects.filter(
            employee=employee
        ).order_by("-start_date", "-id")[:5]

        recent_payrolls = Payroll.objects.filter(
            employee=employee
        ).order_by("-created_at", "-id")[:3]

        recent_performance = Performance.objects.filter(
            employee=employee
        ).order_by("-created_at", "-id")[:3]

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

            'recent_attendance': recent_attendance,
            'recent_leaves': recent_leaves,
            'recent_payrolls': recent_payrolls,
            'recent_performance': recent_performance,
        }
        
        return render(request, 'employee/pages/dashboard.html', context)
