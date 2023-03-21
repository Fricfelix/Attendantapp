from django.db import models
import datetime
import uuid
from django.utils import timezone
from django.conf import settings

# Create your models here.

class StudentAttendanceCreationModel(models.Model):
	identifier = models.SlugField(max_length=36, unique=True)
	attendanceTitle = models.CharField(max_length=120,default='Title')
	location_point_range = models.FloatField(default=100.00,null=True)
	
	# default is a string-----======
	attendance_duration = models.DateTimeField(default=(timezone.localtime(timezone.now()) + datetime.timedelta(hours=24)),null=True)
	longitude = models.FloatField(null=True)
	latitude = models.FloatField(null=True)
	datetime_created = models.DateTimeField(auto_now_add=True)

	def timer(self):
		now = timezone.now()
		if self.attendance_duration > now:
			time_remaining = self.attendance_duration - now
			return time_remaining
		else:
			return datetime.timedelta(0)

	def save(self, *args, **kwargs):
		if not self.identifier:
			self.identifier = str(uuid.uuid4())
		super().save(*args, **kwargs)

	def __str__(self):
		return self.attendanceTitle


class StudentAttendanceTakingModel(models.Model):
	attendance = models.ForeignKey(StudentAttendanceCreationModel,on_delete=models.CASCADE)
	name = models.CharField(max_length=120)
	reg_number = models.CharField(max_length=120)
	department = models.CharField(max_length=200 ,null=True)
	time_of_attendance = models.DateTimeField(default=datetime.datetime.now)

	
	def __str__(self):
		return self.name





class OfficeAttendanceCreationModel(models.Model):
	identifier = models.SlugField(max_length=36, unique=True)
	attendanceTitle = models.CharField(max_length=120,default='Title')
	location_point_range = models.FloatField(default=100.00,null=True)
	attendance_duration = models.DateTimeField(default=(timezone.localtime(timezone.now()) + datetime.timedelta(hours=24)),null=True)
	longitude = models.FloatField(null=True)
	latitude = models.FloatField(null=True)
	datetime_created = models.DateTimeField(auto_now_add=True)

	def timer(self):
		now = timezone.now()
		if self.attendance_duration > now:
			time_remaining = self.attendance_duration - now
			return time_remaining
		else:
			return datetime.timedelta(0)

	def save(self, *args, **kwargs):
		if not self.identifier:
			self.identifier = str(uuid.uuid4())	

		super().save(*args, **kwargs)
    
	def __str__(self):
		return self.attendanceTitle



class OfficeAttendanceTakingModel(models.Model):
	attendance = models.ForeignKey(OfficeAttendanceCreationModel,on_delete=models.CASCADE)
	name = models.CharField(max_length=120)
	position = models.CharField(max_length=120)
	time_of_attendance = models.DateTimeField(default=datetime.datetime.now)

	def __str__(self):
		return self.name



