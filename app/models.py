from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Helper(models.Model):
    helper_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name


class Request(models.Model):
    FLOOR_CHOICES = [
        ('ground', 'Ground Floor'),
        ('basement1', 'Basement 1'),
        ('basement2', 'Basement 2'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    helper = models.ForeignKey(Helper, on_delete=models.SET_NULL, null=True, blank=True)
    
    floor = models.CharField(max_length=20, choices=FLOOR_CHOICES)
    time_to_reach = models.DateTimeField()
    
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.name} - {self.floor}"