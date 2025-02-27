

# Django Pagination Utils

`django-pagination-utils` is a library that extends the default paginator and provides utilities for pagination in Django. This library includes mixins and views that facilitate the implementation of these functionalities in your Django projects.

## Installation

To install the library, run the following command:

```bash
pip install django-pagination-utils
```

## Usage

### PaginatorView
This class provides pagination and ordering for a queryset. To use it, you must create a subclass of PaginatorView and define the necessary attributes.

```python
Ejemplo:
from django_pagination_utils.paginator_view import PaginatorView
from .models import MyModel
from .filters import MyFilterSet

class MyView(PaginatorView):
    model = MyModel
    template_name = 'my_template.html'
    filterset_class = MyFilterSet
    allowed_fields_order = ['field1', 'field2', 'field3']
```

## Attributes
model: The Django model that will be used for the queryset.
template_name: The name of the template that will be used to render the view.
filterset_class: The filters class that will be applied to the queryset.
allowed_fields_order: List of fields that can be used to order the queryset. If not provided, all fields will be allowed.

## Mixins

```python
QueryOrderMixin
from django_pagination_utils.mixins.query_order_mixin import QueryOrderMixin

class MyOrderView(QueryOrderMixin):
    model = MyModel
    allowed_fields_order = ['field1', 'field2', 'field3']
```

### QueryFilterMixin
The QueryFilterMixin provides functionalities to filter a queryset.

```python
from django_pagination_utils.mixins.query_filter_mixin import QueryFilterMixin

class MyFilterView(QueryFilterMixin):
    model = MyModel
    filterset_class = MyFilterSet
```

### QueryFilterOrderMixin
The QueryFilterOrderMixin provides functionalities to filter and order a queryset.

```python
from django_pagination_utils.mixins.query_filter_order_mixin import QueryFilterOrderMixin

class MyFilterOrderView(QueryFilterOrderMixin):
    model = MyModel
    filterset_class = MyFilterSet
    allowed_fields_order = ['field1', 'field2', 'field3']
```

## Exceptions

The library defines several exceptions that you can handle in your code:

 * InvalidOrderDirectionException: Raised when the ordering direction is invalid.
 * InvalidOrderFieldException: Raised when the ordering field is invalid.
 * InvalidQueryFilterException: Raised when the query filter is invalid.
 * FormFieldNotFoundException: Raised when a form field is not found.

## Example

```python
from django_pagination_utils.paginator_view import PaginatorView
from .models import MyModel
from .filters import MyFilterSet

class MyView(PaginatorView):
    model = MyModel
    template_name = 'my_template.html'
    filterset_class = MyFilterSet
    allowed_fields_order = ['field1', 'field2', 'field3']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_data'] = 'some extra data'
        return context
```

In your my_template.html template, you can access the paginated and ordered objects:

```html
{% for obj in page_obj %}
    {{ obj }}
{% endfor %}

<div class="pagination">
    <span class="step-links">
        {% if page_obj.has_previous %}
            <a href="?page=1">&laquo; first</a>
            <a href="?page={{ page_obj.previous_page_number }}">previous</a>
        {% endif %}

        <span class="current">
            Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
        </span>

        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">next</a>
            <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
        {% endif %}
    </span>
</div>
```

## Licencia
This project is licensed under the MIT License - see the LICENSE file for details.
