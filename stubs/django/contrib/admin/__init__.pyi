from django.db.models import Model, ModelT, QuerySet
from django.urls import RegexURLPattern
from django.http import HttpRequest

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

class TabularInline(InlineModelAdmin):
    pass

class AdminSite(object):
    site_title = ... # type: text_type
    site_header = ... # type: text_type
    site_url = ... # type: text_type
    urls = ... # type: Tuple[List[RegexURLPattern], Any, Any]

    def register(self, model_or_iterable, admin_class=None, **options):
        # type: (Any, type, **Any) -> None
        ...

class SimpleListFilter(object):
    title = ... # type: text_type
    parameter_name = ... # type: text_type

    def lookups(self, request, model_admin):
        # type: (HttpRequest, ModelAdmin) -> Sequence[Tuple[text_type, text_type]]
        ...
    def queryset(self, request, queryset):
        # type: (HttpRequest, QuerySet[Any]) -> QuerySet[Any]
        ...
    def value(self) -> text_type: ...

site = ... # type: AdminSite
HORIZONTAL = ... # type: int
VERTICAL = ... # type: int
