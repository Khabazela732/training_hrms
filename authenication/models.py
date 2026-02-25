from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    role_choices = (
        ('admin', 'Admin'),
        ('hr_manager', 'HR Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=20, choices=role_choices)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
