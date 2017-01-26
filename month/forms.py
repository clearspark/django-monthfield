from django import forms
from month.widgets import MonthSelectorWidget


class MonthField(forms.DateField):
    widget = MonthSelectorWidget
