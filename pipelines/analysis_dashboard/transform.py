"""
    TRANSFORM
    Create relevant statistics about Google trends data
    for streamlit_app.py

"""

import pandas as pd

def trends_statistics(df, rank_category='rising'):
    """Generate relevant statistics for a ranking category of Google trends (rising or top)"""
    
    ## subset by Google Trends category: rising or top
    # select only ranking as specified 
    df = df.loc[df.ranking == rank_category].reset_index(drop=True) 
    
    ## datetime
    # timestamp to date
    df['query_date'] = pd.to_datetime(df.query_timestamp).dt.date
    # time series indicator: t
    df['t'] = df.groupby('query_date').ngroup() 
    # most recent period
    t_max = df.t.max() 
    # drop duplicates
    df = df.drop_duplicates(subset=['ranking', 'query', 'query_date'])


    ## ranking 
    # absolute
    df['rank_t'] = df.groupby('t').value.rank(method='first', ascending=False) 
    df['rank_t-1'] = df.groupby('query').rank_t.shift() # rank in previous period (t-1) 
    df['rank_absolute_change'] = df.rank_t - df['rank_t-1'] # rank change from previous, t-1, to current period, t
    # winners and loosers (ranking of absoulte changes)
    df['rank_absoulte_change_ranking'] =  df.groupby('t').rank_absolute_change.rank(method='first', ascending=False)
    
    # percentile
    df['rank_pct_t'] = df.groupby('t').value.rank(method='first', ascending=False, pct=True)
    df['rank_pct_t-1'] = df.groupby('query').rank_pct_t.shift()
    df['rank_pct_change'] = df.rank_pct_t - df['rank_pct_t-1']    

    ## new entries at time t
    df['new_entry_t'] = (pd.isna(df['rank_t-1']) & pd.notnull(df.rank_t))*1
    
    ## dropouts at time t+1
    # keywords for each period  to compare sets
    queries_dict = df.groupby('t')['query'].apply(list).to_dict()
    # compare query responses sets across last two periods 
    dropouts = list(set(queries_dict[(t_max-1)]).difference(set(queries_dict[t_max]))) 
    df['dropout_t+1'] = ((df.t == t_max-1) & df['query'].isin(dropouts))*1

    ## fill missings
    df = df.fillna(0)
    
    return df

def dashboard_data(df):
    """Create statistics for each category and concatenate dataframes """
    ranking_categories = df.ranking.unique().tolist()
    df = pd.concat([trends_statistics(df, rank_category=r) for r in ranking_categories])
    
    return df
