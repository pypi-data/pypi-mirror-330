from django_filters.filters import Filter
from typing import List, Optional
from django.forms import Form


class FormFieldNotFoundException(Exception):

    def __init__(self, field_name: str):
        super().__init__(f'Campo "{field_name}" no encontrado en el formulario')


class Column:

    def __init__(self, field_name: str, css_class: str = ""):
        self.field_name = field_name
        self.css_class = css_class

    def render_label(self, field: Filter) -> str:
        widget_attr_id = field.widget.attrs.get('id', "")
        return f'<label for="{widget_attr_id}" class="form-label">{field.label}</label>'

    def render(self, field: Filter, field_value: Optional[str]) -> str:
        widget_render = field.widget.render(name=self.field_name, value=field_value)
        return f'<div class="{self.css_class}"> { self.render_label(field) } {widget_render} </div>'


class Row:

    def __init__(self, fields: List[Column], css_class: str = ""):
        self.fields = fields
        self.css_class = css_class

    def render(self, form: Form) -> str:
        row_html = f'<div class="row {self.css_class}">'
        for column in self.fields:
            field_name = column.field_name
            field = form.fields.get(field_name)
            field_value = form.data.get(field_name, '')
            if not field:
                raise FormFieldNotFoundException(field_name)
            row_html += column.render(field, field_value)
        row_html += '</div>'
        return row_html


class FilterLayout:

    def __init__(self, rows: List[Row] = None):
        self.rows = rows if rows is not None else []

    def render(self, form: Form) -> str:
        return '\n'.join(row.render(form) for row in self.rows)
