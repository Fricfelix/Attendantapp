from django import forms
import datetime
from django.utils import timezone


class StudentForm(forms.Form):
	name = forms.CharField(required=True,max_length=100)
	reg_number = forms.CharField(required=True,max_length=50)
	department = forms.CharField(required=False,max_length=250)


class OfficeForm(forms.Form):
	name = forms.CharField(required=True,max_length=100)
	position = forms.CharField(required=True,max_length=50)



class StudentAttendanceCreationForm(forms.Form):
	attendanceTitle = forms.CharField(required=True,max_length=250,label='Title Of Attendance')
	location_point_range = forms.FloatField(required=False,
		widget=forms.NumberInput(attrs={'step':'0.01','min':'0','max':'100'}),
		label="Range of attendance coverage (meters)")
	attendance_duration = forms.DateTimeField(required=False, widget =forms.DateTimeInput(attrs={'type':'datetime-local'}))

	def clean(self):
		cleaned_data = super().clean()
		location_point_range = cleaned_data.get('location_point_range')
		attendance_duration = cleaned_data.get('attendance_duration')
		if not location_point_range:
			cleaned_data['location_point_range']=100.00
		if not attendance_duration:
			cleaned_data['attendance_duration'] = timezone.now() + datetime.timedelta(hours=24)
		else:
			cleaned_data['attendance_duration']=timezone.make_aware(attendance_duration)
		return cleaned_data


class OfficeAttendanceCreationForm(forms.Form):
	attendanceTitle = forms.CharField(required=True,max_length=250,label='Attendance Title')
	location_point_range = forms.FloatField(required=False,
		widget=forms.NumberInput(attrs={'step':'0.01','min':'0','max':'100'}),
		label="Range of attendance coverage (meters)")
	attendance_duration = forms.DurationField(required=False, widget =forms.DateTimeInput(attrs={'type':'datetime-local'}))

	def clean(self):
		cleaned_data = super().clean()
		location_point_range = cleaned_data.get('location_point_range')
		attendance_duration = cleaned_data.get('attendance_duration')
		if not location_point_range:
			cleaned_data['location_point_range']=100.00
		if not attendance_duration:
			cleaned_data['attendance_duration'] = timezone.now() + datetime.timedelta(hours=24)

		else:
			cleaned_data['attendance_duration']=timezone.make_aware(attendance_duration)
			
		return cleaned_data



