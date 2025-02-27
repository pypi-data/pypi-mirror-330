from abc import ABC, abstractmethod
from django_filters import FilterSet
from django.db.models import QuerySet


class InvalidQueryFilterException(Exception):
    def __init__(self):
        super().__init__(f'Los filtros ingresados son inválidos o tienen errores.')


class QueryFilterMixin(ABC):

    @property
    @abstractmethod
    def filterset_class(self) -> FilterSet:
        raise NotImplementedError(
            f"El atributo 'filterset_class' no ha sido implementado en la clase {self.__class__.__name__}. "
            "Define una subclase de 'FilterSet' para usar este mixin."
        )

    def init_filterset_defaults(self):
        self.filterset = None
        self.applied_filters: dict = {}
        self.filters_errors: dict = {}

    def add_applied_filters(self):
        """
        Registra los filtros aplicados exitosamente en `applied_filters`.
        """
        cleaned_data = self.filterset.form.cleaned_data
        for key, value in cleaned_data.items():
            if not value:
                continue
            field = self.filterset.form.fields.get(key)
            if not field:
                continue
            self.applied_filters[key] = {
                'label': field.label,
                'value': value
            }

    def add_filters_errors(self):
        """
        Registra los errores de los filtros en `filters_errors`.
        """
        for key in self.filterset.filters:
            field = self.filterset.form.fields.get(key)
            errors = self.filterset.errors.get(key)
            if not field or not errors:
                continue
            self.filters_errors[key] = {
                'label': field.label,
                'errors': errors
            }

    def apply_filterset_to_queryset(self, queryset: QuerySet, filter_params: dict) -> QuerySet:
        """
        Aplica los filtros definidos en `filterset_class` al queryset.

        Args:
            filter_params: Parámetros de los filtros a aplicar.
            queryset: Queryset a filtrar.

        Returns:
            Queryset filtrado según los parámetros especificados.

        Raises:
            InvalidQueryFilterException: Si los filtros especificados no son válidos.
        """
        self.init_filterset_defaults()
        self.filterset = self.filterset_class(filter_params, queryset=queryset)
        queryset = self.filterset.qs
        self.add_applied_filters()
        if not self.filterset.is_valid():
            self.add_filters_errors()
            raise InvalidQueryFilterException()
        return queryset
