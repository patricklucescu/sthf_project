'''
Created on 29 Sep 2018

@author: S.Walliser, P.Lucescu, F.Ferrari
'''

import datetime as dt
import numpy as np
import pandas as pd

from dateutil.relativedelta import relativedelta

## Global Constants
# Look back window in days
LOOK_BACK_DAYS = 21
# Dates regarding data
START_DATE_OF_DATA = dt.date(2000, 01, 01)
END_DATE_OF_DATA = dt.date(2001, 01, 01)
# Dates regarding trading
START_DATE_OF_TRADING = dt.date(2000, 01, 01)
END_DATE_OF_TRADING = dt.date(2001, 01, 01)

def set_end_trading_day(START_DATE_OF_TRADING, END_DATE_OF_TRADING):
    if START_DATE_OF_TRADING < END_DATE_OF_TRADING:
        raise ValueError('Please enter a end trading date that is after the start trading date')
    else:
        return get_X_prev_day_trading_day(END_DATE_OF_TRADING, 0)




def get_X_prev_day_trading_day(date, days_):
    date_ = dt.date(2018, 8, 22)
    days_ = 30
    date_2 = date_ - relativedelta(date_, days=days_)
    np.busday_offset(date_2, -1)
    return date_2

