'''
Created on 16 Sep 2017

@author: francescoferrari
'''

import datetime as dt
import numpy as np
from dateutil.relativedelta import relativedelta

def get_prev_day_trading(date_, days_):
    date_ = dt.date(2018, 8, 22)
    days_ = 30
    date_2 = date_ - relativedelta(date_, days=days_)
    np.busday_offset(date_2, -1)
    return date_2


# Santiago 