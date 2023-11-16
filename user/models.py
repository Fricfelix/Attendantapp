


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile_picture_url = models.URLField(blank=True)
    email_confirmation_token = models.CharField(max_length=36, default=None, editable=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    reset_password_token = models.CharField(max_length=255,blank=True,null=True)
    reset_password_token_created_time = models.DateTimeField(blank=True,null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    # device_ip_address = models.CharField(max_length=255,blank=True,null=True)


    def save(self,*args, **kwargs):
        if not self.email_confirmation_token:
            self.email_confirmation_token = uuid.uuid4().hex
        super().save(*args,**kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name
