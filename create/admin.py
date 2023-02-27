from django.contrib import admin

# Register your models here.

from .models import ( StudentAttendanceTakingModel,OfficeAttendanceTakingModel,StudentAttendanceCreationModel,
OfficeAttendanceCreationModel)

admin.site.register(StudentAttendanceTakingModel)
admin.site.register(OfficeAttendanceTakingModel)
admin.site.register(StudentAttendanceCreationModel)
admin.site.register(OfficeAttendanceCreationModel)
