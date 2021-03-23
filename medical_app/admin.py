# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from medical_app.models import Doctor, MedicalService, Cabinet, Specification, Schedules, Date, Hospital, Department


class SchedulesAdmin(admin.ModelAdmin):
    list_display = ['doc_id', 'cab_id', 'date', 'time', 'busy']

admin.site.register(Doctor)
admin.site.register(Date)
admin.site.register(MedicalService)
admin.site.register(Cabinet)
admin.site.register(Specification)
admin.site.register(Schedules, SchedulesAdmin)
admin.site.register(Hospital)
admin.site.register(Department)