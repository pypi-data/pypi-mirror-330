from typing import Any, Dict
from django.views import View
from django.core.paginator import Paginator
from abc import ABC, abstractmethod
from django.shortcuts import render
from .mixins import (
    QueryFilterOrderMixin,
    InvalidQueryFilterException,
    InvalidOrderDirectionException,
    InvalidOrderFieldException
)

MESSAGE_TYPE_WARNING = 'warning'
MESSAGE_TYPE_DANGER = 'danger'
MESSAGE_BI_ICONS = {
    'warning': 'bi bi-exclamation-octagon-fill text-warning',
    'danger': 'bi bi-exclamation-triangle text-danger'
}
MESSAGE_DEFAULT_ICON = 'bi bi-info-circle text-primary'


class InvalidPageNumberException(Exception):
    def __init__(self, current_page: int, max_page: int):
        super().__init__(f'El número de página {current_page} es inválido, el rango permitido es de 1 a {max_page}')


class PaginatorView(View, QueryFilterOrderMixin):

    default_value: int = 5
    default_page: int = 1
    default_per_page: int = 5
    default_on_each_side: int = 2
    default_on_ends: int = 0
    max_per_page: int = 100
    export_url: str = None
    import_url: str = None

    @property
    @abstractmethod
    def template_name(self) -> str:
        pass

    def get_integer_query_param(self, name: str, default_value: int, max_value: int = None) -> int:
        try:
            value = int(self.request.GET.get(name, default_value))
        except (ValueError, TypeError):
            value = default_value
        if max_value and value > max_value:
            value = max_value
        return value

    def get_page_obj(self, query):
        per_page = self.get_integer_query_param('per_page', self.default_per_page, self.max_per_page)
        page_number = self.get_integer_query_param('page', self.default_page)
        paginator = Paginator(query, per_page)
        if page_number < 1:
            page_number = 1
        if page_number > paginator.num_pages:
            raise InvalidPageNumberException(page_number, paginator.num_pages)
        page_obj = paginator.get_page(page_number)
        pages = paginator.get_elided_page_range(
            number=page_number,
            on_each_side=self.default_on_each_side,
            on_ends=self.default_on_ends
        )
        return page_obj, pages

    def get_context_error(self, exception: Exception, message_type: str) -> Dict[str, str]:
        return {
            'type': message_type,
            'icon': MESSAGE_BI_ICONS.get(message_type, MESSAGE_DEFAULT_ICON),
            'message': str(exception)
        }

    def build_context(self, request) -> Dict[str, Any]:
        pages = []
        page_obj = None
        page_error = None
        try:
            queryset = self.get_queryset()
            queryset = self.apply_filterset_to_queryset(queryset, request.GET)
            queryset = self.apply_order_to_queryset(queryset, request.GET)
            page_obj, pages = self.get_page_obj(queryset)
        except (InvalidQueryFilterException, InvalidOrderDirectionException, InvalidOrderFieldException) as e:
            page_error = self.get_context_error(e, MESSAGE_TYPE_WARNING)
        except (InvalidPageNumberException) as e:
            page_error = self.get_context_error(e, MESSAGE_TYPE_DANGER)
        except Exception as e:
            raise e
        return {
            'page_error': page_error,
            'page_obj': page_obj,
            'pages': pages,
            'filterset': self.filterset,
            'filters': self.applied_filters,
            'filters_errors': self.filters_errors,
            'order': self.applied_order,
            'defaults': self.get_defaults(),
            'export_url': self.export_url,
            'import_url': self.import_url
        }

    def get(self, request, *args, **kwargs):
        context = self.build_context(request)
        return render(request, self.template_name, context)
