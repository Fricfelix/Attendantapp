from django.contrib import admin

# Register your models here.

from .models import StudentAttendanceModel,OfficeAttendanceModel

admin.site.register(StudentAttendanceModel)
admin.site.register(OfficeAttendanceModel)
