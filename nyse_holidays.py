'''
Created on 29 Sep 2018

@author: S.Walliser, P.Lucescu, F.Ferrari
'''

import datetime

from dateutil import rrule 

def get_nyse_holidays(year_start_, year_end_):
    a = datetime.date(year_start_, 1, 1)
    b = datetime.date(year_end_, 12, 31)
    rs = rrule.rruleset()
    
    # New Years Day
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b,
                         bymonth=12, bymonthday=31, byweekday=rrule.FR))
    # New Years Day   
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b,
                         bymonth= 1, bymonthday= 1))      
    # New Years Day               
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b,
                         bymonth= 1, bymonthday= 2, byweekday=rrule.MO))
    # Martin Luther King Day  
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b,
                         bymonth= 1, byweekday= rrule.MO(3)))
    # Washington's Birthday              
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, 
                         bymonth= 2, byweekday= rrule.MO(3)))
    # Good Friday      
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, 
                         byeaster= -2))
    # Memorial Day
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, 
                         bymonth= 5, byweekday= rrule.MO(-1)))
    # Independence Day
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, 
                         bymonth= 7, bymonthday= 3, byweekday=rrule.FR))
    # Independence Day
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, 
                         bymonth= 7, bymonthday= 4))
    # Independence Day
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, 
                         bymonth= 7, bymonthday= 5, byweekday=rrule.MO))
    # Labor Day
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, 
                         bymonth= 9, byweekday= rrule.MO(1)))
    # Thanksgiving Day
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, 
                         bymonth=11, byweekday= rrule.TH(4)))
    # Christmas 
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, 
                         bymonth=12, bymonthday=24, byweekday=rrule.FR))
    # Christmas 
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b,
                         bymonth=12, bymonthday=25))              
    # Christmas  
    rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b,
                         bymonth=12, bymonthday=26, byweekday=rrule.MO))
    
    # Exclude potential holidays that fall on weekends
    rs.exrule(rrule.rrule(rrule.WEEKLY,
                          dtstart=a,
                          until=b,
                          byweekday=(rrule.SA,rrule.SU)))
    return list(rs)
pass