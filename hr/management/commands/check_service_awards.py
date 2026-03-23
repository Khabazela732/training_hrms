from django.core.management.base import BaseCommand
from hr.models import Employee, Achievement
from datetime import date

class Command(BaseCommand):
    help = 'Check for employee service milestones and create service awards'

    def handle(self, *args, **kwargs):
        milestone_years = [1, 3, 5, 10, 15, 20]
        today = date.today()

        for employee in Employee.objects.all():
            if not employee.date_joined:
                continue

            years_of_service = today.year - employee.date_joined.year

            if (today.month, today.day) < (employee.date_joined.month, employee.date_joined.day):
                years_of_service -= 1

            # 🔍 DEBUG PRINT (ADD HERE)
            self.stdout.write(f"{employee} → {years_of_service} years")

            # 👇 YOUR EXISTING LOGIC
            for milestone in milestone_years:
                if years_of_service >= milestone:
                    already_awarded = Achievement.objects.filter(
                        employee=employee,
                        achievement_type='service_awards',
                        description=f"{milestone} years of service"
                    ).exists()

                    if not already_awarded:
                        Achievement.objects.create(
                            employee=employee,
                            achievement_type='service_awards',
                            description=f"{milestone} years of service"
                        )

                        self.stdout.write(self.style.SUCCESS(
                            f"Service award created for {employee} ({milestone} years)"
                        ))