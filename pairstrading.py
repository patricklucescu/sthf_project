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

sys.exit()

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

def set_start_trading_day(START_DATE_OF_TRADING):
    start_date_of_trading_temp = get_X_prev_day_trading_day(START_DATE_OF_TRADING, 0)
    if get_X_prev_day_trading_day(start_date_of_trading_temp, LOOK_BACK_DAYS) > START_DATE_OF_DATA:
        return start_date_of_trading_temp
    else:
        raise ValueError('Please enter a START_DATE - LOOK_BACK_DAYS that is after the start DATA date')

def get_Pairs(STOCK_DATA,START_DATE_OF_TRADING):
    start_day_lookback = get_X_prev_trading_day(START_DATE_OF_TRADING,LOOK_BACK_DAYS)
    end_day_lookback = get_X_prev_day_trading_day(START_DATE_OF_TRADING,1) ##TODO SPECIFY HOW TO DO THIS

    start_day_lookback = dt.date(2000, 1, 1)
    end_day_lookback = dt.date(2001, 1, 1)

    temp = STOCK_DATA
    temp.set_index(temp)

    lookback_dataframe = STOCK_DATA( start_day_lookback, end_day_lookback)

    pairs_list = list( combinations(list(lookback_dataframe.columns.values)[1:],2))


