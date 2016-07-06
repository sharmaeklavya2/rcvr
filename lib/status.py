from __future__ import unicode_literals

from main.models import Volunteer, Registration
from django.db.models import QuerySet
from datetime import date

def filter_by_active(queryset, today, active):
    # type: (QuerySet[Volunteer], date, bool) -> QuerySet[Volunteer]
    current_regs = Registration.objects.filter(start__lte=today, end__gte=today)
    vids = current_regs.values_list('volunteer', flat=True)
    if active:
        result = queryset.filter(id__in=vids)
    else:
        result = queryset.exclude(id__in=vids)
    return result
