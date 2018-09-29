'''
Created on 29 Sep 2018

@author: S.Walliser, P.Lucescu, F.Ferrari
'''

import datetime as dt
import numpy as np

from dateutil.relativedelta import relativedelta

def get_start_lookback(date_, days_):
    date_ = dt.date(2018, 8, 22)
    days_ = 30
    date_2 = date_ - relativedelta(date_, days=days_)
    np.busday_offset(date_2, -1)
    