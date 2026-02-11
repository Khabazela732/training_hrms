from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=30) #string
    last_name = models.CharField(max_length=30) #string
    department = models.CharField(max_length=50)#string
    phone = models.CharField(max_length=15)#string
    amount = models.DecimalField(max_digits=10, decimal_places=2)#fault/decimal
    active = models.BooleanField(default=True)#boolean
    joined_date = models.DateField(auto_now_add=True)#date

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
