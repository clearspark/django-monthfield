import datetime
from rest_framework import fields, serializers

from month import Month, models

class MonthField(fields.DateField):
  
  def to_internal_value(self, value):
    if isinstance(value, Month):
        month = value
    elif isinstance(value, datetime.date):
        month = Month.from_date(value)
        if len(str(month.year)) < 4:
            raise serializers.ValidationError(
                self.error_messages['invalid_year'],
                code='invalid_year',
                params={'value': value},
            )
    
  def to_representation(self, value):
    return value.strftime(value)
