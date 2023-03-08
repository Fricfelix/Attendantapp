from django.shortcuts import render,redirect

from .forms import StudentForm, OfficeForm,StudentAttendanceCreationForm,OfficeAttendanceCreationForm,IdentifierForm
from .models import ( StudentAttendanceCreationModel, 
OfficeAttendanceCreationModel, StudentAttendanceTakingModel, OfficeAttendanceTakingModel )
import geoip2
from django.contrib import messages
from django.urls import reverse
import datetime
from geopy.distance import distance 
from django.utils import timezone
from django.forms import DateTimeField
# Create your views here.




def create_attendance(request):
	if request.method == 'POST':
		if 'student_form' in request.POST:
			studentattendanceForm = StudentAttendanceCreationForm(request.POST or None,prefix='student_form')
			if studentattendanceForm.is_valid():
				latitude = request.POST.get('latitude')
				longitude = request.POST.get('longitude')
				attendanceTitle=studentattendanceForm.cleaned_data['attendanceTitle']
				location_point_range=studentattendanceForm.cleaned_data['location_point_range']
				attendance_duration=studentattendanceForm.cleaned_data['attendance_duration']
				
				stdInstance = StudentAttendanceCreationModel(attendanceTitle=attendanceTitle,location_point_range=location_point_range,
																attendance_duration=attendance_duration
																,longitude=longitude,latitude=latitude)
				stdInstance.save()
				attendance_url = request.build_absolute_uri(reverse('student_take_attendance',args=[stdInstance.identifier]))
				context ={'attendance_url':attendance_url,'identifier':stdInstance.identifier}
				messages.success(request, 'Attendance created ')

				return render(request, 'links.html',context)

		elif 'office_form' in request.POST:
			officeattendanceForm = OfficeAttendanceCreationForm(request.POST or None,prefix='office_form' )
			if officeattendanceForm.is_valid():
				latitude = request.POST.get('latitude')
				longitude = request.POST.get('longitude')
				attendanceTitle=officeattendanceForm.cleaned_data['attendanceTitle']
				location_point_range=officeattendanceForm.cleaned_data['location_point_range']
				attendance_duration=officeattendanceForm.cleaned_data['attendance_duration']
				
				offInstance = OfficeAttendanceCreationModel(attendanceTitle=attendanceTitle,
															location_point_range=location_point_range,
															attendance_duration=attendance_duration,longitude=longitude,latitude=latitude)
				offInstance.save()
				attendance_url = request.build_absolute_uri(reverse('office_take_attendance',args=[offInstance.identifier]))

				context={'attendance_url':attendance_url,'identifier':offInstance.identifier}
				return render(request, 'links.html',context)
		
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
			'attendance_title':studentattendance_url.attendanceTitle
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
			'attendance_title':officeattendance_ur.attendanceTitle
			
			}
		
		return render(request , 'office_take_attendance.html',context)

	except StudentAttendanceCreationModel.DoesNotExist:
		messages.error(request,"The url you requested does not exist or has the attendance time has ellapsed")
		
		return redirect('404.html')




def attendance_identifier(request):
    if request.method == "POST":
        identifier_code = IdentifierForm(request.POST)
        if identifier_code.is_valid():
            identifier = identifier_code.cleaned_data['identifier']
            try:
                stdidentifier = StudentAttendanceCreationModel.objects.get(identifier=identifier)
                return redirect('student_take_attendance', identifier=identifier)
            except StudentAttendanceCreationModel.DoesNotExist:
            	pass
            

            try:
                offidentifier = OfficeAttendanceCreationModel.objects.get(identifier=identifier)
                return redirect('office_take_attendance', identifier=identifier)
            except OfficeAttendanceCreationModel.DoesNotExist:
            	messages.error(request,"It seems the code you provided does not exist, please check the code and try again")
            return redirect ("/attendance_identifier")
    else:
        identifierform = IdentifierForm()
        context = {'identifierform': identifierform}
        return render(request, 'identifier.html', context)






def custom_404(request,exception):
	return render(request,'404.html',status=404)