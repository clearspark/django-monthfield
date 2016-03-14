import sys

PY3 = sys.version_info >= (3,)

if PY3:
    string_type = str
else:
    string_type = basestring
