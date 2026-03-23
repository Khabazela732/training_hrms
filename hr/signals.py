from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from hr.models import Achievement

@receiver(post_save, sender=Achievement)
def send_achievement_email(sender, instance, created, **kwargs):
    if not created:
        return

    employee = instance.employee

    if not employee.email:
        return

    # ✅ FIX: No Site framework
    base_url = "http://127.0.0.1:8000"  # change later for production

    certificate_url = f"{base_url}{reverse('download_certificate', args=[instance.id])}"

    # ✅ Build message FIRST (your previous bug was here)
    if instance.achievement_type == 'employee_of_the_month':
        subject = "🎉 Employee of the Month"
        message = f"""
Hi {employee.first_name},

Congratulations! You are Employee of the Month.

Download your certificate:
{certificate_url}
"""

    elif instance.achievement_type == 'service_awards':
        subject = "🎖️ Service Award"
        message = f"""
Hi {employee.first_name},

Congratulations on your {instance.description}!

Download your certificate:
{certificate_url}
"""

    elif instance.achievement_type == 'certification':
        subject = "📜 Certification"
        message = f"""
Hi {employee.first_name},

You earned: {instance.description}

Download your certificate:
{certificate_url}
"""
    else:
        return

    # ✅ Send email ONCE
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [employee.email],
        fail_silently=False,
    )