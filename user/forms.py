

from django import forms
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMessage
from django.conf import settings

from django.contrib.auth.forms import UserCreationForm
import cloudinary.uploader
from .models import UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)


    class Meta:
        model = UserProfile
        fields = ('name', 'email', 'profile_picture', 'password1', 'password2')

    profile_picture = forms.FileField()


    

    

    def save(self, commit=True):
        user = super().save(commit=False)
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            uploaded_image = cloudinary.uploader.upload(profile_picture)
            user.profile_picture_url = uploaded_image['secure_url']
        if commit:
            user.save()
        return user


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your email address'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address does not exist")
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        user = UserProfile.objects.filter(email=email).first()
        if user and not user.is_active:
            raise forms.ValidationError('This account is not active')
        return cleaned_data

class CustomPasswordConfirmForm(forms.Form):
    new_password = forms.CharField(max_length=32, widget=forms.PasswordInput, required=True)
    new_password_confirm = forms.CharField(max_length=32, widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')

       
        new_password_confirm = cleaned_data.get('new_password_confirm')
        if new_password and new_password_confirm and new_password != new_password_confirm:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data

    def save(self,user):
        password = self.cleaned_data['new_password']
        user.set_password(password)

