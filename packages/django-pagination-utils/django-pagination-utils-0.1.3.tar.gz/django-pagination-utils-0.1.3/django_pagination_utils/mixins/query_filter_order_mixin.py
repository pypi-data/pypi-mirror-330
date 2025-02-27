from abc import abstractmethod
from django.db.models import Model
from .query_filter_mixin import QueryFilterMixin
from .query_order_mixin import QueryOrderMixin


class QueryFilterOrderMixin(QueryFilterMixin, QueryOrderMixin):
    """ Clase abstracta que define un mixin para aplicar filtros y ordenamientos a un queryset. """

    @property
    @abstractmethod
    def model(self) -> Model:
        raise NotImplementedError

    def __init__(self):
        super().__init__()
        self.init_filterset_defaults()
        self.init_order_defaults()

    def get_queryset(self):
        return self.model.objects.all()

    def get_complete_queryset(self, params: dict):
        queryset = self.get_queryset()
        queryset = self.apply_filterset_to_queryset(queryset, params)
        queryset = self.apply_order_to_queryset(queryset, params)
        return queryset

    def get_defaults(self):
        return {
            'order_by': self.default_order_by,
            'order_direction': self.default_order_direction,
            'fields_order': self.allowed_fields_order,
            'field_time': self.default_field_time
        }
