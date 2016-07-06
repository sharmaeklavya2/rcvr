from __future__ import unicode_literals

from main.models import Volunteer, Registration
from django.db.models import QuerySet
from datetime import date
from django.utils import timezone

from typing import Optional

def filter_by_active(queryset, today, active):
    # type: (QuerySet[Volunteer], date, bool) -> QuerySet[Volunteer]
    current_regs = Registration.objects.filter(start__lte=today, end__gte=today)
    vids = current_regs.values_list('volunteer', flat=True)
    if active:
        result = queryset.filter(id__in=vids)
    else:
        result = queryset.exclude(id__in=vids)
    return result

def get_status(volunteer, today=None):
    # type: (Volunteer, Optional[date]) -> bool
    if today is None:
        today = timezone.now().date()
    regs = Registration.objects.filter(start__lte=today, end__gte=today, volunteer=volunteer)
    return regs.exists()

get_status.short_description = 'Active' # type: ignore
