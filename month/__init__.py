import datetime

from month.util import string_type


def days(days):
    return datetime.timedelta(days=days)


class Month(object):
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self._date = datetime.date(year=self.year, month=self.month, day=1)

    @classmethod
    def from_int(cls, months):
        y, m = divmod(months, 12)
        m += 1
        return cls(y, m)

    @classmethod
    def from_date(cls, date):
        return cls(date.year, date.month)
    
    @classmethod
    def from_string(cls, date):
        y = int(date[:4])
        m = int(date[5:7])
        return cls(y, m)

    def __add__(self, x):
        '''x is an integer'''
        return Month.from_int(int(self) + x)
    def __sub__(self, x):
        '''x is integer or Month instance'''
        if isinstance(x, Month):
            return int(self) - int(x)
        else:
            return Month.from_int(int(self) - int(x))
    def next_month(self):
        return self + 1
    def prev_month(self):
        return self - 1
    def first_day(self):
        return self._date
    def last_day(self):
        return self.next_month().first_day() - days(1)
    def __int__(self):
        return self.year * 12 + self.month - 1
    def __contains__(self, date):
        return self == date
    def __eq__(self, x):
        if isinstance(x, Month):
            return x.month == self.month and x.year == self.year
        if isinstance(x, datetime.date):
            return self.year == x.year and self.month == x.month
        if isinstance(x, int):
            return x == int(self)
        if isinstance(x, string_type):
            return str(self) == x[:7]
    def __gt__(self, x):
        if isinstance(x, Month):
            if self.year != x.year: return self.year > x.year
            return self.month > x.month
        if isinstance(x, datetime.date):
            return self.first_day() > x
        if isinstance(x, int):
            return int(self) > x
        if isinstance(x, string_type):
            return str(self) > x[:7]
    def __ne__(self, x):
        return not self == x
    def __le__(self, x):
        return not self > x
    def __ge__(self, x):
        return (self > x) or (self == x)
    def __lt__(self, x):
        return not self >= x
    def __str__(self):
        return '%s-%02d' %(self.year, self.month)
    def __unicode__(self):
        return self.__str__()
    def __repr__(self):
        return self.__str__()
    def __hash__(self):
        return hash(self.datestring())
    def datestring(self):
        return self.first_day().isoformat()
    isoformat = datestring
    def range(self, x):
        '''x must be an instance of Month that is larger than self.
        returns a list of Month objects that make up the timespan from self to x (inclusive)'''
        months_as_ints = range(int(self), int(x) + 1)
        return [ Month.from_int(i) for i in months_as_ints ]
