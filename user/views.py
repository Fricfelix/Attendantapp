


from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.urls import reverse_lazy

from user.forms import SignUpForm,FaceRecognitionForm
from django.conf import settings
import cloudinary.uploader
from . models import UserProfile
from django.contrib import messages
import uuid
from .forms import CustomPasswordResetForm,CustomPasswordConfirmForm
from django.utils import timezone 


from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import views as auth_views

from datetime import datetime, timedelta




def custom_password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        
        if form.is_valid():

            email = form.cleaned_data.get('email')
            existing_user = UserProfile.objects.filter(email=email).first()
            if existing_user:
                domain = get_current_site(request)
                reset_password_token = default_token_generator.make_token(existing_user)
                existing_user.reset_password_token = reset_password_token
                existing_user.reset_password_token_created_time = datetime.now()
                existing_user.save()
                reset_password_url = request.build_absolute_uri(reverse('custom_password_reset_confirm',kwargs={'uidb64':urlsafe_base64_encode(force_bytes(existing_user.pk)),'token':reset_password_token}))
                subject = 'Reset your password'
                message = render_to_string('password_reset_email_template.html',{'domain':domain,'reset_password_url':reset_password_url,'user':existing_user.name})
                sendmail = EmailMessage(subject,message,settings.EMAIL_HOST_USER,[existing_user.email])
                sendmail.content_type ='html'
                sendmail.send()
                messages.success(request,'Instructions on password reset has been sent to your email')
                form = CustomPasswordResetForm()
                return render(request,'password_reset.html',{'form':form})
            
            form.add_error('email','User not found ')
        messages.error(request,'Invalid Email')   
    form = CustomPasswordResetForm()
    return render(request,'password_reset.html',{'form':form})



def custom_password_reset_confirm(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserProfile.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomPasswordConfirmForm(data=request.POST)
            if form.is_valid():
                form.save(user = user)
                user.reset_password_token = None
                user.save()
                messages.success(request, 'Password has been reset. You can now login with your new password')
                return redirect('login')
            messages.error(request,'Password does not match')
        
        form = CustomPasswordConfirmForm()
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'Invalid password reset link')
        return redirect('login')



# SIGN UP ,LOGIN AND CONFIRMATION EMAIL VIEWS


def send_confirmation_email(user,request):
  current_site = get_current_site(request)
  uid = urlsafe_base64_encode(force_bytes(user.pk))
  token = default_token_generator.make_token(user)
  confirmation_url = request.build_absolute_uri(reverse('confirm_email',kwargs={'uid':uid,'token':token}))
  subject = "Please confirm email to activate your account"
  message = render_to_string('confirm-email.html',{'user':user,'domain':current_site.domain,'confirmation_url':confirmation_url})
    
  email_from = settings.EMAIL_HOST_USER
  recipient_lists = [user.email]
  send_mail = EmailMessage(subject,message,email_from,recipient_lists)
  send_mail.content_type = 'html'
  send_mail.send()


def email_confirmation_requierd(view_func):
    def view(request,*args,**kwargs):
        if request.method=='POST':
            email = request.POST.get('email')
            if UserProfile.objects.filter(email=email,is_active=False).exists():
                existing_user = UserProfile.objects.get(email=email)
                send_confirmation_email(existing_user,request)
                messages.error(request ,'Inactive User, email confirmation has be sent Please confirm email')
                return redirect(reverse('signup'))
        return view_func(request,*args,**kwargs)
    return view 





@email_confirmation_requierd
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = form.save(commit=False)

            # Check if user already exists but is inactive
            try:
                existing_user = UserProfile.objects.get(email=email)
                if not existing_user.is_active:
                    send_confirmation_email(existing_user, request)
                    messages.info(request, "An email has been sent to confirm your account. Please check your email.")
                    return redirect('login')
                else:
                    messages.error(request, "This email address has already been registered.")
                    return redirect('login')
            except UserProfile.DoesNotExist:
                pass

            # New user, save and send confirmation email
            user.is_active = False
            user.save()
            send_confirmation_email(user, request)
            messages.success(request, "Account created successfully. Please check your email to confirm your account.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'user/register.html', {'form': form})



def confirm_email(request, uid, token):
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = UserProfile.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,"your email has been confirmed.Login to continue.")
        return redirect('login')
    messages.error(request,'The confirmation link was invalid ')
    return redirect('home')





@email_confirmation_requierd
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    
        messages.error(request,'Invalid Email or Password')
        form = AuthenticationForm()
        return render(request,'login.html',{'form':form})

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def recognize_faces(request):
    if request.method == 'POST':
        form = FaceRecognitionForm(request.POST)
        if form.is_valid():
            processed_image = form.recognize_faces()
            return JsonResponse({'result': processed_image.decode('utf-8')})
    else:
        form = FaceRecognitionForm()
    return render(request, 'facial_recognition.html', {'form': form})




def logout(request):
    auth_logout(request)
    return redirect('home')




