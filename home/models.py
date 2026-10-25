from django.db import models

# Create your models here.

class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name