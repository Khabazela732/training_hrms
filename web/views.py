from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path
from . import views
from django.template import loader
from django.http import HttpResponse
from authenication.models import CustomUser as User
from hr.models import Job, Candidate


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
        Candidate.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            applied_job=job,
            current_stage='Applied'
        )
        return redirect('home') 

    return render(request, 'web/job_detail.html', {'job': job})