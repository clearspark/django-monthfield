import datetime

from django.test import TestCase
from month.models import Month
from example.models import Example


def TestMonthFunctions(TestCase):

    def tearDown(self):
        Example.objects.all().delete()

    def test_constructors(self):
        m = Month(2010, 1)
        self.assertEqual(m.year, 2010)
        self.assertEqual(m.month, 1)

        m = Month.from_string('2010-01')
        self.assertEqual(m.year, 2010)
        self.assertEqual(m.month, 1)

        m = Month.from_date(datetime.date(year=2010, month=1, day=20))
        self.assertEqual(m.year, 2010)
        self.assertEqual(m.month, 1)
    
    def test_addition(self):
        m = Month(2010, 1)
        x = m + 5
        self.assertEqual(x.year, 2010)
        self.assertEqual(x.month, 6)

        x = m + 11
        self.assertEqual(x.year, 2010)
        self.assertEqual(x.month, 12)

        x = m + 12
        self.assertEqual(x.year, 2011)
        self.assertEqual(x.month, 1)

        x = m + 13
        self.assertEqual(x.year, 2011)
        self.assertEqual(x.month, 2)

        x = m - 1
        self.assertEqual(x.year, 2009)
        self.assertEqual(x.month, 12)

        x = m + 0
        self.assertEqual(x.year, 2010)
        self.assertEqual(x.month, 1)

        x = m - 12
        self.assertEqual(x.year, 2009)
        self.assertEqual(x.month, 1)

        x = m.next_month()
        self.assertEqual(x.year, 2010)
        self.assertEqual(x.month, 2)

        x = m.prev_month()
        self.assertEqual(x.year, 2009)
        self.assertEqual(x.month, 12)

    def test_firstday(self):
        m = Month(2010, 1)
        self.assertEqual(m.firstDay(), datetime.date(year=2010, month=1, day=1))
        self.assertEqual(m.last_day(), datetime.date(year=2010, month=1, day=31))

        m = Month(2010, 2)
        self.assertEqual(m.firstDay(), datetime.date(year=2010, month=2, day=1))
        self.assertEqual(m.last_day(), datetime.date(year=2010, month=2, day=28))

        m = Month(2008, 2)
        self.assertEqual(m.firstDay(), datetime.date(year=2008, month=2, day=1))
        self.assertEqual(m.last_day(), datetime.date(year=2008, month=2, day=29))

    def test_contains(self):
        m = Month(2010, 1)
        assert datetime.date(year=2010, month=1, day=1) in m
        assert datetime.date(year=2010, month=1, day=10) in m
        assert datetime.date(year=2010, month=1, day=31) in m
        assert datetime.date(year=2010, month=2, day=1) not in m
        assert datetime.date(year=2009, month=12, day=31) not in m
        assert datetime.date(year=2009, month=1, day=31) not in m
        assert datetime.date(year=2010, month=2, day=15) not in m
    
    def test_int_conversion(self):
        m = Month(2010, 1)
        n = Month.from_int(int(m))
        self.assertEqual(n.year, 2010)
        self.assertEqual(n.month, 1)

    def test_comparisons(self):
        m = Month(2010, 1)
        assert m == "2010-01-20"
        assert m == "2010-01-20"
        assert m == "2010-01"
        assert m == "2010-01-20"
        assert m < "2010-02-01"
        assert m > "2009-12"
        assert m > "2009-12-31"
        
        p = m.prev_month()
        n = m.next_month()

        assert m == m
        assert m <= m
        assert m >= m
        assert not m > m
        assert not m < m
        assert not m != m

        assert not m == p
        assert m > p
        assert m >= p
        assert not m <= p
        assert not m < p
        assert m != p

        assert not m == n
        assert m != n
        assert m < n
        assert m <= n
        assert not m > n
        assert not m >= n

class test_model_field(TestCase):

    def test_queries(self):
        e = Example(name='2010-01', month=Month(2010, 1))
        e.save()
        assert isinstance(e.month, Month)
        assert e.month.month == 1
        assert e.month.year == 2010
        pk = e.pk
        
        e = Example.objects.get(pk=pk)
        assert isinstance(e.month, Month)
        assert e.month.month == 1
        assert e.month.year == 2010


        e = Example(name='2010-01', month='2010-01')
        e.save()
        pk = e.pk
        
        e = Example.objects.get(pk=pk)
        assert isinstance(e.month, Month)
        assert e.month.month == 1
        assert e.month.year == 2010

        e = Example(name='2010-01', month=datetime.date(year=2010, month=1, day=20))
        e.save()
        pk = e.pk
        
        e = Example.objects.get(pk=pk)
        assert isinstance(e.month, Month)
        assert e.month.month == 1
        assert e.month.year == 2010

        Example.objects.all().delete()
        for year in range(2001, 2011):
            for month in range(1, 13):
                name = "%s - %02d" %(year, month)
                Example(name=name, month=Month(year, month)).save()

        qs = Example.objects.filter(month='2005-12')
        assert qs.exists()
        assert qs.count() == 1

        qs = Example.objects.filter(month__gte='2005-12')
        assert qs.exists()
        self.assertEqual(qs.count(), 61)

        qs = Example.objects.filter(month__gt='2005-12')
        assert qs.exists()
        assert qs.count() == 60
