from django.shortcuts import render,redirect

from .forms import StudentForm, OfficeForm,StudentAttendanceCreationForm,OfficeAttendanceCreationForm
from .models import ( StudentAttendanceCreationModel, 
OfficeAttendanceCreationModel, StudentAttendanceTakingModel, OfficeAttendanceTakingModel )
import geoip2
from django.contrib import messages
from django.urls import reverse
import datetime

# Create your views here.

# def attendance_links(request,identifier):

# 	context = {}
# 	try:
# 		studentattendance_id = StudentAttendanceCreationModel.objects.get(identifier=identifier)
# 		attendance_url = request.build_absolute_uri(reverse('student_take_attendance',args=[identifier]))
# 	except StudentAttendanceCreationModel.DoesNotExist:

# 		try:
# 			officeattendance_id = OfficeAttendanceCreationModel.objects.get(identifier=identifier)
# 			attendance_url = request.build_absolute_uri(reverse('office_take_attendance',args=[officeattendance_id]))
# 		except OfficeAttendanceCreationModel.DoesNotExist:
# 			attendance_url = None
# 	context['attendance_url'] = attendance_url
# 	return render(request,'links.html',context)



 

def create_attendance(request):
	if request.method == 'POST':
		if 'student_form' in request.POST:
			studentattendanceForm = StudentAttendanceCreationForm(request.POST or None,prefix='student_form')
			if studentattendanceForm.is_valid():
				latitude = request.POST.get('latitude')
				longitude = request.POST.get('longitude')
				attendanceTitle=studentattendanceForm.cleaned_data['attendanceTitle']
				location_point_range=studentattendanceForm.cleaned_data['location_point_range']
				attendance_duration=str(studentattendanceForm.cleaned_data['attendance_duration'])
				if not attendance_duration or attendance_duration=='':
					attendance_duration=datetime.timedelta(hours=24)
				else:
					attendance_duration=str(attendance_duration)
					if attendance_duration.startswith('1 day '):
						attendance_duration='1 day '+ attendance_duration[7:]
						attendance_duration=datetime.datetime.strptime(attendance_duration,'%d day %H:%M:%S')
				stdInstance = StudentAttendanceCreationModel(attendanceTitle=attendanceTitle,location_point_range=location_point_range,
																attendance_duration=attendance_duration
																,longitude=longitude,latitude=latitude)
				stdInstance.save()
				attendance_url = request.build_absolute_uri(reverse('student_take_attendance',args=[stdInstance.identifier]))
				context ={'attendance_url':attendance_url}

				return render(request, 'links.html',context)

		elif 'office_form' in request.POST:
			officeattendanceForm = OfficeAttendanceCreationForm(request.POST or None,prefix='office_form' )
			if officeattendanceForm.is_valid():
				latitude = request.POST.get('latitude')
				longitude = request.POST.get('longitude')
				attendanceTitle=officeattendanceForm.cleaned_data['attendanceTitle']
				location_point_range=officeattendanceForm.cleaned_data['location_point_range']
				attendance_duration=str(officeattendanceForm.cleaned_data['attendance_duration'])
				if not attendance_duration or attendance_duration=='':
					attendance_duration=datetime.timedelta(hours=24)
				else:
					attendance_duration=str(attendance_duration)
					if attendance_duration.startswith('1 day '):
						attendance_duration='1 day '+ attendance_duration[7:]
						attendance_duration=datetime.datetime.strptime(attendance_duration,'%d day %H:%M:%S')
				print(attendance_duration)
				offInstance = OfficeAttendanceCreationModel(attendanceTitle=attendanceTitle,
															location_point_range=location_point_range,
															attendance_duration=attendance_duration,longitude=longitude,latitude=latitude)
				offInstance.save()
				attendance_url = request.build_absolute_uri(reverse('office_take_attendance',args=[offInstance.identifier]))

				context={'attendance_url':attendance_url}
				return render(request, 'links.html',context)
		studentattendanceForm = StudentAttendanceCreationForm(request.POST or None,prefix='student_form')
		officeattendanceForm = OfficeAttendanceCreationForm(request.POST or None,prefix='office_form' )
		context={'studentattendanceForm':studentattendanceForm,'officeattendanceForm':officeattendanceForm}
		return render(request,'create.html',context)
	
	studentattendanceForm = StudentAttendanceCreationForm(request.POST or None,prefix='student_form')
	officeattendanceForm = OfficeAttendanceCreationForm(request.POST or None,prefix='office_form' )
	context = {'studentattendanceForm': studentattendanceForm,
        		'officeattendanceForm': officeattendanceForm}

	return render(request, 'create.html', context)

   




def student_take_attendance(request,identifier,*args,**kwargs):
	try:
		studentattendance_url = StudentAttendanceCreationModel.objects.get(identifier=identifier)
		student_form = StudentForm(request.POST or None,prefix="studentform")
		if student_form.is_valid():
			name = student_form.cleaned_data['name']
			reg_number = student_form.cleaned_data['reg_number']
			department = student_form.cleaned_data['department']

			# create a new instance of the first model
			studentModelInstance = StudentAttendanceTakingModel(attendance=studentattendance_url,name=name,reg_number=reg_number,department=department)
			studentModelInstance.save()
			return redirect('/')

	
		student_form = StudentForm(prefix="studentform")
		context ={
			'student_form':student_form,
			'studentattendance_url':studentattendance_url,
			}
		
		return render(request , 'student_take_attendance.html',context)

	except StudentAttendanceCreationModel.DoesNotExist:
		messages.error(request,"The url you requested does not exist or has the attendance time has ellapsed")
		
		return redirect('404.html')





def office_take_attendance(request,identifier,*args,**kwargs):
	try:
		officeattendance_ur = OfficeAttendanceCreationModel.objects.get(identifier=identifier)
		officeattendanceForm = OfficeForm(request.POST or None,prefix="officeform")
		
		if officeattendanceForm.is_valid():
			name = officeattendanceForm.cleaned_data['name']
			position = officeattendanceForm.cleaned_data['position']

			officeModelInstance = OfficeAttendanceTakingModel(attendance =officeattendance_ur,name=name,position=position)
			officeModelInstance.save()
			return redirect('/')

		office_form = OfficeForm(prefix="officeform")
		context ={
			'office_form':office_form,
			'officeattendance_ur':officeattendance_ur,
			}
		
		return render(request , 'office_take_attendance.html',context)

	except StudentAttendanceCreationModel.DoesNotExist:
		messages.error(request,"The url you requested does not exist or has the attendance time has ellapsed")
		
		return redirect('404.html')




def custom_404(request,exception):
	return render(request,'404.html',status=404)