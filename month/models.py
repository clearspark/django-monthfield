import datetime

from django.db import models

from month import forms
from month import widgets
from month import Month
from month.util import string_type


class MonthField(models.DateField):
    description = "A specific month of a specific year."
    widget = widgets.MonthSelectorWidget

    def to_python(self, value):
        if isinstance(value, Month):
            month = value
        elif isinstance(value, datetime.date):
            month = Month.from_date(value)
        elif isinstance(value, string_type):
            month = Month.from_string(value)
        else:
            month = None
        return month

    def get_prep_value(self, value):
        month = self.to_python(value)
        if month is not None:
            return month.first_day()
        return None

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def clean(self, value, instance):
        return self.to_python(value)

    def formfield(self, **kwargs):
        # defaults = {'widget': self.widget}
        # defaults.update(kwargs)
        # return forms.MonthField(**defaults)

        # The widget is allready being specified somewhere by models.DateField...
        kwargs['widget'] = self.widget
        return forms.MonthField(**kwargs)
