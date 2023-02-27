"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from home.views import home_view
from create.views import student_take_attendance,create_attendance,office_take_attendance,custom_404
from user.views import user_view
from login.views import login_view
from logout.views import logout_view
from about.views import about_view
from contact.views import contact_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view, name='home'),
    path('404',custom_404, name='custom_404'),
    path('office_take_attendance/<slug:identifier>/',office_take_attendance, name='office_take_attendance'),
    path('student_take_attendance/<slug:identifier>/',student_take_attendance, name='student_take_attendance'),
    path('create',create_attendance, name='create_attendance'),
    path('user',user_view, name='user'),
    path('about',about_view, name='about'),
    path('login',login_view, name='login'),
    path('logout',logout_view, name='logout'),
    path('contact',contact_view, name='contact'),

]

if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)