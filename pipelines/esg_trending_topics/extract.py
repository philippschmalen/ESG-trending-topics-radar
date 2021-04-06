import pandas as pd
from pytrends.request import TrendReq

# ~------------------ EXTRACT ------------------~
def get_queries(kw_list):
    """ Calls pytrend' related_queries with a list of keywords and geo settings 
    Input
        pytrend: TrendReq() session of pytrend
        kw_list: list of strings, used as input for query and passed to TrendReq().build_payload() 
    Return
        Dataframe with query result
    """    
    assert isinstance(kw_list, list), "Keyword(s) should be a list"

    df_related_queries = pd.DataFrame()

    try:
        pytrend = TrendReq() 

        pytrend.build_payload(kw_list)
        df_related_queries = pytrend.related_queries()

        print(f"Query succeeded for", *kw_list, sep='\n\t')
    except Exception as e:
        print(e, "\nQuery not unsuccessful. Return empty DataFrame.\n", '='*42)

    return df_related_queries