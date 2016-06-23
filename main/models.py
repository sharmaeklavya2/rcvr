from __future__ import unicode_literals

import datetime
from django.db import models

from six import text_type
from typing import Optional, Tuple

address_help_text = """Please don't include your district, city, state in your address.
That will be extracted from your PIN code"""

class State(models.Model):
    scode = models.CharField('State Code', max_length=3, primary_key=True) # type: text_type
    name = models.CharField(max_length=30, unique=True) # type: text_type
    class Meta(object):
        db_table = 'State'

class District(models.Model):
    pin = models.PositiveIntegerField(primary_key=True) # type: int
    name = models.CharField(max_length=60, blank=True) # type: text_type
    state = models.ForeignKey(State) # type: State
    class Meta(object):
        db_table = 'District'

class SubDistrict(models.Model):
    pin = models.PositiveIntegerField() # type: int
    name = models.CharField(max_length=60, blank=True) # type: text_type
    district = models.ForeignKey(District) # type: District
    class Meta(object):
        db_table = 'SubDistrict'
        unique_together = (('pin', 'district'),)

SCHOOL_CHOICES = (
    ('J', 'Junior'),
    ('Y', 'Youth'),
) # type: Tuple[Tuple[text_type, text_type], ...]

class School(models.Model):
    name = models.CharField(max_length=30) # type: text_type
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

    class Meta(object):
        db_table = 'School'

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
) # type: Tuple[Tuple[text_type, text_type], ...]

class Volunteer(models.Model):
    create_stamp = models.DateTimeField('Created', auto_now_add=True) # type: datetime.datetime
    update_stamp = models.DateTimeField('Last Updated', auto_now=True) # type: datetime.date

    name = models.CharField(max_length=100) # type: text_type
    aadharid = models.BigIntegerField('Aadhar ID', unique=True) # type: int
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
    school = models.ForeignKey(School, null=True, blank=True) # type: Optional[School]

    class Meta(object):
        db_table = 'Volunteer'

    def volunteer_type(self):
        # type: () -> text_type
        if self.school is None:
            return 'C'
        else:
            return self.school.school_type
    volunteer_type.admin_order_field = 'school__school_type' # type: ignore

    def state(self):
        # type: () -> Optional[State]
        if self.subdistrict is None:
            return None
        else:
            return self.subdistrict.district.state
    state.admin_order_field = 'subdistrict__district__state' # type: ignore

class Registration(models.Model):
    start = models.DateField() # type: datetime.date
    end = models.DateField() # tyep: datetime.date
    volunteer = models.ForeignKey(Volunteer) # type: Volunteer

    class Meta(object):
        db_table = 'Registration'