from __future__ import unicode_literals

import datetime
from django.db import models
from django.core.validators import RegexValidator

from six import text_type, python_2_unicode_compatible
from typing import Any, Optional, Tuple
from lib import mypy_dummy

address_help_text = """Please don't include your district, city, state in your address.
That will be extracted from your Sub-district/PIN code"""

@python_2_unicode_compatible
class State(models.Model):
    scode = models.CharField('State Code', max_length=3, primary_key=True) # type: text_type
    name = models.CharField('State Name', max_length=30, unique=True) # type: text_type

    objects = mypy_dummy.dummyStateManager()
    class Meta(object):
        db_table = 'State'

    def __str__(self):
        # type: () -> str
        return self.name # type: ignore

@python_2_unicode_compatible
class District(models.Model):
    pin = models.PositiveIntegerField('District PIN', primary_key=True) # type: int
    name = models.CharField('District Name', max_length=60, blank=True) # type: text_type
    state = models.ForeignKey(State) # type: State

    objects = mypy_dummy.dummyDistrictManager()
    class Meta(object):
        db_table = 'District'

    def __str__(self):
        # type: () -> str
        return "{} ({}, {})".format(self.pin, self.name or "-", self.state.name) # type: ignore

@python_2_unicode_compatible
class SubDistrict(models.Model):
    pincode = models.PositiveIntegerField('PIN Code', primary_key=True)
    pin = models.PositiveIntegerField('Sub-District PIN') # type: int
    name = models.CharField('Sub-District Name', max_length=60, blank=True) # type: text_type
    district = models.ForeignKey(District) # type: District

    objects = mypy_dummy.dummySubDistrictManager()
    class Meta(object):
        db_table = 'SubDistrict'
        unique_together = (('pin', 'district'),)

    def get_pincode(self):
        # type: () -> int
        return self.pin + self.district.pin * 1000

    def __str__(self):
        # type: () -> str
        name = self.name or "-"
        district = self.district.name or "-"
        state = self.district.state.name or "-"
        return "{} ({}, {}, {})".format(self.pincode, name, district, state) # type: ignore

    def save(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        self.pincode = self.get_pincode()
        super(SubDistrict, self).save(*args, **kwargs)

SCHOOL_CHOICES = (
    ('S', 'School'),
    ('C', 'College'),
) # type: Tuple[Tuple[text_type, text_type], ...]

@python_2_unicode_compatible
class School(models.Model):
    id = 0 # type: int
    name = models.CharField('School Name', max_length=30) # type: text_type
    school_type = models.CharField('Type', max_length=1, choices=SCHOOL_CHOICES) # type: text_type
    base_address = models.CharField('Address', max_length=250,
        help_text=address_help_text) # type: text_type
    subdistrict = models.ForeignKey(SubDistrict, verbose_name='Sub-District',
        null=True) # type: Optional[SubDistrict]
    phone = models.BigIntegerField(unique=True) # type: int
    principal_name = models.CharField("Principal's name", max_length=100) # type: text_type
    counsellor_name = models.CharField("Counsellor's name", max_length=100) # type: text_type
    counsellor_phone = models.BigIntegerField("Counsellor's phone", null=True,
        blank=True) # type: Optional[int]

    objects = mypy_dummy.dummySchoolManager()
    class Meta(object):
        db_table = 'School'
        verbose_name = 'School/College'

    def __str__(self):
        # type: () -> str
        return "{}: {}".format(self.id, self.name) # type: ignore

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
) # type: Tuple[Tuple[text_type, text_type], ...]

AADHAR_LENGTH = 12

@python_2_unicode_compatible
class Volunteer(models.Model):
    id = 0 # type: int
    create_stamp = models.DateTimeField('Created', auto_now_add=True) # type: datetime.datetime
    update_stamp = models.DateTimeField('Last Updated', auto_now=True) # type: datetime.date

    name = models.CharField(max_length=100) # type: text_type
    aadharid = models.CharField('Aadhar ID', max_length=AADHAR_LENGTH, unique=True,
        validators=[RegexValidator(regex=r'\d{%s}' % (AADHAR_LENGTH,), message='Invalid Aadhar ID')]) # type: int
    phone = models.BigIntegerField() # type: int

    gender = models.CharField(max_length=2, choices=GENDER_CHOICES) # type: text_type
    dob = models.DateField('Date of birth', null=True) # type: Optional[datetime.datetime]
    email = models.EmailField(blank=True) # type: text_type
    skills = models.CharField(max_length=100, blank=True) # type: text_type
    base_address = models.CharField('Address', max_length=250, help_text=address_help_text) # type: text_type
    subdistrict = models.ForeignKey(SubDistrict, verbose_name='Sub-District', null=True,
        related_name="volunteer_set") # type: Optional[SubDistrict]
    perm_base_address = models.CharField('Permanent Address', max_length=250,
        help_text=address_help_text) # type: text_type
    perm_subdistrict = models.ForeignKey(SubDistrict, verbose_name='Permanent Sub-Discrict',
        null=True, related_name="perm_volunteer_set") # type: Optional[SubDistrict]
    school = models.ForeignKey(School, verbose_name="School/College", null=True, blank=True) # type: Optional[School]

    objects = mypy_dummy.dummyVolunteerManager()
    class Meta(object):
        db_table = 'Volunteer'

    def __str__(self):
        # type: () -> str
        return self.name # type: ignore

    def volunteer_type(self):
        # type: () -> text_type
        if self.school is None:
            return 'Community'
        elif self.school.school_type == 'S':
            return 'Junior'
        elif self.school.school_type == 'C':
            return 'Youth'
        else:
            return 'Unknown'
    volunteer_type.admin_order_field = 'school__school_type' # type: ignore

    def state(self):
        # type: () -> Optional[State]
        if self.subdistrict is None:
            return None
        else:
            return self.subdistrict.district.state
    state.admin_order_field = 'subdistrict__district__state' # type: ignore

@python_2_unicode_compatible
class Registration(models.Model):
    id = 0 # type: int
    start = models.DateField() # type: datetime.date
    end = models.DateField() # tyep: datetime.date
    volunteer = models.ForeignKey(Volunteer) # type: Volunteer

    objects = mypy_dummy.dummyRegistrationManager()
    class Meta(object):
        db_table = 'Registration'

    def __str__(self):
        # type: () -> str
        return "{}({} - {})".format(self.volunteer, self.start, self.end) # type: ignore
