from __future__ import unicode_literals

from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet

from main.models import Volunteer, School, State, District, SubDistrict, Registration

from six import text_type
from typing import Mapping, Sequence, Tuple

class RegistrationInline(admin.TabularInline):
    model = Registration

class VTypeListFilter(admin.SimpleListFilter):
    title = "Volunteer Type"
    parameter_name = 'vtype'

    def lookups(self, request, model_admin):
        # type: (HttpRequest, admin.ModelAdmin) -> Sequence[Tuple[text_type, text_type]]
        return (
            ('J', "Junior"),
            ('Y', "Youth"),
            ('C', "Community"),
        )

    def queryset(self, request, queryset):
        # type: (HttpRequest, QuerySet[Volunteer]) -> QuerySet[Volunteer]
        if self.value() == 'C':
            return queryset.filter(school__isnull=True)
        elif self.value():
            return queryset.filter(school__school_type=self.value())

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('aadharid', 'name', 'volunteer_type', 'phone', 'gender',
        'subdistrict', 'state')
    search_fields = ('=aadharid', 'name', 'email', 'base_address', 'skills', 'school__name',
        'subdistrict__name', 'subdistrict__district__name')
    list_filter = ('gender', VTypeListFilter, 'subdistrict__district__state__name')
    radio_fields = {'gender': admin.VERTICAL}
    inlines = (RegistrationInline,)
    raw_id_fields = ('school', 'subdistrict', 'perm_subdistrict')

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'school_type', 'base_address', 'subdistrict', 'phone')
    search_fields = ('name', 'base_address', 'counsellor_name', 'subdistrict__name',
        'subdistrict__district__name')
    list_filter = ('school_type', 'subdistrict__district__state__name',)
    radio_fields = {'school_type': admin.VERTICAL}
    raw_id_fields = ('subdistrict',)

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
    raw_id_fields = ('district',)

admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(SubDistrict, SubDistrictAdmin)
