from __future__ import unicode_literals

from django.contrib import admin

from main.models import Volunteer, School, State, District, SubDistrict, Registration

from six import text_type
from typing import Mapping, Tuple

class RegistrationInline(admin.TabularInline):
    model = Registration

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('aadharid', 'name', 'volunteer_type', 'phone', 'gender',
        'subdistrict', 'state')
    search_fields = ('=aadharid', 'name', 'email', 'base_address', 'skills', 'school__name',
        'subdistrict__name', 'subdistrict__district__name')
    list_filter = ('gender', 'school__school_type', 'subdistrict__district__state__name')
    radio_fields = {'gender': admin.VERTICAL}
    inlines = (RegistrationInline,)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'school_type', 'base_address', 'subdistrict', 'phone')
    search_fields = ('name', 'base_address', 'counsellor_name', 'subdistrict__name',
        'subdistrict__district__name')
    list_filter = ('school_type', 'subdistrict__district__state__name',)
    radio_fields = {'school_type': admin.VERTICAL}

class StateAdmin(admin.ModelAdmin):
    list_display = ('scode', 'name',)
    search_fields = ('name',)

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('pin', 'name', 'state')
    search_fields = ('name', 'state__name')
    list_filter = ('state__name',)

class SubDistrictAdmin(admin.ModelAdmin):
    list_display = ('pin', 'name', 'district')
    search_fields = ('name', 'district__name')
    list_filter = ('district__state__name',)

admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(SubDistrict, SubDistrictAdmin)
