'''
Created on 29 Sep 2018

@author: S.Walliser, P.Lucescu, F.Ferrari
'''

import datetime as dt
import numpy as np
import pandas as pd

from itertools import combinations
from nyse_holidays import get_nyse_holidays

def read_df_from_db(field_):
#     field_ = "PX_LAST"
    df = pd.read_csv(dir_path + field_ + ext, parse_dates=['Dates'])
    return df
pass

def read_industry_groups():
    sector_df = pd.read_csv(dir_path + 'SECTOR' + ext)
    return sector_df
pass

def get_tickers_list_by_ind_group(ind_group_):
#     ind_group_ = "Electronics"
    sector_df = read_industry_groups()
    idx = sector_df.iloc[1,:] == ind_group_
    tickers_list = sector_df.columns.values[idx].tolist()
    return tickers_list
pass

def get_df_from_to(df_, date_from_, date_to_, ind_group_ = None):
#     date_from_ = dt.date(2010, 1, 1)
#     date_to_ = dt.date(2010, 1, 15)
#     ind_group_ = "Electronics"
    idx_start = df_.index[df_['Dates'] == date_from_]
    idx_end = df_.index[df_['Dates'] == date_to_]
    if ind_group_ == None:
        sel_df = df_.loc[idx_start[0]:idx_end[0]]
    else:
        tickers_list = get_tickers_list_by_ind_group(ind_group_)
        sel_df = df_.loc[idx_start[0]:idx_end[0]][['Dates'] + tickers_list]
    sel_df = sel_df.dropna(axis=1)
    return sel_df
pass

def get_normalized_df(df_):
    norm_df = df_.copy()
    norm_df.iloc[:,1:] = norm_df.iloc[:,1:]/norm_df.iloc[0,1:]
    return norm_df
pass
    
def get_x_trading_day(date_, trad_days_):
    out_date = np.busday_offset(date_, trad_days_, holidays = NYSE_HOLIDAYS)
    return out_date.astype(dt.date)
pass

def get_pairs_list(date_from_, date_to_, ind_group_):
#     date_from_ = dt.date(2010, 1, 1)
#     date_to_ = dt.date(2010, 1, 15)
#     ind_group_ = "Electronics"
    df_ = get_df_from_to(totret_df, date_from_, date_to_, ind_group_)
    norm_df_ = get_normalized_df(df_)
    pairs_list = list(combinations(list(norm_df_.columns.values)[1:],2))
    return pairs_list
pass








dir_path = '/Users/francescoferrari/Desktop/'
ext = '.csv'
close_df = read_df_from_db('PX_LAST')
totret_df = read_df_from_db('TOT_RETURN_INDEX_GROSS_DVDS')



















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
NYSE_HOLIDAYS = get_nyse_holidays(2010, 2018)

def set_end_trading_day(START_DATE_OF_TRADING, END_DATE_OF_TRADING):
    if START_DATE_OF_TRADING < END_DATE_OF_TRADING:
        raise ValueError('Please enter a end trading date that is after the start trading date')
    else:
        return get_x_trading_day(END_DATE_OF_TRADING, 0)
pass

def set_start_trading_day(START_DATE_OF_TRADING):
    start_date_of_trading_temp = get_x_trading_day(START_DATE_OF_TRADING, 0)
    if get_x_trading_day(start_date_of_trading_temp, -LOOK_BACK_DAYS) > START_DATE_OF_DATA:
        return start_date_of_trading_temp
    else:
        raise ValueError('Please enter a START_DATE - LOOK_BACK_DAYS that is after the start DATA date')
pass

print(get_x_trading_day(dt.date(2018, 9, 28), -1))




