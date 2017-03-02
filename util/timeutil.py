
from datetime import datetime

def get_date_str(datetime_obj):
    assert (isinstance(datetime_obj, datetime))
    return '%.4d%.2d%.2d' % \
           (datetime_obj.year,
            datetime_obj.month,
            datetime_obj.day)

def get_datetime_obj(timestamp_str):
    year, month, day = int(timestamp_str[0:4]), \
                       int(timestamp_str[4:6]), \
                       int(timestamp_str[6:8])
    return datetime(year, month, day)


