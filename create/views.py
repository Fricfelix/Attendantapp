from django.shortcuts import render,redirect

from .forms import StudentForm, OfficeForm
from .models import StudentAttendanceModel, OfficeAttendanceModel

# Create your views here.

def create_view(request,*args,**kwargs):
	if request.method == "POST":

		student_form = StudentForm(request.POST or None,prefix="studentform")
		office_form = OfficeForm(request.POST or None,prefix="officeform")

		if 'student_form' in request.POST:
			if student_form.is_valid():
				name = student_form.cleaned_data['name']
				reg_number = student_form.cleaned_data['reg_number']
				department = student_form.cleaned_data['department']

			# create a new instance of the first model 
				studentModelInstance = StudentAttendanceModel(name=name,reg_number=reg_number,department=department)
			# save the instace to the database 
				studentModelInstance.save()
				return redirect(request.path)

		elif 'office_form' in request.POST:
			if office_form.is_valid():
				name = office_form.cleaned_data['name']
				position = office_form.cleaned_data['position']
				officeModelInstance = OfficeAttendanceModel(name=name,position=position)
				officeModelInstance.save()
				return redirect(request.path)
	else:
		student_form = StudentForm(prefix="studentform")
		office_form = OfficeForm(prefix="officeform")

	context ={
		'student_form':student_form,
		'office_form' :office_form,
	}
	return render(request , 'create.html',context)

