from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path
from . import views
from django.template import loader
from django.http import HttpResponse
from authenication.models import CustomUser as User
from hr.models import Job, Candidate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def home(request):
    user = User.objects.first()
    jobs = Job.objects.filter(status='Open').order_by('-posted_date')  # only open jobs
    context = {
        'user': user,
        'jobs': jobs,
    }
    return render(request, 'web/home.html', context)


def job_detail_public(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        candidate = Candidate.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            applied_job=job,
            current_stage="Applied"
        )

        messages.success(request, f"You have successfully applied for {job.title} 🎉")
        message = render_to_string('hr/email/application_confirmation.html', {
            'candidate': candidate,
            'job': job
        })
        send_mail(
            subject="Application Received",
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=message
        )

        return redirect('job_detail_public', pk=job.pk)

    return render(request, 'web/job_detail.html', {'job': job})

def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        Candidate.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            applied_job=job,
            current_stage="Applied"
        )
        messages.success(request, f"You have successfully applied for {job.title}")
        return redirect('home')

    return render(request, 'web/apply_job.html', {'job': job})