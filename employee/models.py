from django.db import models
from django.contrib.auth.models import User
from hr.models import Department, Role

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"