from django import forms


# class SelectForm(forms.Form):
# 	SELECT_CHOICES = [
# 		("Student Attendat form","student"),
# 		("Office Attendat form","office")
# 	]

# 	select = forms.ChoiceField(choices=SELECT_CHOICES,
# 		label="Please select Attendant type",required=True)


class StudentForm(forms.Form):
	name = forms.CharField(required=True,max_length=100)
	reg_number = forms.CharField(required=True,max_length=50)
	department = forms.CharField(required=False,max_length=250)


class OfficeForm(forms.Form):
	name = forms.CharField(required=True,max_length=100)
	position = forms.CharField(required=True,max_length=50)
