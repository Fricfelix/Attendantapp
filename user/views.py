from django.shortcuts import render,redirect
from django.http import HttpResponse ,request 
from django.core.mail import send_mail,EmailMessage
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
import cloudinary.uploader
from user.forms import SignUpForm,LogInForm
from django.contrib import messages
from . models import User
from django.forms import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from django.urls import reverse
import uuid
from django.utils import timezone

# Create your views here.

def send_confirmation_email(user,request):
	current_site = get_current_site(request)
	uid = urlsafe_base64_encode(force_bytes(user.pk))
	token = user.email_confirmation_token
	confirmation_url = request.build_absolute_uri(reverse('confirm_email',kwargs={'uidb64':uid,'token':token}))
	subject = "Please confirm email to activate your account"
	message = render_to_string('comfirm-email.html',{'user':user,'domain':current_site.domain,'confirmation_url':confirmation_url})
	
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [user.email]
	send_mail = EmailMessage(subject,message,email_from,recipient_list)
	send_mail.content_type = 'html'
	send_mail.send()



def signup(request,*args,**kwargs):
	if request.method == 'POST':
		form = SignUpForm(request.POST,request.FILES)
		if form.is_valid():
			name  = form.cleaned_data['name']
			email = form.cleaned_data['email']
			profile_image = form.cleaned_data['profile_image']

			# Store the uploaded image in  cloudinary the get the image cloudinary url
			image_upload = cloudinary.uploader.upload(profile_image,folder="profile_image")
			profile_image_url = image_upload['secure_url']

			password = form.cleaned_data['password']
			confirm_password =form.cleaned_data['confirm_password']
			user = User(name=name,email=email,profile_image_url=profile_image_url)
			user.set_password(password)
			user.is_active = False
			user.save()
			send_confirmation_email(user,request)
			# REDIRECT TO A SUCCESS PAGE TELLING THE USER TO COMFIRM EMAIL WILL HAVE A COMFIRM EMAIL LOGIG
			messages.success(request, "Account created successfuly. Please check your email to comfirm your account")

			return redirect('login')

	else:
		form = SignUpForm()
	return render(request,'signup.html',{'form':form})




def login(request):
	if request.method == 'POST':
		form = LogInForm(request.POST)
		if form.is_valid():
			authenticate_user = authenticate(request,email=form.cleaned_data['email'],password=form.cleaned_data['password'])
			if authenticate_user is not None:

				login(request, authenticate_user)
				return redirect('home')
			else:
				form.add_error(None,'Invalid login credentials')

	else:
		form = LogInForm()
	return render(request,'login.html',{'form':form})

	


def logout(request):
	logout(request)
	return redirect('home')


def confirm_email(request,uidb64,token):
	User = get_user_model()
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = User.objects.get(pk=uid)
	except:
		user = None

	if user is not None and user.email_confirmation_token==token:
		# check if the confirmation link has expired
		token_time = uuid.UUID(token).time
		current_time = timezone.now().timestamp()
		if current_time - token_time<=24 * 60 * 60:
			user.email_confirmed = True
			user.is_active = True
			user.save()
			messages.success(request,"your email has been confirmed.thanks for signing up!.")
			return redirect('login')

		else:
			messages.error(request,'The confirmation link has expird')
	else:
		messages.error(request,'The confirmation link was invalid ')
	return redirect('home')