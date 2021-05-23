"""
    TRANSFORM
    Create relevant statistics about Google trends data
    for streamlit_app.py

"""

import pandas as pd
import logging
import streamlit as st

def create_query_date(df):
    """ Day format of query_timestamp """
    df['query_date'] = pd.to_datetime(df.query_timestamp).dt.date
    return df

def drop_duplicates(df):
    """ Remove duplicates for anlaysis  """
    df_nodup = df.drop_duplicates(subset=['query', 'value', 'query_date', 'ranking'])
    logging.info(f"Drop {len(df)-len(df_nodup)} duplicates")
    return df_nodup

def trends_statistics(df):
    """Generate relevant statistics for a ranking category of Google trends (rising or top)"""

    # time series indicator: t
    df['t'] = df.groupby('query_date').ngroup()
    # most recent period
    t_max = df.t.max()

    logging.debug(f"df dtypes after adding time series: {df.dtypes}")

    # ranking
    # absolute
    df['rank_t'] = df.groupby('t').value.rank(method='first', ascending=False)
    # rank in previous period (t-1)
    df['rank_t-1'] = df.groupby('query').rank_t.shift()
    # rank change from previous, t-1, to current period, t
    df['rank_absolute_change'] = df.rank_t - df['rank_t-1']
    # winners and loosers (ranking of absoulte changes)
    df['rank_absoulte_change_ranking'] = df.groupby(
        't').rank_absolute_change.rank(method='first', ascending=False)

    # percentile
    df['rank_pct_t'] = df.groupby('t').value.rank(
        method='first', ascending=False, pct=True)
    df['rank_pct_t-1'] = df.groupby('query').rank_pct_t.shift()
    df['rank_pct_change'] = df.rank_pct_t - df['rank_pct_t-1']

    # new entries at time t
    df['new_entry_t'] = (pd.isna(df['rank_t-1']) & pd.notnull(df.rank_t)) * 1

    # dropouts at time t+1
    # keywords for each period  to compare sets
    queries_dict = df.groupby('t')['query'].apply(list).to_dict()
    # compare query responses sets across last two periods
    dropouts = list(
        set(queries_dict[(t_max - 1)]).difference(set(queries_dict[t_max])))
    df['dropout_t+1'] = ((df.t == t_max - 1) & df['query'].isin(dropouts)) * 1

    # fill missings
    df = df.fillna(0)

    return df


def dashboard_data(df):
    """Create statistics for a rank category (rising as default) """   
    df_list = []
    for rank_category in df.ranking.unique().tolist():
        logging.info(f"dashboard_data(): rank category: {rank_category}")
        df = df.loc[df.ranking == rank_category].reset_index(drop=True)
        df_trends = (df.pipe(create_query_date)
                        .pipe(drop_duplicates)
                        .pipe(trends_statistics))
        df_list.append(df_trends)

    return pd.concat(df_list)


# TESTING ------------------------
# import streamlit as st
# import logging
# import sys
# sys.path.append('../')

# from esg_trending_topics.transform import clean_data
# from extract import load_data

# # df_raw = load_data('../../data/2_final', filename='esg_trends_analysis')
# # rising_kw = df_raw.loc[df_raw.ranking == 'rising'].drop_duplicates(subset=['query_date', 'keyword', 'ranking'])
# # '', df_raw.shape
# # '', rising_kw.shape

# kw_raw = load_data(raw_data_dir='../../data/2_final', filename='esg_trends_analysis')
# '', kw_raw
# '', dashboard_data(kw_raw)

# st.stop()

# # -------------------------------