import datetime

from django.db import models
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _


from month import forms
from month import widgets
from month import Month
from month.util import string_type


class MonthField(models.DateField):
    description = "A specific month of a specific year."
    widget = widgets.MonthSelectorWidget

    default_error_messages = {
        'invalid_year': _("Year informed invalid. Enter at least 4 digits."),
    }

    def to_python(self, value):
        if isinstance(value, Month):
            month = value
        elif isinstance(value, datetime.date):
            month = Month.from_date(value)
            if len(str(month.year)) < 4:
                raise exceptions.ValidationError(
                    self.error_messages['invalid_year'],
                    code='invalid_year',
                    params={'value': value},
                )
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
        # The widget is allready being specified somewhere by models.DateField...
        kwargs['widget'] = self.widget
        defaults = {
            'form_class': forms.MonthField
        }
        defaults.update(kwargs)
        return super(MonthField, self).formfield(**defaults)
