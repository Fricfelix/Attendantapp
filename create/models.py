from django.db import models
import datetime

# Create your models here.

class StudentAttendanceModel(models.Model):
	name = models.CharField(max_length=120)
	reg_number = models.CharField(max_length=120)
	department = models.CharField(max_length=200 ,blank=True)
	time_of_attendance = models.DateTimeField(default=datetime.datetime.now)

class OfficeAttendanceModel(models.Model):
	name = models.CharField(max_length=120)
	position = models.CharField(max_length=120)
	time_of_attendance = models.DateTimeField(default=datetime.datetime.now)
