from django.contrib import admin
from .models import Patient, Helper, Request
# Register your models here.
admin.site.register(Patient)
admin.site.register(Helper)
admin.site.register(Request)