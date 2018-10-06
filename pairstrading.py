'''
Created on 29 Sep 2018

@author: S.Walliser, P.Lucescu, F.Ferrari
'''

import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from itertools import combinations
from nyse_holidays import get_nyse_holidays

def read_df_from_db(field_):
#     field_ = "PX_LAST"
    df = pd.read_csv(DIR_PATH + field_ + EXT, parse_dates=['Dates'])
    return df
pass

def read_industry_info():
    sector_df = pd.read_csv(DIR_PATH + 'SECTOR' + EXT)
    return sector_df
pass

def get_industry_groups():
    sector_df = read_industry_info()
    return np.unique(sector_df.loc[1])
pass

def get_industry_sector():
    sector_df = read_industry_info()
    return np.unique(sector_df.loc[0])
pass

def get_tickers_list_by_ind_gr_sec(ind_gr_sec_):
#     ind_group_ = "Electronics"
    sector_df = read_industry_info()
    idx = sector_df.iloc[0,:] == ind_gr_sec_
    tickers_list = sector_df.columns.values[idx].tolist()
    return tickers_list
pass

def get_df_from_to(df_, date_from_, date_to_,
                   ind_gr_sec_ = None,
                   tickers_list_ = None):
#     date_from_ = dt.date(2010, 1, 1)
#     date_to_ = dt.date(2010, 1, 15)
#     ind_group_ = "Electronics"
    idx_start = df_.index[df_['Dates'] == date_from_]
    idx_end = df_.index[df_['Dates'] == date_to_]
    if tickers_list_ is not None:
        sel_df = df_.loc[idx_start[0]:idx_end[0]][['Dates'] + tickers_list_]
    elif ind_gr_sec_ is not None:
        tickers_list = get_tickers_list_by_ind_gr_sec(ind_gr_sec_)
        sel_df = df_.loc[idx_start[0]:idx_end[0]][['Dates'] + tickers_list]       
    else:
        sel_df = df_.loc[idx_start[0]:idx_end[0]]
    sel_df = sel_df.dropna(axis=1)
    return sel_df
pass

def get_normalized_df(df_):
    norm_df = df_.copy()
    norm_df.iloc[:,1:] = norm_df.iloc[:,1:]/norm_df.iloc[0,1:]*100
    return norm_df
pass
    
def get_x_trading_day(date_, trad_days_):
    output_date = np.busday_offset(date_, trad_days_, holidays = NYSE_HOLIDAYS)
    return output_date.astype(dt.date)
pass

def get_pair_selection_criterium(df_pair_1, df_pair_2_):
    criterium = np.std(df_pair_1 - df_pair_2_)
    return criterium
pass

def get_pairs_ind_gr_sec(df_, date_from_, date_to_, ind_gr_sec_):
#     date_from_ = dt.date(2010, 1, 1)
#     date_to_ = dt.date(2010, 1, 15)
#     ind_gr_sec_ = "Electronics"
    df_ = get_df_from_to(df_, date_from_, date_to_, ind_gr_sec_)
    norm_df_ = get_normalized_df(df_)
    pairs_list = list(combinations(list(norm_df_.columns.values)[1:],2))
    for i, pair in enumerate(pairs_list):
        criterium = get_pair_selection_criterium(norm_df_[pair[0]],
                                                 norm_df_[pair[1]])
        pairs_list[i] = pairs_list[i] + (criterium,)
    return pairs_list
pass

def get_trad_schedule(df_,
                      trad_date_from_,
                      trad_date_to_,
                      est_per_days_,
                      trad_per_days_):
#     est_per_days_ = 21 * 12
#     trad_per_days_ = 21 * 6
#     trad_date_from_ = dt.date(2011, 2, 1)
#     trad_date_to_ = dt.date(2018, 2, 1)
    first_date_data = df_.iloc[0,0].to_pydatetime().date()
    end_date_data = df_.iloc[-1,0].to_pydatetime().date()
    assert trad_date_to_ <= end_date_data
    assert get_x_trading_day(trad_date_from_, -(est_per_days_+1)) >= first_date_data
    date = trad_date_from_
    trad_dates = [tuple((date,
                         get_x_trading_day(date, trad_per_days_)))]
    while date < trad_date_to_:
        trad_date_start = get_x_trading_day(date, trad_per_days_)
        date = trad_dates[-1][1]
        if get_x_trading_day(date, trad_per_days_) >= trad_date_to_:
            trad_date_end = trad_date_to_
        else:
            trad_date_end = get_x_trading_day(date, trad_per_days_)
        trad_dates.append(tuple((trad_date_start, trad_date_end)))
    return trad_dates[:-1]
pass

def get_selected_pairs(df_, date_from_, date_to_, no_pairs_):
#     date_from_ = dt.date(2010, 1, 4)
#     date_to_ = get_x_trading_day(date_from_, 252)
#     no_pairs_ = 2
    sectors = get_industry_sector()
    pairs_list = []
    for sector in sectors:
        pairs_list += get_pairs_ind_gr_sec(df_, date_from_, date_to_, sector)
    pairs_list_sorted = sorted(pairs_list, key = lambda x: x[2])
    pairs_selected = pairs_list_sorted[0:no_pairs_]
    return pairs_selected
pass

def get_postions_pair(df_, date_from_, date_to_, pair_):
#     date_from_ = get_x_trading_day(dt.date(2010, 1, 4), 252 + 1)
#     date_to_ = get_x_trading_day(date_from_, 126)
#     pair_ = ('ED US Equity', 'XEL US Equity', 1.348713804343775)
    debug_msg = 'Getting positions for pair {} and {}'.format(pair_[0],
                                                              pair_[1])
    print(debug_msg)
    pair_df = get_df_from_to(df_, date_from_, date_to_,
                             tickers_list_ = list(pair_[0:2]))
    norm_pair_df = get_normalized_df(pair_df)
    norm_pair_df['diff'] = norm_pair_df.iloc[:,1] - norm_pair_df.iloc[:,2]
    norm_pair_df['abs_diff_le_std'] = np.abs(norm_pair_df.iloc[:,3]) >= 2 * pair_[2]
    norm_pair_df['trade_open'] = np.zeros(norm_pair_df.shape[0], dtype=bool)
    for i in range(norm_pair_df.shape[0]-1):
        if i == 0:
            continue
        if norm_pair_df.iloc[i, 4]:
            norm_pair_df.iloc[i+1:, 5] = True
        if np.sign(norm_pair_df.iloc[i-1, 3]) != np.sign(norm_pair_df.iloc[i, 3]):
            norm_pair_df.iloc[i+1:, 5] = False
            norm_pair_df.iloc[i,3] *= -1
    col_pos_names = [ticker + ' Pos' for ticker in pair_[0:2]]
    norm_pair_df[col_pos_names[0]] = np.sign(norm_pair_df['diff']) * -1 * norm_pair_df['trade_open']
    norm_pair_df[col_pos_names[1]] = np.sign(norm_pair_df['diff']) * norm_pair_df['trade_open']
    norm_pair_df['RF Pos'] = np.ones(norm_pair_df.shape[0]) - np.abs(norm_pair_df[col_pos_names[0]])
    
    # Plot for analysis
    #plt.plot(norm_pair_df['Dates'], norm_pair_df[pair_[0]]/100)
    #plt.plot(norm_pair_df['Dates'], norm_pair_df[pair_[1]]/100)
    #plt.plot(norm_pair_df['Dates'], norm_pair_df[col_pos_names[0]])
    #plt.plot(norm_pair_df['Dates'], norm_pair_df[col_pos_names[1]])
    return norm_pair_df[['Dates', col_pos_names[0], col_pos_names[1], 'RF Pos']]
pass

def merge_positions_df(tot_pos_df_, pair_pos_df_):
    tot_pos_df = tot_pos_df_.copy()
    col_tot_pos_df = tot_pos_df.columns.values[1:]
    col_pair_pos_df = pair_pos_df_.columns.values[1:]
    for col_pair_pos in col_pair_pos_df:
        if col_pair_pos in col_tot_pos_df:
            tot_pos_df[col_pair_pos] += pair_pos_df_[col_pair_pos]
        else:
            tot_pos_df[col_pair_pos] = pair_pos_df_[col_pair_pos]
    return tot_pos_df
pass

def get_df_tot_positions(df_, 
                         trad_date_from_, 
                         trad_date_to_,
                         est_per_trad_days_,
                         no_pairs_):
#     trad_date_from_ = dt.date(2011, 2, 1)
#     trad_date_to_ = get_x_trading_day(trad_date_from_, 126)
#     est_per_trad_days_ = 252
#     no_pairs_ = 50
    est_date_from = get_x_trading_day(trad_date_from_,
                                      -(est_per_trad_days_+1))
    est_date_to = get_x_trading_day(trad_date_from_, -1)
    debug_msg = 'Estimating from {} to {}'.format(est_date_from, est_date_to)
    print(debug_msg)
    pairs_selected = get_selected_pairs(df_, 
                                        est_date_from, 
                                        est_date_to, 
                                        no_pairs_)
    debug_msg = 'Trading from {} to {}'.format(trad_date_from_, trad_date_to_)
    print(debug_msg)
    tot_pos_df = get_postions_pair(df_,
                                   trad_date_from_,
                                   trad_date_to_,
                                   pairs_selected[0])
    for sel_pair in pairs_selected[1:]:
        pair_pos_df = get_postions_pair(df_,
                                        trad_date_from_,
                                        trad_date_to_,
                                        sel_pair)
        tot_pos_df = merge_positions_df(tot_pos_df, pair_pos_df)
    return tot_pos_df
pass

def simulate_trading(totret_df_,
                     trad_date_from_,
                     trad_date_to_,
                     est_per_trad_days_,
                     trad_per_trad_days_,
                     no_pairs_):
    trad_periods = get_trad_schedule(totret_df_,
                                     trad_date_from_,
                                     trad_date_to_,
                                     est_per_trad_days_,
                                     trad_per_trad_days_)
    trad_period_positions = get_df_tot_positions(totret_df_,
                                                 trad_periods[0][0],
                                                 trad_periods[0][1],
                                                 est_per_trad_days_,
                                                 no_pairs_)
    for trad_period in trad_periods[1:]:
        sub_period_positions = get_df_tot_positions(totret_df_,
                                                    trad_period[0],
                                                    trad_period[1],
                                                    est_per_trad_days_,
                                                    no_pairs_)
        trad_period_positions = trad_period_positions.append(sub_period_positions[1:])
    trad_period_positions = trad_period_positions.fillna(value=0)
    return trad_period_positions
pass

def get_log_returns(prices_df_):
    log_returns = prices_df_.copy()
    log_returns.iloc[:,1:] = np.log(prices_df_.iloc[:, 1:].shift(1)) - np.log(prices_df_.iloc[:, 1:])
    return log_returns.fillna(value=0)
pass



# Global Variables
#DIR_PATH = '/Users/francescoferrari/Dropbox (Personal)/HF/Data/'
DIR_PATH = "/Users/Santiago/Dropbox/1_Studium/1_MQF/1_Semester/5 - Strategies at Hedge Funds/2 - Project/SharedProject Folder/Data/"
EXT = '.csv'
NYSE_HOLIDAYS = get_nyse_holidays(2010, 2018)
# Reading data
close_df = read_df_from_db('PX_LAST')

#-------------------------------------------------------------------------------
totret_df = read_df_from_db('TOT_RETURN_INDEX_GROSS_DVDS')
est_per_trad_days = 126 #252
trad_per_trad_days = 21 #126
no_pairs = 10
trad_date_from = dt.date(2011, 2, 1)
trad_date_to = dt.date(2018, 2, 1)
positions_df = simulate_trading(totret_df,
                     trad_date_from,
                     trad_date_to,
                     est_per_trad_days,
                     trad_per_trad_days,
                     no_pairs)


dates = positions_df["Dates"]
positions_df = positions_df.drop(["RF Pos", "Dates"], 1)
ticker_list = [ticker[:-4] for ticker in positions_df.columns]
positions_df.columns = ticker_list
positions_df /= no_pairs # define correct weights
positions_df = pd.concat([dates, positions_df], axis = 1)


prices = get_df_from_to(totret_df, trad_date_from, trad_date_to, tickers_list_= ticker_list)
log_returns = get_log_returns(prices)
ordinary_returns = np.exp(log_returns.iloc[:,1:]) - 1

weighted_log_returns_cum_sum = np.cumsum(np.log(np.sum(ordinary_returns * positions_df.iloc[:,1:], axis = 1) + 1))
weigthed_ordinary_returns_cum_sum = np.exp(weighted_log_returns_cum_sum)
plt.plot(prices['Dates'], weigthed_ordinary_returns_cum_sum)








