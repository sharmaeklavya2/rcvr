# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals

from datetime import date
from django.test import TestCase

import os
import six

from main.models import Volunteer, Registration, AADHAR_LENGTH
from lib.status import filter_by_active, get_status

from six import text_type

aadhar_counter = 0

def make_vol(name):
    # type: (text_type) -> Volunteer
    global aadhar_counter
    aid = str(aadhar_counter).rjust(AADHAR_LENGTH)
    aadhar_counter += 1
    return Volunteer.objects.create(name=name, aadharid=aid, phone=0)

class TestFilter(TestCase):

    def test_get_status(self):
        # type: () -> None
        vol1 = make_vol('vol1')
        vol2 = make_vol('vol2')
        vol3 = make_vol('vol3')

        d0 = date(2000, 1, 1)
        d1 = date(2001, 1, 1)
        d2 = date(2002, 1, 1)
        d3 = date(2003, 1, 1)
        d4 = date(2004, 1, 1)
        d5 = date(2005, 1, 1)

        Registration.objects.create(start=d0, end=d2, volunteer=vol1)
        Registration.objects.create(start=d1, end=d3, volunteer=vol2)
        Registration.objects.create(start=d2, end=d4, volunteer=vol2)

        self.assertTrue(get_status(vol1, d0))
        self.assertTrue(get_status(vol1, d1))
        self.assertTrue(get_status(vol1, d2))
        self.assertFalse(get_status(vol1, d3))
        self.assertFalse(get_status(vol1, d4))
        self.assertFalse(get_status(vol1, d5))

        self.assertFalse(get_status(vol2, d0))
        self.assertTrue(get_status(vol2, d1))
        self.assertTrue(get_status(vol2, d2))
        self.assertTrue(get_status(vol2, d3))
        self.assertTrue(get_status(vol2, d4))
        self.assertFalse(get_status(vol2, d5))

        self.assertFalse(get_status(vol3, d0))
        self.assertFalse(get_status(vol3, d1))
        self.assertFalse(get_status(vol3, d2))
        self.assertFalse(get_status(vol3, d3))
        self.assertFalse(get_status(vol3, d4))
        self.assertFalse(get_status(vol3, d5))

    def test_filter_by_active(self):
        # type: () -> None
        vol1 = make_vol('vol1')
        vol2 = make_vol('vol2')
        vol3 = make_vol('vol3')

        d0 = date(2000, 1, 1)
        d1 = date(2001, 1, 1)
        d2 = date(2002, 1, 1)
        d3 = date(2003, 1, 1)
        d4 = date(2004, 1, 1)
        d5 = date(2005, 1, 1)

        Registration.objects.create(start=d0, end=d2, volunteer=vol1)
        Registration.objects.create(start=d1, end=d3, volunteer=vol2)
        Registration.objects.create(start=d2, end=d4, volunteer=vol2)

        active0 = filter_by_active(Volunteer.objects.all(), d0, True)
        active2 = filter_by_active(Volunteer.objects.all(), d2, True)
        active3 = filter_by_active(Volunteer.objects.all(), d3, True)
        active5 = filter_by_active(Volunteer.objects.all(), d5, True)
        active0a = filter_by_active(Volunteer.objects.exclude(name='vol1'), d0, True)
        active2a = filter_by_active(Volunteer.objects.exclude(name='vol1'), d2, True)
        active3a = filter_by_active(Volunteer.objects.exclude(name='vol1'), d3, True)
        active5a = filter_by_active(Volunteer.objects.exclude(name='vol1'), d5, True)
        inactive0 = filter_by_active(Volunteer.objects.all(), d0, False)
        inactive2 = filter_by_active(Volunteer.objects.all(), d2, False)
        inactive3 = filter_by_active(Volunteer.objects.all(), d3, False)
        inactive5 = filter_by_active(Volunteer.objects.all(), d5, False)
        inactive0a = filter_by_active(Volunteer.objects.exclude(name='vol1'), d0, False)
        inactive2a = filter_by_active(Volunteer.objects.exclude(name='vol1'), d2, False)
        inactive3a = filter_by_active(Volunteer.objects.exclude(name='vol1'), d3, False)
        inactive5a = filter_by_active(Volunteer.objects.exclude(name='vol1'), d5, False)

        self.assertEqual(active0.count(), 1)
        self.assertEqual(active2.count(), 2)
        self.assertEqual(active3.count(), 1)
        self.assertEqual(active5.count(), 0)
        self.assertEqual(active0a.count(), 0)
        self.assertEqual(active2a.count(), 1)
        self.assertEqual(active3a.count(), 1)
        self.assertEqual(active5a.count(), 0)
        self.assertEqual(inactive0.count(), 2)
        self.assertEqual(inactive2.count(), 1)
        self.assertEqual(inactive3.count(), 2)
        self.assertEqual(inactive5.count(), 3)
        self.assertEqual(inactive0a.count(), 2)
        self.assertEqual(inactive2a.count(), 1)
        self.assertEqual(inactive3a.count(), 1)
        self.assertEqual(inactive5a.count(), 2)

        self.assertEqual(sorted(active0.values_list('id', flat=True)), [vol1.id])
        self.assertEqual(sorted(active2.values_list('id', flat=True)), [vol1.id, vol2.id])
        self.assertEqual(sorted(active3.values_list('id', flat=True)), [vol2.id])
        self.assertEqual(sorted(active2a.values_list('id', flat=True)), [vol2.id])
        self.assertEqual(sorted(active3a.values_list('id', flat=True)), [vol2.id])
        self.assertEqual(sorted(inactive0.values_list('id', flat=True)), [vol2.id, vol3.id])
        self.assertEqual(sorted(inactive2.values_list('id', flat=True)), [vol3.id])
        self.assertEqual(sorted(inactive3.values_list('id', flat=True)), [vol1.id, vol3.id])
        self.assertEqual(sorted(inactive5.values_list('id', flat=True)), [vol1.id, vol2.id, vol3.id])
        self.assertEqual(sorted(inactive0a.values_list('id', flat=True)), [vol2.id, vol3.id])
        self.assertEqual(sorted(inactive2a.values_list('id', flat=True)), [vol3.id])
        self.assertEqual(sorted(inactive3a.values_list('id', flat=True)), [vol3.id])
        self.assertEqual(sorted(inactive5a.values_list('id', flat=True)), [vol2.id, vol3.id])
