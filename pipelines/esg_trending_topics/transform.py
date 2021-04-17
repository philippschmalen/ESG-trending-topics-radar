
import pandas as pd
import numpy as np
from datetime import datetime

# ~------------------ RESPONSE DATA ------------------~
def process_response(response, kw, ranking, geo):
    """ Utility function for create_response_df() """
    try:
        df = response[kw][ranking]
        df[['keyword', 'ranking', 'geo', 'query_timestamp']] = [kw, ranking, geo, datetime.now()]
    except:
        print(f"Append empty dataframe for {ranking}: {kw}")
        return pd.DataFrame(columns=['query', 'value', 'keyword', 'ranking', 'geo', 'query_timestamp'])
    
    return df

def create_response_df(response, geo='global'):
    """ Unpack response and create one dataframe for each ranking and each keyword """
    assert isinstance(response, dict), "Empty response, caught in transform.py. Try again." 

    ranking = [*response[[*response][0]]]
    keywords = [*response]

    df_list = []
    for r in ranking: 
        for kw in keywords:
            df_list.append(process_response(response, kw=kw, ranking=r, geo=geo))

    return pd.concat(df_list)

def clean_data(df, blacklist):
    """ Cleans the data
            1. drops non-english strings
            2. removes entries from blacklist
            3. reset index
    
    Args
        df: pd.dataframe, 
        blacklist: list, contains keywords that should be removed
        
    Return
        dataframe
    """
    # remove non-ascii strings: select rows where string has ascii format  
    df_en = df.loc[df['query'].apply(lambda x: x.isascii()), :]

    # remove blacklisted words 
    df_clean = df_en.loc[~df_en['query'].str.contains('|'.join(blacklist)),:]
    
    # reset index
    df = df_clean.reset_index(drop=True)
    
    return df

# ~------------------ PLOT DATA ------------------~
def add_features(df):
    """ Create normalized values for even display """
    
    assert set(["query", "value", "keyword", "ranking", "query_timestamp", "geo"]).issubset(df.columns), "Add features failed. \
    Missing one of [query, value, keyword, ranking, query_timestamp, geo]"
    
    # feature engineering: totals and normalize
    grouped = df.groupby(['ranking']).value # group values by ranking
    df['value_total'] = grouped.transform('sum') # total sum 
    df['value_normalized'] = ((df.value-grouped.transform('min'))/(grouped.transform('max')-grouped.transform('min'))).astype(float) 
    df['value_normalized_total'] = df.groupby(['ranking']).value_normalized.transform('sum') # total sum of normalized values 
    df['date'] = pd.to_datetime(df.query_timestamp).dt.strftime("%d. %B %Y")
    
    return df

def select_topn(df, top_n):
    """ Select top-n keywords for each ranking ordered by value """
    assert df.columns.str.contains("ranking").any(), "select_topn failed. Missing 'ranking' column."

    df = df.reset_index(drop=True)
    df.value = pd.to_numeric(df.value, errors='coerce') # avoid object dtype
    topn_idx = df.groupby("ranking")['value'].nlargest(top_n).droplevel(0).index

    return df.loc[topn_idx, : ]

def sanitize_labels(df, to_uppercase):
    """ Insert linebreaks and create headings """
    # make some labels uppercase
    if to_uppercase:
        for s in to_uppercase:
            df['query'] = df['query'].str.replace(s.lower(), s)
    # create labels
    df['labels'] = df['query'].apply(lambda x: x.replace(' ', '<br>')) # linebreaks
    df['ranking_label'] = df.ranking.replace({'top': f'Evergreens - updated {df.date.to_list()[0]}',
                                              'rising': f'Trending - updated {df.date.to_list()[0]}'})
   
    return df

def plot_data(df, to_uppercase, top_n=35):
    """ Return 2 dataframes: Newcomer ("rising") and top charts ("top") """
    df = (df.pipe(select_topn, top_n=top_n)
            .pipe(add_features)
            .pipe(sanitize_labels, to_uppercase=to_uppercase)
            )

    # rankings: top and rising    
    return df.query('ranking == "rising"'),  df.query('ranking == "top"')
