from django.db import models
from authenication.models import CustomUser as User
    
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    @classmethod
    def bulk_create_departments(cls, department_data):
        """Bulk create departments from list of dicts"""
        departments = []
        for data in department_data:
            dept = cls(
                name=data['name'],
                description=data.get('description', '')
            )
            departments.append(dept)
        return cls.objects.bulk_create(departments)
    
class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='employee_profiles/', blank=True, null=True) #media/employee_profiles/
    contract_copy = models.FileField(upload_to='employee_contracts/', blank=True, null=True) #media/employee_contracts/

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Leave(models.Model):

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Declined", "Declined"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.employee.name} - {self.status}"


    
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']
    
    def _str_(self):
        return f"{self.employee} - {self.date} ({self.status})"
    

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    month = models.CharField(max_length=50)  
    created_at = models.DateTimeField(auto_now_add=True)

    def total_salary(self):
        return self.basic_salary + self.bonus - self.deductions

    def __str__(self):
        return f"{self.employee} - {self.month}"

    @property
    def net_pay(self):
        return (self.basic_salary or 0) + (self.bonus or 0) - (self.deductions or 0)

    class Meta:  
        unique_together = ('employee', 'month')

class Performance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  
    role = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.rating}"



