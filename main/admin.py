from __future__ import unicode_literals

from django.contrib import admin

from main.models import Volunteer, School, State, District, SubDistrict, Registration

from six import text_type
from typing import Mapping, Tuple

class RegistrationInline(admin.StackedInline):
    model = Registration

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('aadharid', 'name', 'volunteer_type', 'phone', 'gender',
        'subdistrict', 'state')
    radio_fields = {'gender': admin.VERTICAL}
    inlines = (RegistrationInline,)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'school_type', 'base_address', 'subdistrict', 'phone')
    radio_fields = {'school_type': admin.VERTICAL}

class StateAdmin(admin.ModelAdmin):
    list_display = ('scode', 'name',)

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('pin', 'name', 'state')

class SubDistrictAdmin(admin.ModelAdmin):
    list_display = ('pin', 'name', 'district')

admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(SubDistrict, SubDistrictAdmin)
