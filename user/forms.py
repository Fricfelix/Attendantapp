from django import forms
from django.contrib.auth.hashers import make_password,check_password
from .models import User
from django.forms import ValidationError



class SignUpForm(forms.Form):
	name = forms.CharField(required=True,max_length=100)
	email = forms.EmailField(required=True)
	profile_image = forms.FileField(required=True,help_text='Required!.Upload a Photo of your face for recognition' )
	password = forms.CharField(required=True,max_length=32,widget=forms.PasswordInput)
	confirm_password = forms.CharField(required=True,max_length=32,widget=forms.PasswordInput)

	def clean_email(self):
		email = self.cleaned_data["email"]
		if User.objects.filter(email=email).exists():
			raise ValidationError("The Email address already exists! Try loging in ")
		return email


	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')

		if password != confirm_password:
			raise ValidationError("The passwords do not match")

		# Harsh the password befor saving to database
		hashed_password = make_password(password)
		cleaned_data['password'] = hashed_password


		return cleaned_data



class LogInForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(max_length=32, widget=forms.PasswordInput)
	confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput)

	def clean(self):
		cleaned_data = super().clean()
		email = cleaned_data.get('email')
		password = cleaned_data.get('password')

		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			raise forms.add_error('The Entered Email does not exist in our database')

		if not check_password(password,user.password):
			raise ValidationError('password','Incorrect password.')

		# IF Password and email matches add user object to cleaned data dictionary for use in the View

		cleaned_data['user'] = user 
		return cleaned_data

