django-monthfield
=================

Introduction
------------

This module provides a custom field for storing month (YYYY-MM) as a django field.

This can be useful when dealing with data that relates to a whole month, for example,
the total expenditure for a given month.

This module also adds some arithmetic and other functionality for dealing with months.

Usage
-----

Adding a month field to a django model:

.. code-block:: console

    from django.db import models
    from month.models import MonthField


    # Create your models here.

    class ExampleModel(models.Model):
        name = models.CharField(max_length=20, blank=True)
        month = MonthField("Month Value", help_text="some help...")

        def __unicode__(self):
            return unicode(self.month)

The module defines a "Month" class which is used to represent the MonthField attribute on the model.
The "Month" class can also be used standalone without any django model.

Some examples of funcionality provided by the Month class:

.. code-block:: console

    import month

    m = month.Month(2017, 3)

    print(m)
    >"2017-03"

    print(m + 2)
    >"2017-05"

    print(m.last_day())
    >"2017-03-31"

    m2 = month.Month(2017, 7)

    print(m > m2)
    >"False"

    print(m.range(m2))
    >"[2017-03, 2017-04, 2017-05, 2017-06, 2017-07]"

Example project
---------------

An example website using this module is included in the repository.

username: test
password: test
