'''
Created on 29 Sep 2018

@author: S.Walliser, P.Lucescu, F.Ferrari
'''
import datetime as dt
import numpy as np
import pandas as pd
import sys

from dateutil.relativedelta import relativedelta
from itertools import combinations
from nyse_holidays import get_nyse_holidays
from dateutil import rrule 

## Global Constants
# Look back window in days
LOOK_BACK_DAYS = 21
# Dates regarding data
START_DATE_OF_DATA = dt.date(2000, 1, 1)
END_DATE_OF_DATA = dt.date(2001, 1, 1)
# Dates regarding trading
START_DATE_OF_TRADING = dt.date(2000, 1, 1)
END_DATE_OF_TRADING = dt.date(2001, 1, 1)
# Import data
STOCK_DATA = pd.read_csv("random_stock_data.csv", sep = ",")#, parse_dates=['Date'])
# Define NYSE holiday
NYSE_HOLIDAYS = get_nyse_holidays(1996, 2018)

sys.exit()

def get_x_prev_trading_day(date_, trad_days_):
    out_date = np.busday_offset(date_, -252, holidays = NYSE_HOLIDAYS)
    return out_date.astype(dt.date)
pass

# def get_nyse_holidays(year_start_, year_end_):
#     a = dt.date(year_start_, 1, 1)
#     b = dt.date(year_end_, 12, 31)
#     rs = rrule.rruleset()
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, bymonth=12, bymonthday=31, byweekday=rrule.FR)) # New Years Day  
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, bymonth= 1, bymonthday= 1))                     # New Years Day  
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, bymonth= 1, bymonthday= 2, byweekday=rrule.MO)) # New Years Day    
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, bymonth= 1, byweekday= rrule.MO(3)))            # Martin Luther King Day   
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, bymonth= 2, byweekday= rrule.MO(3)))            # Washington's Birthday
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, byeaster= -2))                                  # Good Friday
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, bymonth= 5, byweekday= rrule.MO(-1)))           # Memorial Day
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, bymonth= 7, bymonthday= 3, byweekday=rrule.FR)) # Independence Day
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, bymonth= 7, bymonthday= 4))                     # Independence Day
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, bymonth= 7, bymonthday= 5, byweekday=rrule.MO)) # Independence Day
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, bymonth= 9, byweekday= rrule.MO(1)))            # Labor Day
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, bymonth=11, byweekday= rrule.TH(4)))            # Thanksgiving Day
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, bymonth=12, bymonthday=24, byweekday=rrule.FR)) # Christmas  
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, bymonth=12, bymonthday=25))                     # Christmas  
#     rs.rrule(rrule.rrule(rrule.YEARLY, dtstart=a, until=b, bymonth=12, bymonthday=26, byweekday=rrule.MO)) # Christmas 
#     # Exclude potential holidays that fall on weekends
#     rs.exrule(rrule.rrule(rrule.WEEKLY, dtstart=a, until=b, byweekday=(rrule.SA,rrule.SU)))
#     return list(rs)
# pass

def set_end_trading_day(START_DATE_OF_TRADING, END_DATE_OF_TRADING):
    if START_DATE_OF_TRADING < END_DATE_OF_TRADING:
        raise ValueError('Please enter a end trading date that is after the start trading date')
    else:
        return get_X_prev_day_trading_day(END_DATE_OF_TRADING, 0)
pass

def set_start_trading_day(START_DATE_OF_TRADING):
    start_date_of_trading_temp = get_X_prev_day_trading_day(START_DATE_OF_TRADING, 0)
    if get_X_prev_day_trading_day(start_date_of_trading_temp, LOOK_BACK_DAYS) > START_DATE_OF_DATA:
        return start_date_of_trading_temp
    else:
        raise ValueError('Please enter a START_DATE - LOOK_BACK_DAYS that is after the start DATA date')
pass

def get_Pairs(STOCK_DATA,START_DATE_OF_TRADING):
    start_day_lookback = get_X_prev_trading_day(START_DATE_OF_TRADING,LOOK_BACK_DAYS)
    end_day_lookback = get_X_prev_day_trading_day(START_DATE_OF_TRADING,1) ##TODO SPECIFY HOW TO DO THIS

    start_day_lookback = dt.date(2000, 1, 1)
    end_day_lookback = dt.date(2001, 1, 1)

    temp = STOCK_DATA
    temp.set_index(temp)

    lookback_dataframe = STOCK_DATA( start_day_lookback, end_day_lookback)

    pairs_list = list( combinations(list(lookback_dataframe.columns.values)[1:],2))
pass