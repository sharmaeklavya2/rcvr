from django.db.models import Model
from django.urls import RegexURLPattern

from six import text_type
from typing import Any, AnyStr, Iterable, List, Mapping, Optional, Sequence, Tuple, Union

class BaseModelAdmin(object):
    pass

class ModelAdmin(BaseModelAdmin):
    list_display = ... # type: Sequence[text_type]
    radio_fields = ... # type: Mapping[text_type, int]
    inlines = ... # type: Sequence[Any]

class InlineModelAdmin(BaseModelAdmin):
    model = ... # type: type

class StackedInline(InlineModelAdmin):
    pass

class AdminSite(object):
    site_title = ... # type: text_type
    site_header = ... # type: text_type
    site_url = ... # type: text_type
    urls = ... # type: Tuple[List[RegexURLPattern], Any, Any]

    def register(self, model_or_iterable, admin_class=None, **options):
        # type: (Any, type, **Any) -> None
        ...

site = ... # type: AdminSite
HORIZONTAL = ... # type: int
VERTICAL = ... # type: int
