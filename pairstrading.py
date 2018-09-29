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
START_DATE_OF_TRADING = dt.date(2000, 1, 1) # MUST BE A TRADING DAY IN THE DATA
END_DATE_OF_TRADING = dt.date(2001, 1, 1)
# Import data
STOCK_DATA = pd.read_csv("random_stock_data.csv", sep = ",", index_col=['Date'], parse_dates=['Date'])
# Define NYSE holiday
NYSE_HOLIDAYS = get_nyse_holidays(1996, 2018)
# Number of stock pairs
NUM_STOCK_PAIRS = 10
# Number of days that we hold stocks
NUM_HOLD_DAYS = 60

#sys.exit()

def get_x_prev_trading_day(date_, trad_days_):
    out_date = np.busday_offset(date_, - trad_days_, holidays = NYSE_HOLIDAYS)
    return out_date.astype(dt.date)
pass

# Assert this:
# end_date_of_trading_: start_date_of_trading_ < end_date_of_trading_
# start_date_of_trading_: get_X_prev_day_trading_day(start_date_of_trading_temp, LOOK_BACK_DAYS) > START_DATE_OF_DATA




def get_Pairs(stock_data_, start_date_of_trading_):

    start_day_lookback = get_X_prev_trading_day(start_date_of_trading, LOOK_BACK_DAYS)
    assert start_day_lookback > START_DATE_OF_DATA, 'Error 1 - Define a later day of start tarding - not in database'

    end_day_lookback = get_X_prev_day_trading_day(start_date_of_trading, 1)

    lookback_dataframe = stock_data_[start_day_lookback:end_day_lookback]

    lookback_dataframe = (lookback_dataframe / lookback_dataframe.iloc[0]) * 100

    pairs_list = list( combinations(list(lookback_dataframe.columns.values)[1:],2))
    std_pairs=[]
    for pair in pairs_list:
        stock_A = lookback_dataframe[pair[0]]
        stock_B = lookback_dataframe[pair[1]]
        delta_A_B = stock_A - stock_B
        std_delta_A_B = np.std(delta_A_B)
        triple = (std_delta_A_B, pair[0], pair[1])
        std_pairs.append(triple)

    sorted_std_pairs = sorted(std_pairs, key=lambda x: float(x[0]))
    chosen_stock_pairs = sorted_std_pairs[0:NUM_STOCK_PAIRS-1]
    # chosen_stock_pairs = [x[1:] for x in chosen_stock_pairs] #remove std fromt triple, become tuple

    return sorted_std_pairs
pass


# Analyze and trade
def roll_over_time(stock_data_, start_date_of_trading_, end_date_of_trading_, num_hold_days_):

    assert start_date_of_trading_ < end_date_of_trading_, "Error 2 - Trading start day before end day"


    #start_date_of_trading_ = START_DATE_OF_TRADING
    #end_date_of_trading_ = END_DATE_OF_TRADING

    list_of_dates = list(stock_data_.index)

    # iterate over alle dates and trade and analyze





get_x_prev_trading_day(dt.date(2018, 9, 28), 252)