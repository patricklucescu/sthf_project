'''
Created on 29 Sep 2018

@author: S.Walliser, P.Lucescu, F.Ferrari
'''

import datetime
from dateutil.relativedelta import relativedelta 

def as_workday(datetime_, next_ = True):
    """ Returns next or previous working day for given date, if given date is 
    working day will return unmodified
    """
    assert isinstance(datetime_, datetime.date), \
        "datetime_ must be a datetime.date"
    if next_:
        ref_day = 7 ## take next Monday as reference
    else:
        ref_day = 4 ## take prev Friday as reference
    weekday = datetime_.weekday()
    shift = ((weekday // 5) * (ref_day - weekday)) ## //5 insures that we are in weekday
    shifted_date = datetime_ + datetime.timedelta(days=shift)
    return(shifted_date)
pass

def get_shifted_bus_day(date_, days_):
    is_following_bday = days_ > 0
    return as_workday(date_ + datetime.timedelta(days = days_),
                      next_ = is_following_bday)
pass

def get_last_bus_day(date_):
    return get_shifted_bus_day(date_, days_=-1)
pass

def get_next_bus_day(date_):
    return get_shifted_bus_day(date_, days_=+1)
pass
