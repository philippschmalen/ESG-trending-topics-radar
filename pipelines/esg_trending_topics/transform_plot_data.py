
import pandas as pd

def add_features(df):
    """ Create normalized values for even display """
    
    assert df.columns.str.contains("query|value|keyword|ranking|timestamp|geo").all(), "Add features failed. \
    Missing one of [query, value, keyword, ranking, timestamp, geo]"
    
    # feature engineering: totals and normalize
    grouped = df.groupby(['ranking']).value # group values by ranking
    df['value_total'] = grouped.transform('sum') # total sum 
    df['value_normalized'] = (df.value-grouped.transform('min'))/(grouped.transform('max')-grouped.transform('min')) # normalize 
    df['value_normalized_total'] = df.groupby(['ranking']).value_normalized.transform('sum') # total sum of normalized values 
    df['date'] = pd.to_datetime(df.query_timestamp).dt.strftime("%d. %B %Y")
    
    return df

def select_topn(df, top_n=25):
    """ Select top-n keywords for each ranking and value_normalized """
    assert df.columns.str.contains("ranking").any(), "select_topn failed. Missing 'ranking' column."
    
    # top-n by ranking
    topn_idx = df.groupby("ranking").value_normalized.nlargest(top_n).droplevel(0).index
    
    return df.loc[topn_idx, : ]

def sanitize_labels(df):
    """ Insert linebreaks and create headings """
    df['labels'] = df['query'].apply(lambda x: x.replace(' ', '<br>')) # linebreaks
    df['ranking_label'] = df.ranking.replace({'top': f'Evergreens - updated {df.date[0]}',
                                              'rising': f'Trending - updated {df.date[0]}'})
    return df

def transform_plot_data(df):
    """ Return 2 dataframes: Newcomer ("rising") and top charts ("top") """
    df = (df.pipe(add_features)
              .pipe(select_topn, top_n=TOP_N)
            .pipe(sanitize_labels))
    
    # rankings: top and rising    
    return df.query('ranking == "rising"'),  df.query('ranking == "top"')
