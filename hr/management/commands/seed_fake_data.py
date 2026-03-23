from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from hr.models import Employee, Department, Role, Performance, Achievement
from datetime import date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Seed fake employees, performances, and achievements"

    def handle(self, *args, **kwargs):

        if not Department.objects.exists() or not Role.objects.exists():
            self.stdout.write(self.style.ERROR("Create at least 1 Department and 1 Role first!"))
            return

        departments = list(Department.objects.all())
        roles = list(Role.objects.all())

        first_names = [
            "Liam", "Noah", "Ethan", "James", "Daniel",
            "Thabo", "Sipho", "Lerato", "Ayanda", "Zanele",
            "Michael", "David", "Chris", "Nathan", "Ryan"
        ]

        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones",
            "Mokoena", "Nkosi", "Dlamini", "Khumalo", "Ndlovu",
            "Naidoo", "Pillay", "Van der Merwe", "Botha", "Jacobs"
        ]

        for i in range(5):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)

            clean_last_name = last_name.lower().replace(" ", "").replace("'", "")
            clean_first_name = first_name.lower().replace(" ", "")

            username = f"{clean_first_name}{clean_last_name}{random.randint(100,999)}"

            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': f"{username}@test.com"
                }
            )

            service_years_options = [1, 3, 5]
            service_years = random.choice(service_years_options)
            extra_days = random.randint(0, 364)
            hire_date = date.today() - timedelta(days=(365 * service_years + extra_days))

            employee, _ = Employee.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'department': random.choice(departments),
                    'role': random.choice(roles),
                    'date_joined': hire_date
                }
            )

            rating = round(random.uniform(2.0, 5.0), 1)
            Performance.objects.get_or_create(
                employee=employee,
                department=employee.department,
                role=employee.role.name if hasattr(employee.role, 'name') else 'Employee',
                rating=rating,
                remarks="Fake performance for testing."
            )

            Achievement.objects.get_or_create(
                employee=employee,
                achievement_type='employee_of_the_month',
                description='Top performer of the month',
                date_awarded=date.today() - timedelta(days=random.randint(1, 60))
            )

            years_of_service = (date.today() - employee.date_joined).days // 365
            if years_of_service in [1, 2, 5]:
                Achievement.objects.get_or_create(
                    employee=employee,
                    achievement_type='service_awards',
                    description=f'{years_of_service} years of service',
                    date_awarded=date.today()
                )

            certifications_by_department = {
                "Software Dev": [
                    "React Beginner Certification",
                    "React Intermediate Certification",
                    "React Advanced Certification",
                    "Angular Certification"
                ],
                "IT Support": ["CompTIA A+", "Network+"],
                "Cybersecurity": ["CEH", "Security+"],
                "Finance & Accounting": ["SAP Certification"],
                "HR": ["HR Management Certification"]
            }

            dept_name = employee.department.name
            cert_list = certifications_by_department.get(dept_name, ["General Certification"])
            cert_name = random.choice(cert_list)

            Achievement.objects.get_or_create(
                employee=employee,
                achievement_type='certification',
                description=cert_name,
                date_awarded=date.today() - timedelta(days=random.randint(1, 180))
            )

        self.stdout.write(self.style.SUCCESS("Fake employees and achievements created successfully!"))